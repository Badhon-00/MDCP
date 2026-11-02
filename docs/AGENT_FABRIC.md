# MDCP Universal Agent Fabric

## Purpose

The agent fabric is a local orchestration CLI. It can discover public GitHub repositories concurrently and dispatch a bounded set of specialist analysis prompts to a configured OpenAI-compatible chat-completions endpoint (including an OmniRoute endpoint if configured).

It does not create 64 independent Claude.ai/ChatGPT/Codex hosted sessions by itself. Each model call is a normal API request to the endpoint configured by the operator. Actual concurrency is limited by provider quotas, model availability, network, rate limits and local resources.

## Safety and limits

- Hard maximum concurrency: 64; default: 8.
- Repository discovery uses GitHub's public search API; unauthenticated rate limits apply.
- Analysis reads only text files in the selected local checkout and skips common vendor, VCS, build, cache and secret paths.
- File count, file size, total context and output tokens are bounded.
- No code execution, package installation, writes or auto-fixes occur during analysis.
- API keys are read from environment variables and are never written into reports.
- Repository contents are untrusted input. Prompt injection inside source files must be treated as data, not instructions.
- Model results are suggestions; verify findings manually and with deterministic tools.

## Install

```bash
python -m pip install -e .
mdcp-fabric --help
```

Python 3.10+; runtime uses the standard library only.

## Repository search

```bash
mdcp-fabric search "mcp server" "agent framework" --limit 25 --workers 16
```

Search results include repository metadata, URL, stars, language, and description. This is discovery, not a security or quality endorsement. Review licenses, commit activity, maintainers, releases and source code before adopting external skills/plugins.

## Parallel analysis

Configure an OpenAI-compatible endpoint:

```bash
export MDCP_LLM_BASE_URL="http://localhost:20128/v1"
export MDCP_LLM_API_KEY="your-key"
export MDCP_LLM_MODEL="model-id"
mdcp-fabric analyze . --agents 8 --max-parallel 8
```

Use `--agents 64 --max-parallel 64` only when the endpoint can handle the request rate and context load. The CLI uses a specialist roster and submits selected roles concurrently; it does not claim 64 independent reasoning engines if the provider does not provide them.

## Token-aware context

```bash
mdcp-fabric context . --max-chars 12000 --output .mdcp/context-pack.md
```

The local cache tracks hashes and metadata so unchanged files can be skipped during repeated indexing. Context packs contain bounded excerpts and paths, not a complete semantic representation of the codebase. Rebuild when files change. Model prompt caching is provider-specific and separate from this local cache.

## Outputs

Analysis writes Markdown and JSON reports under `.mdcp/reports/` by default. Reports include role, model identifier, timestamp, findings and source file references. No report should be treated as a verified vulnerability without reproduction.

## Extending

Add specialist definitions in `agents/roles.json`. Keep each role narrow, non-overlapping, and with explicit output schema. Do not create large numbers of near-duplicate agents merely to inflate the count.
