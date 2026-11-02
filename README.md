# MDCP: Master Developer Claude.ai Plugin

One plugin: the `master-developer` skill (35 rule files on demand) plus 48 skills from ECC, awesome-claude-skills, replica-skill, Vercel agent-skills and threejs-skills, and two of its own (mdcp-self-check, mdcp-token-meter). See THIRD_PARTY_NOTICES.md.

## Layout
```
.claude-plugin/plugin.json        plugin manifest
.claude-plugin/marketplace.json   lets this repo act as its own marketplace
skills/master-developer/
  SKILL.md                        core rules + which file to open
  references/                     35 topic files (security, API, DB, UI, 3D, testing, deploy, ...)
```

## Install in Claude Code
```
/plugin marketplace add <your-github-user>/MDCP
/plugin install mdcp@mdcp-marketplace
```
Private repo: Claude Code uses your git credentials, so `git` must be able to clone it.

## Use only the skill
Copy `skills/master-developer/` into `~/.claude/skills/` (all projects) or `<project>/.claude/skills/`.

## Project rules
Copy `skills/master-developer/references/CLAUDE.md` to a project's root as `CLAUDE.md` if you want the short rules always loaded.

## Notes
- Rules guide behavior. Build, typecheck, tests and scanners enforce it.
- Verify every MCP URL in `references/mcp.md` against the vendor's docs before use.
- `references/crypto-vault.md` code is untested; add a round-trip test before relying on it.

## Token meter
`python3 scripts/token-meter.py` prints context in use, output tokens and cache counts for the current Claude Code session. `--statusline` gives one line for the status bar. Details: `skills/mdcp-token-meter/SKILL.md`. It reads Claude Code transcripts only, and shows session context, not plan quota.
