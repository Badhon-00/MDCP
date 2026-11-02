# MDCP Project Context

> Keep this file short. It is the portable, human-reviewed project brief loaded before task-specific skills.

## Identity
- Project: MDCP — Master Developer Claude Plugin / Universal developer workflow toolkit.
- Maintainer: Badhon-00.
- Repository: https://github.com/Badhon-00/MDCP
- Primary goal: reusable coding skills, platform adapters, optional connectors, and compact project memory.

## Working principles
- Inspect the existing implementation before editing; preserve working behavior and licenses.
- Load only the skills and files relevant to the current task.
- Prefer small, testable changes over giant generated file counts.
- Use current official documentation when versions or APIs may have changed.
- Never invent test results, integrations, platform support, performance numbers or security guarantees.
- Run relevant validation after changes and report what was and was not tested.
- Keep credentials out of Git and generated context packs.

## Platform notes
- Claude Code: use the existing marketplace plugin and Claude-specific instructions.
- Codex: follow repository `AGENTS.md` and Codex-specific configuration.
- ChatGPT: use project/custom GPT instructions and connectors only where the account and host support them.
- Gemini, Cursor, Windsurf and other agents: use their documented native instruction surfaces or portable Markdown.
- Shared Markdown guidance does not make a provider connector or plugin automatically available.

## Context entry points
- Architecture: `docs/UNIVERSAL_AI_ARCHITECTURE.md`
- Memory and token efficiency: `docs/TOKEN_EFFICIENCY_AND_MEMORY.md`
- Connector guidance: `connectors/README.md`
- Platform adapters: `adapters/README.md`
