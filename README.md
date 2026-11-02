# MDCP: Master Developer Claude Plugin

[![validate](https://github.com/Badhon-00/MDCP/actions/workflows/validate.yml/badge.svg)](https://github.com/Badhon-00/MDCP/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

One plugin for Claude Code with **82 skills** for building, securing, testing and shipping web software: a core `master-developer` skill with 35 on-demand rule files, a Claude-Code token meter, and a curated set of open-source skills for design, Three.js, backend, workflow and plugin/MCP development. Every bundled skill keeps its original license and is credited in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Install

In Claude Code:

```
/plugin marketplace add Badhon-00/MDCP
/plugin install mdcp@mdcp-marketplace
```

Only want a few skills? Copy the folders you need from `skills/` into `~/.claude/skills/` (all projects) or `<project>/.claude/skills/`. Each skill is self-contained.

## What is inside

| Area | Skills |
|---|---|
| Core (3) | `master-developer` (rules, security, API, DB, UI, testing, deploy; opens only the file a task needs), `mdcp-self-check` (checks before "done", defense review, self-debug), `mdcp-token-meter` |
| Security and quality (9) | `security-review`, `security-scan`, `agent-security-hardening`, `mcp-dependency-review`, `tdd-workflow`, `verification-loop`, `coding-standards`, `e2e-testing`, `webapp-testing` |
| Backend and data (7) | `api-design`, `backend-patterns`, `database-migrations`, `postgres-patterns`, `prisma-patterns`, `docker-patterns`, `deployment-patterns` |
| Frontend (7) | `frontend-patterns`, `frontend-a11y`, `nextjs-turbopack`, `web-design-guidelines`, `react-best-practices`, `composition-patterns`, `react-view-transitions` |
| Design (7) | `frontend-design`, `ui-ux-pro-max` (searchable palettes, fonts, styles, UX rules), `canvas-design`, `algorithmic-art`, `brand-guidelines`, `theme-factory`, `web-artifacts-builder` |
| Three.js (13) | fundamentals, geometry, materials, lighting, textures, animation, interaction, loaders, shaders, postprocessing, performance, asset pipeline, react-three-fiber |
| Workflow (11) | `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `requesting-code-review`, `receiving-code-review`, `finishing-a-development-branch`, `dispatching-parallel-agents`, `using-git-worktrees`, `subagent-driven-development` |
| Clean-room app cloning (11) | `replica-recon` to `replica-deploy`: study an app's features from public sources, rebuild them from scratch, rebrand before launch |
| Build your own (14) | `skill-creator`, `plugin-structure`, `skill-development`, `command-development`, `agent-development`, `hook-development`, `plugin-settings`, `mcp-integration`, `build-mcp-server`, `build-mcpb`, `build-mcp-app`, `mcp-builder`, `claude-md-improver`, `claude-api` |

Also in the repo: [`mcp/`](mcp/README.md) (setup for Context7, Supabase, Figma, Playwright, with what was verified) and [`scripts/token-meter.py`](scripts/token-meter.py).

## Examples

- "Review this PR for security problems" loads `security-review` and `master-developer`'s OWASP Top 10:2025 checklist.
- "Add a Prisma model and an API route" loads `prisma-patterns`, `api-design` and the Next.js data-access rules.
- "Make a 3D hero section" loads the Three.js skills and `frontend-design`.
- "Why does this test fail?" loads `systematic-debugging`.

Skills load by their description, so a request that matches one is enough. You do not need to name it.

## Token meter

```bash
python3 scripts/token-meter.py              # context in use, output tokens, cache counts
python3 scripts/token-meter.py --statusline # one line for the Claude Code status bar
```

It reads the Claude Code session transcript. It shows session context, not plan quota (use `/usage` for that), and it does not see claude.ai web chats.

## How this repo is run

- **Curated, not copied blind.** Skills come from open-source projects, listed with license and what was left out and why. Hooks and anything that starts a local server or runs code unprompted are not bundled.
- **Checked on every push.** `scripts/validate.py` (run by CI) verifies JSON manifests, frontmatter, unique skill names and credits. It checks structure; it does not prove a skill behaves well. Third-party skills are not security audited. Read a skill before relying on it.
- **Rules guide, tests enforce.** The rule files shape how Claude works. Your build, type checker, tests and scanners decide whether code is right.
- **More skills are not always better.** Each skill's description is loaded into context. If you only build Next.js apps, copy only what you use.

## Contributing

Issues and pull requests are welcome: a bug in a rule, an outdated command, a missing skill, a license problem. See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports go through [SECURITY.md](SECURITY.md).

```bash
python3 scripts/validate.py   # run before opening a PR
```

## License

MIT for this repository's own files ([LICENSE](LICENSE)). Bundled skills are under their own licenses (MIT or Apache-2.0); see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [`licenses/`](licenses/).
