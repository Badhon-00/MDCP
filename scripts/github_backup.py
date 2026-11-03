#!/usr/bin/env python3
"""Back up GitHub repositories you own (public, private and archived).

Requires Python 3.10+ and git. Uses GITHUB_TOKEN or GH_TOKEN from the environment.
The token is sent in request headers only; it is never written to the backup.
"""
from __future__ import annotations
import argparse
import base64
import concurrent.futures as futures
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

API = "https://api.github.com"
USER_AGENT = "mdcp-github-backup/1.0"


def scrub(value: str, token: str) -> str:
    if not token:
        return value
    basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    return value.replace(token, "[REDACTED]").replace(basic, "[REDACTED]")


def api_pages(url: str, token: str):
    while url:
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, list):
                raise RuntimeError("GitHub API returned an unexpected list response")
            yield from payload
            match = re.search(r'<([^>]+)>;\s*rel="next"', response.headers.get("Link", ""))
            url = match.group(1) if match else None


def list_repositories(token: str, affiliation: str) -> list[dict]:
    return list(api_pages(f"{API}/user/repos?per_page=100&visibility=all&affiliation={affiliation}&sort=full_name", token))


def list_gists(token: str) -> list[dict]:
    return list(api_pages(f"{API}/gists?per_page=100", token))


def git(args: list[str], token: str = "", cwd: Path | None = None) -> tuple[int, str]:
    env = os.environ.copy()
    if token:
        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        env["GIT_CONFIG_COUNT"] = "1"
        env["GIT_CONFIG_KEY_0"] = "http.extraHeader"
        env["GIT_CONFIG_VALUE_0"] = f"Authorization: Basic {basic}"
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, env=env)
    return result.returncode, scrub((result.stdout + result.stderr).strip(), token)


def mirror_repository(url: str, destination: Path, token: str) -> tuple[bool, str]:
    if (destination / "HEAD").is_file():
        code, output = git(["remote", "update", "--prune"], token, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        code, output = git(["clone", "--mirror", url, str(destination)], token)
    if code:
        return False, output
    # GitHub's pull-request refs are not advertised by the normal mirror refspec.
    # Fetch them explicitly so closed PR commits survive the backup.
    code, output = git(["fetch", "origin", "+refs/pull/*/head:refs/pull/*/head", "+refs/pull/*/merge:refs/pull/*/merge"], token, destination)
    if code:
        return True, "pull-request refs unavailable: " + output[-240:]
    return True, output


def fetch_repository_metadata(repo: dict, token: str) -> dict:
    full_name = repo["full_name"]
    result = {"repository": repo}
    endpoints = {
        "issues": f"repos/{full_name}/issues?state=all&per_page=100",
        "pull_requests": f"repos/{full_name}/pulls?state=all&per_page=100",
        "issue_comments": f"repos/{full_name}/issues/comments?per_page=100",
        "review_comments": f"repos/{full_name}/pulls/comments?per_page=100",
        "releases": f"repos/{full_name}/releases?per_page=100",
    }
    for key, endpoint in endpoints.items():
        try:
            result[key] = list(api_pages(f"{API}/{endpoint}", token))
        except Exception as exc:
            result[key] = {"error": scrub(f"{type(exc).__name__}: {exc}", token)}
    return result


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_repo_name(full_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", full_name)


def backup_repository(repo: dict, output: Path, token: str, include_metadata: bool, include_wiki: bool) -> dict:
    full_name = repo["full_name"]
    name = safe_repo_name(full_name)
    result = {"name": full_name, "private": repo.get("private"), "archived": repo.get("archived"), "fork": repo.get("fork"), "status": "ok"}
    mirror = output / "repos" / f"{name}.git"
    ok, note = mirror_repository(repo["clone_url"], mirror, token)
    if not ok:
        return {**result, "status": "FAILED", "error": note[-500:]}
    result["pull_request_refs"] = "fetched" if not note.startswith("pull-request refs unavailable") else note

    code, message = git(["fsck", "--connectivity-only"], cwd=mirror)
    if code:
        return {**result, "status": "FAILED", "error": "git fsck: " + message[-400:]}

    bundle = output / "bundles" / f"{name}.bundle"
    bundle.parent.mkdir(parents=True, exist_ok=True)
    code, message = git(["bundle", "create", str(bundle), "--all"], cwd=mirror)
    if code and "empty bundle" in message.lower():
        result["bundle"] = "empty repository; no bundle created"
    elif code:
        return {**result, "status": "FAILED", "error": "git bundle create: " + message[-400:]}
    else:
        code, message = git(["bundle", "verify", str(bundle)], cwd=mirror)
        if code:
            return {**result, "status": "FAILED", "error": "git bundle verify: " + message[-400:]}
        result["bundle_sha256"] = file_sha256(bundle)

    if include_wiki and repo.get("has_wiki"):
        wiki_url = repo["clone_url"].removesuffix(".git") + ".wiki.git"
        wiki_ok, wiki_note = mirror_repository(wiki_url, output / "wikis" / f"{name}.wiki.git", token)
        result["wiki"] = "ok" if wiki_ok else "unavailable: " + wiki_note[-200:]

    if include_metadata:
        metadata = fetch_repository_metadata(repo, token)
        folder = output / "metadata" / name
        folder.mkdir(parents=True, exist_ok=True)
        for key, value in metadata.items():
            (folder / f"{key}.json").write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
        result["metadata_counts"] = {key: len(value) if isinstance(value, list) else "error" for key, value in metadata.items() if key != "repository"}
    return result


def write_manifest(output: Path, repos_found: int, expected: int | None, results: list[dict]) -> None:
    manifest = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repositories_found": repos_found,
        "expected_repositories": expected,
        "completed": len(results),
        "failed": sum(item.get("status") == "FAILED" for item in results),
        "results": sorted(results, key=lambda item: item["name"].lower()),
    }
    temporary = output / "manifest.json.tmp"
    temporary.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(output / "manifest.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=f"github-backup-{dt.date.today().isoformat()}")
    parser.add_argument("--affiliation", default="owner", help="owner by default; optionally owner,collaborator,organization_member")
    parser.add_argument("--expect", type=int, help="expected repository count; mismatch exits 2")
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--gists", action="store_true")
    parser.add_argument("--no-meta", action="store_true")
    parser.add_argument("--no-wiki", action="store_true")
    parser.add_argument("--list-only", action="store_true")
    args = parser.parse_args(argv)

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        print("Set GITHUB_TOKEN (or GH_TOKEN) in your shell; never paste it into a file.", file=sys.stderr)
        return 2
    repos = list_repositories(token, args.affiliation)
    public_count = sum(not bool(repo.get("private")) for repo in repos)
    private_count = len(repos) - public_count
    archived_count = sum(bool(repo.get("archived")) for repo in repos)
    print(f"Found {len(repos)} repositories: {public_count} public, {private_count} private, {archived_count} archived")
    exit_code = 0
    if args.expect is not None and args.expect != len(repos):
        print(f"Count mismatch: expected {args.expect}, found {len(repos)}. Check token access and --affiliation.", file=sys.stderr)
        exit_code = 2
    if args.list_only:
        for repo in sorted(repos, key=lambda item: item["full_name"].lower()):
            print(("private " if repo.get("private") else "public  ") + repo["full_name"])
        return exit_code

    output = Path(args.out).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with futures.ThreadPoolExecutor(max_workers=max(1, min(args.jobs, 8))) as pool:
        jobs = {pool.submit(backup_repository, repo, output, token, not args.no_meta, not args.no_wiki): repo for repo in repos}
        for index, future in enumerate(futures.as_completed(jobs), 1):
            try:
                item = future.result()
            except Exception as exc:
                item = {"name": jobs[future].get("full_name", "unknown"), "status": "FAILED", "error": scrub(f"{type(exc).__name__}: {exc}", token)}
            results.append(item)
            write_manifest(output, len(repos), args.expect, results)
            print(f"[{index}/{len(repos)}] {item['status']:<6} {item['name']}")

    if args.gists:
        try:
            for gist in list_gists(token):
                name = f"gist:{gist['id']}"
                ok, note = mirror_repository(gist["git_pull_url"], output / "gists" / f"{gist['id']}.git", token)
                results.append({"name": name, "status": "ok" if ok else "FAILED", "error": None if ok else note[-300:]})
                write_manifest(output, len(repos), args.expect, results)
        except Exception as exc:
            results.append({"name": "gists", "status": "FAILED", "error": scrub(f"{type(exc).__name__}: {exc}", token)})

    write_manifest(output, len(repos), args.expect, results)
    failed = sum(item.get("status") == "FAILED" for item in results)
    print(f"Finished: {len(repos)} repositories discovered, {failed} failures. Manifest: {output / 'manifest.json'}")
    if failed:
        return 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
