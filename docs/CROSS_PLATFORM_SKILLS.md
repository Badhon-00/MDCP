# Cross-Platform Skill and Plugin Distribution

## One source of truth

MDCP keeps canonical skill playbooks under `skills/<skill-name>/SKILL.md`. Platform-specific adapters point to or package these playbooks without pretending that all hosts share one plugin format.

| Platform | How to use MDCP |
|---|---|
| Claude Code | Install the MDCP marketplace plugin; skills are discovered in the plugin's skill directory |
| Claude.ai | Upload/import selected skill Markdown or files into a Project/custom workflow that supports knowledge/instructions |
| Codex CLI | Use repository `AGENTS.md`; portable skills are under `.agents/skills/` |
| ChatGPT | Import selected skill files into a Project or custom GPT knowledge/instructions where supported |
| ChatGPT connectors / GPT Actions | Configure separately using supported connector/action setup and permissions |
| OmniRoute | Configure as a model gateway for compatible API/CLI clients; not a plugin loader |

## Distribution bundle

Build a portable archive:

```bash
python scripts/package_skills.py --output dist/mdcp-skills.zip
```

The archive contains canonical skill folders and this platform guide. Review upstream licenses in `THIRD_PARTY_NOTICES.md` before redistribution.

## What is not automatic

- A Claude Code plugin is not directly installable as a ChatGPT plugin.
- ChatGPT Projects and Custom GPTs have their own import, knowledge and connector behavior.
- Claude.ai web sessions are not Claude Code terminal sessions.
- Codex CLI and ChatGPT web are different execution surfaces.
- A skill cannot grant shell access, repository permissions, MCP connections, API keys or background execution.
- OmniRoute cannot redirect the hosted inference of Claude.ai or ChatGPT web just because a skill is uploaded.

Always use the platform's current documented import mechanism and verify that the skill is actually available in a test conversation.
