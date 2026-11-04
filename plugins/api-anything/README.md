# API Anything — optional MCP plugin

**Status:** opt-in local MCP integration; not enabled by default.

## Install and connect

Requirements: Node.js 22.13.0 or newer.

Recommended upstream setup:

```bash
npx -y api-anything setup
```

Or install globally and add the STDIO server to a compatible MCP client:

```bash
npm install -g api-anything
api-anything mcp --print-config
```

The MDCP manifest in this folder records the intended server command:

- command: `npx`
- args: `-y api-anything mcp`
- transport: local STDIO
- enabled by default: no

Use the host client's documented MCP configuration format. Do not overwrite existing MCP entries; merge this server entry and back up the configuration first.

## What it does

The server can search a shared operation catalog, inspect available operations, call an operation, and learn a missing operation from browser traffic. See the upstream [README](https://github.com/goodnight000/api-anything) and [quick start](https://github.com/goodnight000/api-anything/blob/main/docs/QUICKSTART.md).

## Cloud AI compatibility

This package's default integration is a local STDIO process. It is **not** a hosted HTTP MCP endpoint. A cloud-hosted AI client cannot launch a process on the user's device. To use it from a cloud client, deploy a separately secured remote MCP bridge on infrastructure controlled by the user, with explicit per-user isolation for browser sessions and credentials. MDCP does not provision that bridge.

## Security

- Never commit cookies, tokens, browser profiles, or API keys.
- Keep authenticated sessions local to the user.
- Do not share operations learned from private sessions without explicit consent.
- Require explicit user intent for every write operation.
- Respect target-site terms, access controls, rate limits, and privacy rules.
- Review upstream releases and dependencies before upgrading.

Upstream: https://github.com/goodnight000/api-anything  
Owner mirror: https://github.com/Badhon-00/api-anything  
License: MIT; retain upstream copyright notice when redistributing upstream code.
