import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "github_backup.py"
spec = importlib.util.spec_from_file_location("github_backup", MODULE)
gb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gb)
TOKEN = "ghp_TEST_TOKEN_0123456789abcdef"


def git(*args, cwd=None):
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", *args], cwd=cwd, check=True, capture_output=True)


def source_repo(root: Path, name: str, commits: int = 2) -> Path:
    work = root / f"{name}-work"
    work.mkdir()
    git("init", "-q", "-b", "main", cwd=work)
    for index in range(commits):
        (work / f"file-{index}.txt").write_text(f"{name}-{index}")
        git("add", ".", cwd=work)
        git("commit", "-q", "-m", f"commit-{index}", cwd=work)
    git("tag", "v1", cwd=work)
    bare = root / f"{name}.git"
    git("clone", "-q", "--bare", str(work), str(bare))
    return bare


class GitHubBackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.alpha = source_repo(self.root, "alpha", 3)
        self.empty = self.root / "empty.git"
        git("init", "-q", "--bare", str(self.empty))
        self.pull_ref = self.root / "pull-work"
        self.pull_ref.mkdir()
        git("init", "-q", "-b", "feature", cwd=self.pull_ref)
        (self.pull_ref / "pull.txt").write_text("pull commit")
        git("add", ".", cwd=self.pull_ref)
        git("commit", "-q", "-m", "pull request head", cwd=self.pull_ref)
        git("update-ref", "refs/pull/7/head", "HEAD", cwd=self.pull_ref)
        git("push", str(self.alpha), "refs/pull/7/head:refs/pull/7/head", cwd=self.pull_ref)
        self.repos = [
            {"full_name": "me/alpha", "clone_url": str(self.alpha), "private": True, "archived": True, "fork": False, "has_wiki": False},
            {"full_name": "me/empty", "clone_url": str(self.empty), "private": False, "archived": False, "fork": False, "has_wiki": False},
        ]
        self.env = mock.patch.dict(os.environ, {"GITHUB_TOKEN": TOKEN})
        self.env.start()
        self.list_patch = mock.patch.object(gb, "list_repositories", lambda token, affiliation: self.repos)
        self.meta_patch = mock.patch.object(gb, "fetch_repository_metadata", lambda repo, token: {"repository": repo, "issues": [], "pull_requests": [], "issue_comments": [], "review_comments": [], "releases": []})
        self.list_patch.start()
        self.meta_patch.start()

    def tearDown(self):
        self.list_patch.stop()
        self.meta_patch.stop()
        self.env.stop()
        self.temp.cleanup()

    def run_backup(self, *args):
        output = self.root / "backup"
        code = gb.main(["--out", str(output), *args])
        return code, output

    def test_mirror_bundle_metadata_and_pull_refs(self):
        code, output = self.run_backup("--expect", "2")
        self.assertEqual(code, 0)
        mirror = output / "repos" / "me__alpha.git"
        self.assertTrue((mirror / "HEAD").exists())
        refs = subprocess.run(["git", "show-ref", "refs/pull/7/head"], cwd=mirror, capture_output=True, text=True)
        self.assertEqual(refs.returncode, 0)
        bundle = output / "bundles" / "me__alpha.bundle"
        subprocess.run(["git", "bundle", "verify", str(bundle)], cwd=mirror, check=True, capture_output=True)
        restored = self.root / "restored"
        git("clone", "-q", str(bundle), str(restored))
        self.assertEqual(len(subprocess.run(["git", "log", "--oneline", "main"], cwd=restored, capture_output=True, text=True).stdout.strip().splitlines()), 3)
        self.assertTrue((output / "metadata" / "me__alpha" / "pull_requests.json").exists())
        manifest = json.loads((output / "manifest.json").read_text())
        self.assertEqual(manifest["failed"], 0)

    def test_secret_is_not_written_to_backup(self):
        _, output = self.run_backup()
        basic = gb.base64.b64encode(f"x-access-token:{TOKEN}".encode()).decode()
        for path in output.rglob("*"):
            if path.is_file():
                data = path.read_bytes()
                self.assertNotIn(TOKEN.encode(), data)
                self.assertNotIn(basic.encode(), data)

    def test_count_mismatch_exit_code(self):
        code, _ = self.run_backup("--list-only", "--expect", "114")
        self.assertEqual(code, 2)

    def test_existing_mirror_updates(self):
        self.run_backup("--no-meta", "--no-wiki")
        work = self.root / "alpha-work"
        (work / "later.txt").write_text("later")
        git("add", ".", cwd=work)
        git("commit", "-q", "-m", "later", cwd=work)
        git("push", "-q", str(self.alpha), "main", cwd=work)
        _, output = self.run_backup("--no-meta", "--no-wiki")
        log = subprocess.run(["git", "log", "--oneline", "main"], cwd=output / "repos" / "me__alpha.git", capture_output=True, text=True).stdout.strip().splitlines()
        self.assertEqual(len(log), 4)

    def test_missing_repository_is_reported(self):
        self.repos.append({"full_name": "me/missing", "clone_url": str(self.root / "absent.git"), "private": True, "archived": False, "fork": False, "has_wiki": False})
        code, output = self.run_backup()
        self.assertEqual(code, 1)
        self.assertEqual(json.loads((output / "manifest.json").read_text())["failed"], 1)

    def test_list_only_does_not_create_output(self):
        output = self.root / "list-only"
        code = gb.main(["--out", str(output), "--list-only"])
        self.assertEqual(code, 0)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
