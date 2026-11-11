# Cross-Platform Skill and Plugin Distribution

Canonical skills live in `skills/<name>/SKILL.md`; portable copies are mirrored under `.agents/skills/` and `.gpt/skills/`.

| Host | Usage |
|---|---|
| Claude Code | Install the MDCP marketplace plugin; native skills and agent prompts are included |
| Claude.ai | Import skill Markdown into a Project or supported workflow; no Claude Code CLI is installed |
| Codex CLI | Follow root `AGENTS.md` and use portable `.agents/skills/` |
| ChatGPT | Import selected Markdown into a Project or Custom GPT instructions/knowledge; configure connectors separately |
| OmniRoute | Optional gateway for compatible API/CLI clients; it does not redirect hosted web inference |

Build a portable archive with `python scripts/package_skills.py --output dist/mdcp-skills.zip`. Review third-party notices before redistribution. A Claude Code plugin is not itself a ChatGPT plugin. Skills cannot grant account permissions, credentials, shell access or background execution.

## Unified Creator + Security toolkit

Import `skills/creator-security-automation/SKILL.md` as the umbrella skill; the same short entrypoint is mirrored in `.agents/skills/` and `.gpt/skills/`. Where an MCP connection is supported, configure the `mdcp` tool from `plugins/mdcp-unified/manifest.json`. The runtime provides passive, allowlist-bound HTTPS header inspection, heuristic SQL source review, E2E test-plan generation, and optional delegation to the YouTube runtime. Each host still needs its own connector setup, permissions and secrets. Security testing requires explicit authorization; the website audit is not an active penetration tester. YouTube upload/edit/render features require their configured API, media and cloud-worker services.
