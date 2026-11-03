# Back up your GitHub repositories

The script scripts/github_backup.py exports repositories visible to your personal GitHub account, including public, private and archived repositories. It creates a Git mirror, a verified bundle, and JSON metadata. It is designed to run on your own computer—not in Actions on the same GitHub account.

## Requirements

- Python 3.10+
- Git installed and available as git
- A GitHub token with read-only access to every repository you want to back up

## What is included

| Output | Contents |
|---|---|
| repos/<owner>__<repo>.git | Mirror of branches and tags, plus GitHub pull-request head/merge refs where available |
| bundles/<owner>__<repo>.bundle | Portable Git bundle with a SHA-256 checksum, verified after creation |
| metadata/<owner>__<repo>/ | Repository metadata, issues, pull requests, issue comments, review comments and releases as JSON |
| wikis/ | Wiki mirrors when enabled and available |
| gists/ | Optional gist mirrors when --gists is selected |
| manifest.json | Progress, repository count, per-repository status, errors and checksums |

The script writes a manifest after each completed repository, so interrupted runs leave a useful progress record. Re-running updates existing mirrors and retries failed repositories.

## What is not included

This is a repository backup, not a complete GitHub account image. It does not export Actions secrets/variables, repository settings, branch protection, Pages settings, Projects, Discussions, packages/container images, stars/followers, release binary assets, or Git LFS object contents (only Git LFS pointer files). Metadata JSON is an archive, not an importable recreation of original GitHub issues/PRs. Review the manifest and keep separate records of important account settings.

## 1. Create a read-only token

GitHub → Settings → Developer settings → Personal access tokens.

For a fine-grained token:
- Resource owner: your account
- Repository access: **All repositories**
- Permissions: Contents (read), Metadata (read), Issues (read), Pull requests (read)
- Add Gists (read) only if using --gists

A classic token with repo scope can also read private repositories, but it is broader. Set an expiry and revoke it after the backup.

## 2. Check repository visibility/count first

Never paste the token into chat or commit it. Set it in the shell environment:

~~~bash
export GITHUB_TOKEN='YOUR_TOKEN'
python3 scripts/github_backup.py --list-only --expect 114
~~~

The --expect 114 check is a guard, not an assertion that the account actually has 114 repositories. If the count differs, check token access and whether some repositories belong to organizations. For organization memberships, try --affiliation owner,organization_member; that may include repositories you can access but do not personally own.

## 3. Run the backup

~~~bash
python3 scripts/github_backup.py --out ~/github-backup --expect 114 --gists
~~~

Use --no-meta to skip issue/PR/release JSON, --no-wiki to skip wikis, and --jobs 2 for a slower, lower-bandwidth run. The worker count is capped at 8.

Exit codes:
- 0: all repositories backed up and the expected count matched (or no expected count was supplied)
- 1: one or more backup failures; inspect the manifest and rerun
- 2: missing token or repository-count mismatch

Check manifest.json: the failed count must be zero. Also verify a restore manually:

~~~bash
git clone ~/github-backup/bundles/OWNER__REPO.bundle /tmp/restore-test
~~~

For a mirror restore to another Git host, create an empty private repository there and push from the mirror:

~~~bash
cd ~/github-backup/repos/OWNER__REPO.git
git push --mirror https://gitlab.com/YOUR_ACCOUNT/REPO.git
~~~

## Keep the backup independent and private

- Keep at least three copies on two storage types, with one off-site.
- Encrypt private backups before uploading or moving them to external storage.
- Store the encryption passphrase in a password manager, not beside the archive.
- Do not store the only backup in GitHub Actions or in another repository under the same GitHub account.
- Never commit the token. The script sends it in HTTP headers and scrubs it from command output, but the host process and network must still be trusted.

## Archived repositories and pull requests

Archived repositories are read-only but can still be cloned. The script includes them in the repository list. GitHub does not have an "archive pull request" action: a pull request is open, closed or merged. The mirror attempts to fetch refs/pull/*/head and refs/pull/*/merge; a repository without accessible PR refs still receives its ordinary branch/tag mirror. If you accidentally archived a repository, first make a backup, then unarchive it through Repository → Settings → General → Danger Zone.
