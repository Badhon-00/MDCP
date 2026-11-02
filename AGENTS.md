# MDCP Agent Instructions

Use these instructions for Codex and other non-Claude agents. Preserve all existing Claude-specific files, manifests, skills, workflows, and documentation unless explicitly asked to change them. Inspect before editing. Never overwrite user work or secrets. Keep third-party skill licenses and notices intact. Add portable skills under `.agents/skills/`, ChatGPT material under `.gpt/`, and Codex material under `.codex/`. Add tests for behavior changes. Run `python3 scripts/validate.py` when possible and report exact results. Never claim unrun tests passed. Require explicit approval for destructive operations, production deployments, database writes, permission changes, and active security scans.


## LLM routing

For local and free-tier model routing, read `integrations/omniroute/README.md` and the `omniroute-free-llm-routing` skill. Use OmniRoute only when installed and configured. Never promise unlimited hosted inference, bypass provider quotas, or expose gateway/API keys. Claude Code and Codex CLI can use the upstream OmniRoute launch/configuration flow; Claude.ai and ChatGPT web chat cannot be transparently redirected by repository instructions alone.
