#!/usr/bin/env python3
"""Back up every repository of your GitHub account (public and private, archived included).

Per repo it writes: a full mirror (all branches, tags, and refs/pull/* so closed PR commits survive),
a single-file git bundle, and JSON for repo info, issues, pull requests, comments and releases.
Optionally also wikis and gists. Standard library plus the `git` command only.

  export GITHUB_TOKEN=...            # classic token with `repo`, or fine-grained read-only (Contents, Metadata, Issues, Pull requests) on all repos
  python3 scripts/github_backup.py --out ~/github-backup --expect 114
  python3 scripts/github_backup.py --list-only          # count and list repos, clone nothing

Re-run any time: existing mirrors are updated, not re-downloaded.
The token is sent in an HTTP header for each git command only. It is never written to disk or into .git/config.
The output holds your private code. Keep it on storage you control and encrypt it before it leaves your machine.
"""
import argparse, base64, concurrent.futures as cf, datetime, hashlib, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

API = "https://api.github.com"


def api_pages(url, token):
    """Yield every item of a paginated GitHub list endpoint."""
    while url:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "mdcp-github-backup"})
        with urllib.request.urlopen(req, timeout=60) as r:
            yield from json.loads(r.read().decode())
            m = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get("Link", ""))
            url = m.group(1) if m else None


def list_repos(token, affiliation):
    return list(api_pages(f"{API}/user/repos?per_page=100&visibility=all&affiliation={affiliation}", token))


def list_gists(token):
    return list(api_pages(f"{API}/gists?per_page=100", token))


def fetch_meta(repo, token):
    full = repo["full_name"]
    out = {"repo": repo}
    for name, path in [("issues", "issues?state=all"), ("pulls", "pulls?state=all"), ("issue_comments", "issues/comments"), ("releases", "releases")]:
        sep = "&" if "?" in path else "?"
        try:
            out[name] = list(api_pages(f"{API}/repos/{full}/{path}{sep}per_page=100", token))
        except Exception as e:  # e.g. issues disabled
            out[name] = {"error": scrub(str(e), token)}
    return out


def scrub(text, token):
    return text.replace(token, "***") if token else text


def git(args, token, cwd=None):
    cmd = ["git"]
    if token:
        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        cmd += ["-c", f"http.extraHeader=Authorization: Basic {basic}"]
    p = subprocess.run(cmd + args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, scrub((p.stdout + p.stderr).strip(), token)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mirror(url, dest, token):
    """Clone --mirror, or update an existing mirror. Returns (ok, message)."""
    if (dest / "HEAD").exists():
        rc, msg = git(["remote", "update", "--prune"], token, cwd=dest)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        rc, msg = git(["clone", "--mirror", url, str(dest)], token)
    return rc == 0, msg


def backup_repo(repo, out, token, meta=True, wiki=True):
    name = repo["full_name"].replace("/", "__")
    res = {"name": repo["full_name"], "private": repo.get("private"), "archived": repo.get("archived"), "fork": repo.get("fork"), "status": "ok"}
    ok, msg = mirror(repo["clone_url"], out / "repos" / f"{name}.git", token)
    if not ok:
        return {**res, "status": "FAILED", "error": msg[-400:]}
    mdir = out / "repos" / f"{name}.git"
    rc, msg = git(["fsck", "--connectivity-only"], None, cwd=mdir)
    if rc != 0:
        return {**res, "status": "FAILED", "error": "fsck: " + msg[-300:]}
    bundle = out / "bundles" / f"{name}.bundle"
    bundle.parent.mkdir(parents=True, exist_ok=True)
    rc, msg = git(["bundle", "create", str(bundle), "--all"], None, cwd=mdir)
    if rc != 0 and "empty bundle" in msg:
        res["status"] = "ok (empty repo)"
    elif rc != 0:
        return {**res, "status": "FAILED", "error": "bundle: " + msg[-300:]}
    else:
        rc, msg = git(["bundle", "verify", str(bundle)], None, cwd=mdir)
        if rc != 0:
            return {**res, "status": "FAILED", "error": "bundle verify: " + msg[-300:]}
        res["bundle_sha256"] = sha256(bundle)
    if wiki and repo.get("has_wiki"):
        ok_w, _ = mirror(repo["clone_url"][:-4] + ".wiki.git", out / "wikis" / f"{name}.wiki.git", token)
        res["wiki"] = "ok" if ok_w else "none or not accessible"
    if meta:
        data = fetch_meta(repo, token)
        d = out / "metadata" / name
        d.mkdir(parents=True, exist_ok=True)
        for k, v in data.items():
            (d / f"{k}.json").write_text(json.dumps(v, indent=2, ensure_ascii=False), encoding="utf-8")
        res["issues_and_prs"] = {k: (len(v) if isinstance(v, list) else "error") for k, v in data.items() if k != "repo"}
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=f"github-backup-{datetime.date.today()}")
    ap.add_argument("--affiliation", default="owner", help="owner (default), or e.g. owner,collaborator,organization_member")
    ap.add_argument("--expect", type=int, help="number of repos you expect; the run fails loudly if it differs")
    ap.add_argument("--jobs", type=int, default=3, help="parallel repos (default 3)")
    ap.add_argument("--gists", action="store_true", help="also mirror your gists")
    ap.add_argument("--no-meta", action="store_true", help="skip issues/PRs/releases JSON")
    ap.add_argument("--no-wiki", action="store_true")
    ap.add_argument("--list-only", action="store_true", help="list repos and counts, download nothing")
    a = ap.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("Set GITHUB_TOKEN first (see --help).")
    repos = list_repos(token, a.affiliation)
    pub = sum(1 for r in repos if not r["private"])
    print(f"Found {len(repos)} repositories: {pub} public, {len(repos) - pub} private, {sum(1 for r in repos if r['archived'])} archived, {sum(1 for r in repos if r['fork'])} forks")
    exit_code = 0
    if a.expect is not None and a.expect != len(repos):
        print(f"WARNING: expected {a.expect} but found {len(repos)}. Check the token's access, organization repos (--affiliation), or repos you no longer own.")
        exit_code = 2
    if a.list_only:
        for r in sorted(repos, key=lambda r: r["full_name"].lower()):
            print(("private " if r["private"] else "public  ") + r["full_name"])
        return exit_code

    out = Path(a.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        futs = {pool.submit(backup_repo, r, out, token, not a.no_meta, not a.no_wiki): r for r in repos}
        for i, f in enumerate(cf.as_completed(futs), 1):
            try:
                res = f.result()
            except Exception as e:
                res = {"name": futs[f]["full_name"], "status": "FAILED", "error": scrub(str(e), token)}
            results.append(res)
            print(f"[{i}/{len(repos)}] {res['status']:<18} {res['name']}" + (f"  {res.get('error', '')[:120]}" if res["status"] == "FAILED" else ""))
    if a.gists:
        for g in list_gists(token):
            ok, msg = mirror(g["git_pull_url"], out / "gists" / f"{g['id']}.git", token)
            results.append({"name": f"gist:{g['id']}", "status": "ok" if ok else "FAILED", "error": None if ok else msg[-200:]})

    failed = [r for r in results if r["status"] == "FAILED"]
    manifest = {"created": datetime.datetime.now(datetime.timezone.utc).isoformat(), "repos_found": len(repos), "expected": a.expect, "failed": len(failed), "results": sorted(results, key=lambda r: r["name"].lower())}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nDone: {len(results) - len(failed)} ok, {len(failed)} failed. Manifest: {out / 'manifest.json'}")
    if failed:
        print("Re-run the same command to retry the failed ones.")
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
