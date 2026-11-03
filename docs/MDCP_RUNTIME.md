# MDCP Persistent MCP Task Runtime

The runtime adds a local MCP server and durable background task queue for Claude Code and other MCP hosts that can launch a local stdio server.

## Implemented tools

- `mdcp_task_start`: stores a task in SQLite and queues it for an independent worker thread.
- `mdcp_task_status`: reads persisted state and model output.
- `mdcp_task_resume`: requeues failed or cancelled tasks.
- `mdcp_task_cancel`: cancels queued work or requests cancellation after an in-flight provider request returns.
- `mdcp_skill_search`: discovers canonical `skills/*/SKILL.md` entries.
- `mdcp_plugin_manifest`: exposes Claude plugin manifest metadata.
- Task start automatically attaches up to three relevant skills.
- Provider routing supports OpenAI-compatible APIs, missing-key skips, HTTPS validation, per-provider cooldowns and fallback after rate-limit/server/network failures.
- SQLite persists tasks across server restarts; interrupted running tasks are recovered as queued.

**Important boundary:** the worker makes API calls and returns text. It does not edit files, execute shell commands, commit, push, deploy, or merge code. It is not a full Claude Code replacement or an infinite autonomous coding loop. A separately approved workspace executor is required for file-changing agent workflows.

## Install

From a local MDCP clone:

~~~bash
python3 -m pip install -e '.[mcp]'
python3 -m mdcp_runtime.mcp_server
~~~

The base project supports Python 3.10+. The MCP extra is pinned to the v1 maintenance line for the FastMCP API used here. The server uses stdio transport; launch it through an MCP host and do not expose it directly to the public internet.

## Provider configuration

Set at least one provider key in the environment inherited by the MCP server:

~~~bash
export GROQ_API_KEY='...'
export OPENROUTER_API_KEY='...'
export TOGETHER_API_KEY='...'
~~~

Optional model overrides: `GROQ_MODEL`, `OPENROUTER_MODEL`, `TOGETHER_MODEL`. Default model IDs are examples and may change or become unavailable. Check each provider's current model catalog, quotas, pricing and terms. Free tiers are not guaranteed or unlimited. API keys are not stored in the repository or task database.

For custom OpenAI-compatible providers, define `MDCP_PROVIDERS` as a JSON array. Each entry requires `name`, HTTPS `base_url`, `model`, and `api_key_env`:

~~~bash
export MDCP_PROVIDERS='[
  {"name":"primary","base_url":"https://api.example.com/v1","model":"model-id","api_key_env":"PRIMARY_API_KEY"},
  {"name":"backup","base_url":"https://backup.example.com/v1","model":"backup-model","api_key_env":"BACKUP_API_KEY"}
]'
~~~

## Claude Code integration

The root `.mcp.json` registers the stdio server. Install the optional dependency once in the MDCP checkout, then enable the MDCP plugin. The server inherits provider environment variables from the host process. If the host cannot resolve `CLAUDE_PLUGIN_ROOT`, configure `PYTHONPATH` and `MDCP_REPO_ROOT` to the absolute checkout path in host MCP settings.

Other MCP hosts can use the same stdio command and environment. Claude.ai web plugin/connector availability depends on product and account support; a repository manifest cannot grant a remote host local filesystem or process access.

## Persistence and privacy

- Default state directory: `~/.mdcp`; override with `MDCP_STATE_DIR`.
- Database: `tasks.sqlite3` using SQLite WAL mode.
- The runtime attempts to set the state directory to mode `0700` and the database to `0600`.
- Task/context inputs have size limits and common KEY=value / Bearer-token patterns are redacted before persistence. Do not send secrets or private data to external model providers.
- Task context and provider responses are stored locally. Protect the state directory as sensitive data.
- Tool output and skill content are untrusted input. Review skill instructions and provider output before acting on them.

## Verification

~~~bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q mdcp_runtime tests
python3 scripts/validate.py
python3 scripts/skill_report.py --check
~~~

Tests use fake providers and do not incur API charges. Live provider smoke tests require valid API keys and may incur usage costs.
