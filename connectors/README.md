# Connectors and MCP Servers

MDCP provides guidance and example configuration for optional connectors. A connector is an external capability that must be installed, authenticated and authorized in the host environment.

## Connector categories

- Source control: GitHub, GitLab and other supported Git providers.
- Documentation: Context7 or official documentation retrieval.
- Database: Supabase, PostgreSQL and supported database tools.
- Design: Figma and design-system resources.
- Browser testing: Playwright or other approved browser automation.
- Delivery: Vercel, Cloudflare and other deployment providers.
- Observability: Sentry, PostHog and supported monitoring tools.
- Team workflow: Linear, Notion, Slack and other services where an official or trusted connector exists.

The names above are examples of integration targets, not a statement that every server is bundled, verified, free, or available on every AI platform.

## Safe setup checklist

1. Confirm the connector's official publisher and repository.
2. Read its permissions and tool descriptions.
3. Pin a reviewed version where practical; avoid blindly executing `@latest` in production.
4. Use least-privilege credentials and host secret storage.
5. Test read-only access before enabling writes.
6. Require explicit approval for destructive or externally visible actions.
7. Remove unused connectors and rotate exposed credentials.

See `mcp.example.json` for a deliberately minimal placeholder. Replace commands only with verified official package names and arguments for your host.
