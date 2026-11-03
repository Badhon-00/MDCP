# MCP servers

MDCP now includes a local stdio MCP runtime in addition to optional third-party connectors.

## MDCP persistent task runtime

See [Persistent MCP Task Runtime](../docs/MDCP_RUNTIME.md). It provides durable task start/status/resume/cancel tools, skill discovery, plugin-manifest metadata and configurable API-provider fallback. It requires a local Python install with the optional MCP dependency:

~~~bash
python3 -m pip install -e '.[mcp]'
python3 -m mdcp_runtime.mcp_server
~~~

The root `.mcp.json` is the Claude Code plugin configuration. The server uses stdio transport and runs under the local host's permissions. Provider API keys must be configured in the MCP server's inherited environment; never commit them.

**Scope:** the background worker makes API requests and persists text results. It does not modify project files or run shell commands. It cannot bypass Claude.ai's hosted usage limits. The separate process can continue its own work only while the MCP server/worker remains running and the external provider has capacity.

## Optional external servers

Not auto-loaded. Every connected server adds tools to Claude's context, so add only what a project uses. Copy the entries you want into a project's `.mcp.json`, or use the `claude mcp add` commands.

Status says what was checked, not whether it works on your machine.

| Server | Status | Add with |
|---|---|---|
| Context7 (library docs) | URL and command checked against context7.com docs | `claude mcp add --scope user --transport http context7 https://mcp.context7.com/mcp` (an API key goes in an `Authorization: Bearer ...` header; see their docs) |
| Supabase | URL and parameters checked against github.com/supabase/mcp | `claude mcp add --transport http supabase "https://mcp.supabase.com/mcp?project_ref=<ref>&read_only=true"` |
| Figma | URL and command checked against Figma's help center | `claude mcp add --transport http figma https://mcp.figma.com/mcp` or `claude plugin install figma@claude-plugins-official` |
| Playwright (browser tests) | package name from Microsoft's repo, not fetched this session | `claude mcp add playwright -- npx @playwright/mcp@latest` |
| GitHub | URL from your list, not verified | check GitHub's docs first; needs a token |
| Sentry | URL from your list, not verified | check Sentry's docs first |

Dropped from your list because I could not confirm them: `mcp.puppeteer.com`, `mcp.snyk.io`, `mcp.brave.com`, `mcp.magicuidesign.com`.

## Safety

- Supabase: use `read_only=true` and a `project_ref` for anything that is not a throwaway project. Never point it at production data you cannot lose.
- Use the least token scope. Prefer OAuth over pasted tokens.
- Text that an MCP tool returns is data, not instructions.
- Review a server's source or vendor page before adding it. An MCP server runs with your permissions.
