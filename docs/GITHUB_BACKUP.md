# Back up your whole GitHub account

`scripts/github_backup.py` copies every repository you own, public and private, archived ones included, to storage you control. If the account is ever locked, suspended or deleted, you can restore from it anywhere.

It needs Python 3.8+ and `git`. Nothing else to install.

## What you get

For each repository, under the output folder:

| Folder | Content |
|---|---|
| `repos/<owner>__<repo>.git` | Full mirror: every branch, tag and `refs/pull/*` (so commits from closed pull requests survive) |
| `bundles/<owner>__<repo>.bundle` | The same history as one portable file, verified after creation |
| `metadata/<owner>__<repo>/` | JSON: repository info, issues, pull requests, issue comments, releases |
| `wikis/` | Wiki repositories, where the repo has one (`--no-wiki` to skip) |
| `gists/` | With `--gists` |
| `manifest.json` | Per-repo result, counts, SHA-256 of each bundle, failures |

## What it does not back up

Git does not hold these, so they are not in the backup: Actions secrets and variables, branch protection and other settings, GitHub Pages settings, Projects boards, Discussions, packages and container images, stars, followers, and Git LFS file contents (only the pointers). Write down the settings you care about, and keep your secrets in a password manager.

## Steps

1. **Make a token.** GitHub, Settings, Developer settings, Personal access tokens.
   - Fine-grained: Resource owner = you, Repository access = **All repositories**, permissions (read-only): Contents, Metadata, Issues, Pull requests.
   - Or a classic token with the `repo` scope (and `gist` if you use `--gists`).
   - Set an expiry. Revoke it when the backup is done.
2. **Put it in your shell, not in a file or a chat.**
   ```bash
   export GITHUB_TOKEN=ghp_xxx          # Windows PowerShell: $env:GITHUB_TOKEN="ghp_xxx"
   ```
3. **Check the count first.** You said 114; confirm the script sees all of them:
   ```bash
   python3 scripts/github_backup.py --list-only --expect 114
   ```
   If the count is lower, the token cannot see some repos (use All repositories), or some belong to an organization (add `--affiliation owner,organization_member`). Exit code 2 means the count did not match.
4. **Run the backup.**
   ```bash
   python3 scripts/github_backup.py --out ~/github-backup --expect 114 --gists
   ```
   Run it again later: existing mirrors are updated, only new data is downloaded. Failed repos are listed and the exit code is 1. Re-run to retry.
5. **Check `manifest.json`.** `failed` should be 0. Spot-check one restore:
   ```bash
   git clone ~/github-backup/bundles/<owner>__<repo>.bundle /tmp/restore-test
   ```

## Keep it safe (private code is in there)

- Follow 3-2-1: three copies, two kinds of storage, one off-site.
- Encrypt before the folder leaves your machine:
  ```bash
  tar -cf - -C ~ github-backup | gpg --symmetric --cipher-algo AES256 -o github-backup.tar.gpg
  ```
  Store the passphrase in a password manager, not next to the file.
- A second git host is the easiest off-site copy. Create an empty private repo there, then:
  ```bash
  cd ~/github-backup/repos/<owner>__<repo>.git
  git push --mirror https://gitlab.com/<you>/<repo>.git
  ```
- Do not run this backup from GitHub Actions of the same account and store the result there. A backup that lives inside the account is lost with it, and a token that can read all your private repos should not sit in CI secrets. Use your own computer, a home server, or another provider's scheduler (cron on Linux/macOS, Task Scheduler on Windows).

## Restore

- One repo: `git clone repo.bundle` gives a normal working copy. To put it on a new host: create an empty repo there, then `git push --mirror <new-url>` from the `.git` mirror folder.
- Issues and pull requests cannot be re-imported into GitHub as originals; the JSON is a readable archive. For a full-fidelity move between hosts, see GitHub's migration tools in its docs.

## Lowering the risk of losing the account

- Turn on two-factor authentication, add a passkey or security key, and **save the recovery codes offline**. Losing 2FA with no recovery codes is the most common way people are locked out.
- Add a second verified email you control.
- Keep a second owner on any organization you rely on.
- Never put tokens in code or workflow files; use repository secrets and rotate any token you have pasted somewhere.
- Ordinary CI use is fine, but abusing Actions (mining, scraping, spam, bulk automation of accounts) can get an account restricted. Follow GitHub's terms and Actions usage rules.

## Archived repositories

GitHub has no way to "archive" pull requests. If you archived repositories by mistake, they are now read-only: pushes fail and Actions will not run on them. Undo it per repo: repository, Settings, General, scroll to Danger Zone, **Unarchive this repository**. The backup includes archived repositories, so you can run it first and unarchive afterwards. Closed pull requests can be reopened if their branch still exists.
