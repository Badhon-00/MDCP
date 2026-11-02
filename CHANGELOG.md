# Changelog

## 1.8.0
- Added `scripts/github_backup.py`: full mirror, verified bundles and metadata of all your repositories, with tests and a guide (`docs/GITHUB_BACKUP.md`).
- Added `docs/DOMAIN_AND_OWNERSHIP.md`: custom domain for Pages, what is yours to own, trademark notes.
- Fixed: CI actions moved to Node 24 versions (checkout v6, setup-python v6, upload-pages-artifact v5, deploy-pages v5), removing the Node 20 deprecation warning.
- Fixed: the agent fabric now refuses a non-HTTPS `MDCP_LLM_BASE_URL` (except localhost) so API keys and code are not sent unencrypted.
- CI now runs every test in `tests/`. `site/catalog.json` is generated, not committed. Notices list the original skills.

## 1.5.0
- Repository docs: README rewrite, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, issue and PR templates.
- CI and `scripts/validate.py` (manifests, frontmatter, unique names, credits).

## 1.4.0
- Added Superpowers workflow skills (11) and Anthropic plugin and MCP development skills (11).

## 1.3.0
- Added Anthropic design skills, UI/UX Pro Max, `mcp/` setup guide.

## 1.2.0
- Added Vercel skills, Three.js skills, `mdcp-self-check`, `mdcp-token-meter`.

## 1.1.0
- Added ECC, awesome-claude-skills and replica-skill skills.

## 1.0.0
- `master-developer` skill with 35 rule files.
