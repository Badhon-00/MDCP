import importlib.util, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location("gb", Path(__file__).resolve().parent.parent / "scripts" / "github_backup.py")
gb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gb)

TOKEN = "ghp_SECRETTOKEN1234567890abcdefghijklmn"


def sh(*a, cwd=None):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=cwd, check=True, capture_output=True)


def make_source(root, name, commits=1):
    """A bare repo with history, standing in for a GitHub remote."""
    work = root / f"{name}-work"
    work.mkdir()
    sh("init", "-q", "-b", "main", cwd=work)
    for i in range(commits):
        (work / f"f{i}.txt").write_text(f"{name} {i}")
        sh("add", ".", cwd=work)
        sh("commit", "-q", "-m", f"c{i}", cwd=work)
    sh("tag", "v1", cwd=work)
    bare = root / f"{name}.git"
    sh("clone", "-q", "--bare", str(work), str(bare))
    return bare


def fake_repo(owner, name, bare, private=False):
    return {"full_name": f"{owner}/{name}", "clone_url": str(bare), "private": private, "archived": True, "fork": False, "has_wiki": False}


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.a = make_source(self.root, "alpha", commits=3)
        self.b = make_source(self.root, "beta")
        self.empty = self.root / "empty.git"
        sh("init", "-q", "--bare", str(self.empty))
        self.repos = [fake_repo("me", "alpha", self.a, private=True), fake_repo("me", "beta", self.b), fake_repo("me", "empty", self.empty)]
        self.env = mock.patch.dict("os.environ", {"GITHUB_TOKEN": TOKEN})
        self.env.start()
        self.p1 = mock.patch.object(gb, "list_repos", lambda token, aff: self.repos)
        self.p2 = mock.patch.object(gb, "fetch_meta", lambda repo, token: {"repo": repo, "issues": [{"n": 1}], "pulls": [], "issue_comments": [], "releases": []})
        self.p1.start(); self.p2.start()

    def tearDown(self):
        self.p1.stop(); self.p2.stop(); self.env.stop(); self.tmp.cleanup()

    def run_backup(self, *extra):
        out = self.root / "out"
        code = gb.main(["--out", str(out), *extra])
        return code, out

    def test_backs_up_mirror_bundle_and_metadata(self):
        code, out = self.run_backup("--expect", "3")
        self.assertEqual(code, 0)
        self.assertTrue((out / "repos" / "me__alpha.git" / "HEAD").exists())
        bundle = out / "bundles" / "me__alpha.bundle"
        self.assertEqual(subprocess.run(["git", "bundle", "verify", str(bundle)], cwd=out / "repos" / "me__alpha.git", capture_output=True).returncode, 0)
        # the bundle restores full history and tags
        restored = self.root / "restored"
        sh("clone", "-q", str(bundle), str(restored))
        log = subprocess.run(["git", "log", "--oneline"], cwd=restored, capture_output=True, text=True).stdout.strip().splitlines()
        self.assertEqual(len(log), 3)
        self.assertIn("v1", subprocess.run(["git", "tag"], cwd=restored, capture_output=True, text=True).stdout)
        self.assertEqual(json.loads((out / "metadata" / "me__alpha" / "issues.json").read_text()), [{"n": 1}])
        m = json.loads((out / "manifest.json").read_text())
        self.assertEqual((m["repos_found"], m["failed"]), (3, 0))
        self.assertIn("empty repo", [r for r in m["results"] if r["name"] == "me/empty"][0]["status"])

    def test_token_never_written_to_disk(self):
        _, out = self.run_backup()
        import base64
        needles = [TOKEN.encode(), base64.b64encode(f"x-access-token:{TOKEN}".encode())]
        for f in out.rglob("*"):
            if f.is_file():
                data = f.read_bytes()
                for n in needles:
                    self.assertNotIn(n, data, f"token found in {f}")

    def test_expect_mismatch_returns_2(self):
        code, _ = self.run_backup("--expect", "114")
        self.assertEqual(code, 2)

    def test_second_run_updates_existing_mirror(self):
        self.run_backup()
        work = self.root / "alpha-work"
        (work / "new.txt").write_text("new")
        sh("add", ".", cwd=work); sh("commit", "-q", "-m", "later", cwd=work)
        sh("push", "-q", str(self.a), "main", cwd=work)
        _, out = self.run_backup()
        log = subprocess.run(["git", "log", "--oneline", "main"], cwd=out / "repos" / "me__alpha.git", capture_output=True, text=True).stdout.strip().splitlines()
        self.assertEqual(len(log), 4)

    def test_failed_repo_is_reported_not_hidden(self):
        self.repos.append(fake_repo("me", "gone", self.root / "does-not-exist.git"))
        code, out = self.run_backup()
        self.assertEqual(code, 1)
        m = json.loads((out / "manifest.json").read_text())
        self.assertEqual(m["failed"], 1)
        self.assertEqual([r for r in m["results"] if r["status"] == "FAILED"][0]["name"], "me/gone")

    def test_list_only_downloads_nothing(self):
        out = self.root / "out"
        self.assertEqual(gb.main(["--out", str(out), "--list-only"]), 0)
        self.assertFalse(out.exists())

    def test_scrub(self):
        self.assertNotIn(TOKEN, gb.scrub(f"fatal: {TOKEN} bad", TOKEN))


if __name__ == "__main__":
    unittest.main()
