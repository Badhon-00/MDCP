# auto-git-manager.md

- Before editing: `git status`. Work on a branch, not `main`.
- Commit small, one purpose each, message says why.
- Before committing: `git diff --staged`; confirm no `.env`, keys or tokens.
- Do not push, open a PR, or force-push unless asked. Never rewrite shared history.
- Revert with `git revert` or `git restore` on the specific files; do not discard unrelated changes.
- `.gitignore` covers `.env*`, `node_modules`, build output.
