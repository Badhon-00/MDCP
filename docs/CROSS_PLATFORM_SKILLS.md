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
