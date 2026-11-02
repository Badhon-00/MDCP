# MDCP — Master Developer Claude Plugin

[![Validate](https://github.com/Badhon-00/MDCP/actions/workflows/validate.yml/badge.svg)](https://github.com/Badhon-00/MDCP/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A modular developer toolkit for coding agents.** MDCP combines curated skills, platform-specific instruction adapters, optional MCP connector guidance, and a local project-memory utility designed to reduce repeated context preparation.

> **V2000 architecture track:** a roadmap/version label, not a claim that 2,000 files, agents, plugins, or integrations are implemented. Features are counted only when implemented and validated.

## Existing skill library

MDCP currently includes **82 curated skills** across core development, security, backend/data, frontend, design, Three.js, workflows, clean-room app reconstruction, and skill/plugin/MCP authoring. See the [skill catalog](skills/) and [third-party notices](THIRD_PARTY_NOTICES.md) for source and license details.

## Platform coverage

| Platform | Included guidance | Important boundary |
|---|---|---|
| Claude Code | Existing marketplace plugin and Claude adapter | Native plugin/skill installation |
| OpenAI Codex | `AGENTS.md` and Codex adapter | Host must support the documented instruction discovery |
| ChatGPT | Project / Custom GPT setup guide | Not an automatically installed ChatGPT plugin |
| Gemini | Portable `GEMINI.md` adapter | Add to a supported workspace manually |
| Cursor | `.cursorrules` starter | Follow current Cursor rules support |
| Windsurf | `.windsurfrules` starter | Follow current Windsurf rules support |
| Other agents | Portable Markdown context | Adapt to the host's own format |

See [platform adapters](adapters/README.md) and the [universal architecture](docs/UNIVERSAL_AI_ARCHITECTURE.md).

## Token efficiency and project memory

LLM inference is not free and MDCP cannot guarantee zero token consumption or a fixed 80–90% reduction. It helps avoid unnecessary repeated reads by creating a small, bounded project-context pack and storing explicit decisions locally.

### Quick start

```bash
# Build a compact context pack (stdout)
python3 tools/mdcp_memory.py pack --root . --max-chars 12000

# Save a project decision locally
python3 tools/mdcp_memory.py remember "API versioning" "Use /v1 routes for public endpoints."

# Search saved decisions
python3 tools/mdcp_memory.py search "API"

# Export or delete a memory
python3 tools/mdcp_memory.py export
python3 tools/mdcp_memory.py forget 1
```

The database lives in `.mdcp/memory.sqlite3` and is ignored by Git by default. The utility does **not** write to ChatGPT Memory, Claude memory, Codex session memory, or any provider-private storage. Feed the generated context pack to the agent or configure the host to load it. Read [Token Efficiency & Memory](docs/TOKEN_EFFICIENCY_AND_MEMORY.md).

## Free and local LLM routing (OmniRoute + Ollama)

MDCP includes an integration pack for [OmniRoute](https://github.com/akoeraste/omniroute), a separately maintained open-source AI gateway. It provides one local OpenAI-compatible endpoint, provider/model routing, and fallback according to the providers and accounts you configure. MDCP does not vendor or claim ownership of OmniRoute.

- **Local/private:** Ollama serves models on your own machine. No hosted API quota, but inference is limited by your hardware, memory and electricity.
- **Free hosted tiers:** connect eligible providers such as Gemini API, Groq, Cerebras, Cloudflare Workers AI, NVIDIA NIM, Hugging Face or OpenRouter free models where currently offered. Each provider controls its own quotas, regions, eligibility, model access and terms.
- **Routing:** OmniRoute can route compatible coding CLIs through one local gateway and use configured fallback candidates when supported.
- **Claude Code + Codex CLI:** use OmniRoute's documented CLI launch/configuration commands. Do not replace your existing provider credentials or config blindly.
- **Claude.ai and ChatGPT web apps:** skills/instructions can be reused there, but those hosted chat interfaces do not become OmniRoute clients merely by installing this repository. A supported API/action or compatible client is required.

### Quick start

```bash
# Install the upstream gateway (review its docs and release first)
npm install -g omniroute
omniroute

# Open http://localhost:20128, connect providers you are eligible to use,
# and copy the gateway API key from Dashboard -> Endpoints.

# Launch compatible coding CLIs through the gateway
omniroute run claude --model auto/coding
omniroute run codex --model auto/coding

# Or use the upstream guided configuration
omniroute configure claude
omniroute configure codex

# Optional: connect the local Ollama service in OmniRoute's Providers UI.
# Install Ollama separately, start it, and pull a model that fits your hardware.
ollama serve
ollama pull qwen2.5-coder:7b
```

See [OmniRoute + Ollama integration guide](integrations/omniroute/README.md), [free provider notes](integrations/omniroute/FREE_PROVIDERS.md), and the reusable [OmniRoute routing skill](skills/omniroute-free-llm-routing/SKILL.md).

**No unlimited hosted usage promise:** free tiers are rate-limited and can change or disappear. MDCP does not bypass quotas, rotate accounts to evade limits, or guarantee a zero-cost route. For genuinely uncapped local usage, run Ollama locally subject to hardware constraints.

## Connectors and MCP

MDCP documents optional connector categories including source control, documentation, databases, design, browser testing, deployment, observability and team workflows. Connectors must be installed and authenticated in the host environment. Availability varies by provider and account.

Start with [connector safety and setup](connectors/README.md). Never commit API keys or tokens. Use least-privilege credentials and require approval for destructive or externally visible actions.

## Repository map

```text
MDCP/
├── skills/                 # Curated task-specific skill library
├── plugins/                # Plugin resources
├── mcp/                    # Existing MCP setup notes
├── adapters/               # Claude, Codex, ChatGPT, Gemini, Cursor, Windsurf
├── connectors/             # Connector guidance and safe example config
├── docs/                   # Architecture and memory documentation
├── tools/                  # Local context/memory utilities
├── tests/                  # Utility tests
├── MDCP_CONTEXT.md         # Short portable project brief
├── AGENTS.md               # Repository agent instructions
└── README.md
```

## Quality and security

- Curated skills retain their upstream licenses and attribution.
- Validate repository metadata with `python3 scripts/validate.py`.
- Run memory utility tests with `python3 -m unittest tests/test_mdcp_memory.py`.
- Third-party skills and MCP servers are not automatically security-audited. Review before use.
- Rules guide agents; tests, type checkers, scanners and human review determine whether changes are correct.

## Roadmap

- [x] Portable project context and agent adapters
- [x] Local SQLite decision memory and bounded context packer
- [x] Connector setup and least-privilege guidance
- [ ] Verified integration tests for each host version
- [ ] Optional memory indexing and semantic retrieval
- [ ] Expanded language-specific skills based on tested demand
- [ ] CI coverage for all utilities and supported runtimes

## Contributing

Issues and pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), run the validator, and include tests for behavior changes. Security reports: [SECURITY.md](SECURITY.md).

## License

MIT for MDCP's original files. Bundled skills retain their own licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [licenses/](licenses/).
