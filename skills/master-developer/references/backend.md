# backend.md

- Layers: route handler (parse, auth) -> service (rules) -> data access (queries). No SQL in routes.
- Validate input with Zod at the edge. No `any`; use `unknown` then parse.
- Prisma: `select` only needed fields, paginate every list, index foreign keys and search columns, wrap multi-step writes in `$transaction`.
- Make retried writes idempotent (idempotency key or unique constraint).
- Cache with Redis only with an explicit TTL and a clear invalidation point.
- Structured logger, no `console.log` of secrets, tokens or personal data.
- Timeouts on every outbound call. Graceful shutdown for workers.
