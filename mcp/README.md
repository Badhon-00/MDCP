# MCP servers

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
