# OmniRoute + Ollama + Free LLM Integration

MDCP uses [OmniRoute](https://github.com/akoeraste/omniroute) as an optional external gateway rather than reimplementing or vendoring it. OmniRoute's release, provider catalog, supported CLIs and configuration commands are maintained upstream. Check upstream documentation before each deployment.

## Architecture

```text
Claude Code CLI ─┐
                 ├── OmniRoute local gateway (127.0.0.1:20128)
Codex CLI ───────┘          │
                            ├── Ollama (local model; hardware-bound)
                            ├── Gemini API (free tier if eligible)
                            ├── Groq / Cerebras (free developer tiers if eligible)
                            ├── Cloudflare Workers AI / NVIDIA NIM
                            ├── Hugging Face / OpenRouter :free
                            └── Other providers explicitly connected by user

Claude.ai / ChatGPT web ── reusable MDCP skills & instructions
                           (not transparently routed through localhost)
```

## Install

Requirements: supported Node.js/npm version for the current OmniRoute release. Review the official release notes and security guidance first.

```bash
npm install -g omniroute
omniroute
```

Then open `http://localhost:20128`. Complete the first-run setup, connect only providers you are eligible to use, and copy the gateway key from Dashboard → Endpoints. Keep it private.

## Claude Code and Codex

OmniRoute documents dedicated CLI launch/configuration commands. These are preferred because they handle each CLI's environment/model mapping:

```bash
omniroute run claude --model auto/coding
omniroute run codex --model auto/coding

# Interactive native configuration (review changes before accepting)
omniroute configure claude
omniroute configure codex
```

Run `omniroute --help` and check the upstream CLI guide if command names differ in your installed release. Start with a non-sensitive test prompt and confirm which provider/model served it in the gateway dashboard.

## Ollama

Install Ollama separately from https://ollama.com. Start the service and download a model that fits your hardware:

```bash
ollama serve
ollama pull qwen2.5-coder:7b
ollama list
```

In OmniRoute, add/enable the local Ollama provider and confirm the model is listed. Model tags, quality and hardware needs vary; use the model catalog and license before downloading. On Android/Termux, large models may not fit device memory.

## Free hosted model sources

The OmniRoute provider catalog may include Gemini API, Groq, Cerebras, Cloudflare Workers AI, NVIDIA NIM, Hugging Face, OpenRouter free models and other offers. Check the live catalog for current model IDs and eligibility. A free tier can have RPM/TPM/day caps, region restrictions, verification requirements, model changes or service interruptions.

**Do not interpret “free” as “unlimited.”** No quota bypass, account farming, identity rotation or credential sharing. Fallback must respect each provider's terms and cooldowns. Local Ollama avoids hosted API billing but still consumes hardware, electricity and time.

## ChatGPT and Claude web apps

- Claude Code CLI: can be launched/configured through OmniRoute as documented upstream.
- Codex CLI: can be launched/configured through OmniRoute as documented upstream.
- Claude.ai web and ChatGPT web: cannot be redirected to a localhost gateway by adding skills or README instructions. Use their native project/custom-GPT instructions, or a supported public HTTPS API/action/connector when available. Do not expose a local gateway publicly without authentication, TLS, network restrictions and review.

## MCP

OmniRoute documents an MCP server. For Claude Code, upstream currently documents a local HTTP MCP endpoint at `http://localhost:20128/api/mcp/stream`. Confirm the exact command and transport in the installed release's MCP guide before adding it. Only connect MCP if you need gateway-management tools; basic model routing does not require MCP.

## Recommended operating profile

| Task | Preferred route |
|---|---|
| Small edits, boilerplate, local code explanation | Ollama local model |
| Routine coding when eligible | Hosted free-tier coding model |
| Complex debugging or architecture | Best available connected model, subject to its terms |
| Sensitive code / private repository | Local Ollama or an approved private provider |
| Final verification | Deterministic tests, linters, type checks and human review |

## Security checklist

- Bind the gateway to loopback unless remote access is intentionally secured.
- Use the gateway's authentication key; never publish it.
- Never commit provider keys, tokens, OAuth sessions or gateway database files.
- Review provider terms and data-retention policies before sending private source code.
- Use least privilege and remove providers you no longer need.
- Avoid enabling untrusted MCP servers or plugins.
- Back up existing Claude/Codex configuration before using an automated configurator.

## Official references

- OmniRoute repository and docs: https://github.com/akoeraste/omniroute
- OmniRoute documentation: https://omni.moju-ai.com/docs
- Ollama: https://ollama.com
