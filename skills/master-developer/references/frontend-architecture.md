# frontend-architecture.md

```
app/            routes, layouts, route handlers
components/     ui/ (primitives), features/<name>/, layout/
lib/            utils, env.ts (validated env), auth, rate-limit
data/           server-only data access layer + DTOs
hooks/
prisma/         schema.prisma, migrations/
```

- One feature = one folder under `components/features/`.
- Server Components by default; add `'use client'` only for state, effects or browser APIs.
- Client Components receive minimal props, never whole DB rows.
- Validate env once in `lib/env.ts` with Zod.
