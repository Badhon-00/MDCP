# MDCP Upstream AI Repository Audit

**Owner:** Badhon-00  
**Core:** https://github.com/Badhon-00/MDCP  
**Routing:** https://github.com/Badhon-00/OMNIROUTE  
**Audit date:** 2026-11-03

## Scope and safety

This file records candidate repositories visible in the owner's GitHub repository inventory and their README-level purpose. A repository appearing here does **not** mean its code has been copied, installed, security-reviewed, or merged into MDCP. Prefer adapter manifests, documented installation instructions, and pinned upstream references. Vendor code only after reviewing its exact upstream license, notices, dependency tree, security posture, and compatibility.

Do not copy secrets, tokens, account data, generated build output, or private project data into MDCP.

## Candidate repository map

| Owner repository | Observed purpose from README / metadata | MDCP treatment | License / status |
|---|---|---|---|
| [free-claude-code](https://github.com/Badhon-00/free-claude-code) | Claude-compatible local/API gateway and coding client setup | Optional provider/client integration guide; never claim to be official Claude software | README declares AGPL-3.0; review obligations before copying or linking binaries |
| [ECC](https://github.com/Badhon-00/ECC) | Agent harness / coding-agent operating system | Skills and agent workflow adapter candidate | Exact license and upstream revision must be rechecked |
| [replica-skill](https://github.com/Badhon-00/replica-skill) | Claude skills for clean-room app reconstruction and testing | Skill catalog reference; enforce clean-room, trademark, copyright and data boundaries | README describes MIT; verify LICENSE file and attribution |
| [awesome-freellm-apis](https://github.com/Badhon-00/awesome-freellm-apis) | Machine-readable directory of free LLM APIs and provider/model metadata | Provider discovery reference; revalidate quota, region, terms and model availability at use time | License and freshness need explicit verification; do not promise free or unlimited access |
| [awesome-free-llm-apis](https://github.com/Badhon-00/awesome-free-llm-apis) | Curated directory of permanent/free-tier text inference APIs | Secondary provider discovery reference; deduplicate against the previous directory | Verify exact LICENSE and provider claims before reuse |
| [Mobile-Harness](https://github.com/Badhon-00/Mobile-Harness) | Android AI development workspace with coding-agent, terminal and preview workflows | Mobile workflow compatibility reference; no APK redistribution without separate review | README badge declares MIT; verify LICENSE and release provenance |
| [ai-design-skills](https://github.com/Badhon-00/ai-design-skills) | Design skills for Claude Code, Cursor, Codex and other Markdown-rule agents | Import selected skills only after file-level review; preserve author attribution | README supports portable SKILL.md use; verify LICENSE before vendoring |
| [deepseek-harness](https://github.com/Badhon-00/deepseek-harness) | Plugin-oriented AI agent harness, currently described as developer preview | Experimental adapter reference; isolate and label preview compatibility | Review upstream license, safety notice and breaking-change policy |
| [ACW](https://github.com/Badhon-00/ACW) | Awesome Claude Skills catalog | Discovery index; curate individual skills instead of copying the whole catalog | README shows Apache-2.0 badge; verify repository LICENSE and each skill's origin |
| [composio](https://github.com/Badhon-00/composio) | SDK for agent toolkits, authentication, triggers and sandbox integrations | Optional connector adapter; do not bundle credentials or imply hosted access is included | Verify exact LICENSE, package versions and service terms |
| [OMNIROUTE](https://github.com/Badhon-00/OMNIROUTE) | AI gateway / model routing project | Keep as a separately maintained project; MDCP documents supported integration points | Preserve upstream identity, source history and license |

## Integration rules

1. Keep MDCP's own skills and adapters independently authored and maintainable.
2. For upstream skills, record the canonical upstream URL, author, exact commit/tag, file path, license, and required attribution.
3. Do not assume an entire repository shares one license if it contains third-party assets or individually licensed skills.
4. Do not automatically execute downloaded MCP servers, install scripts, package lifecycle hooks, or arbitrary agent tools.
5. Require explicit user configuration for API keys. Store secrets in environment variables or a secret manager; never commit them.
6. Treat provider pricing, free quotas, rate limits, availability, and terms as volatile data.
7. Mark preview/experimental integrations clearly and pin tested versions.
8. Keep Claude.ai, Claude Code, Codex CLI, ChatGPT, Gemini, Cursor and Windsurf instructions in separate adapters. Do not claim one platform's plugin format installs natively on another.
9. Preserve trademark notices and avoid implying endorsement by Anthropic, OpenAI, Google, DeepSeek, or other vendors.
10. Run license, dependency, secret, static-analysis and test checks before any code is vendored.

## Current implementation status

- MDCP already has platform adapters, skills, MCP guidance, OmniRoute integration documentation, and a skills explorer reference in its README.
- This audit adds a review queue and safe integration policy; it does not claim that every candidate has been imported.
- Full file-by-file audit, license verification, pinned upstream commits, and CI validation remain required before marking any candidate as fully integrated.
