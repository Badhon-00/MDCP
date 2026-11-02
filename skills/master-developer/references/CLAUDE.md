# CLAUDE.md

Project rules for Badhon-00 (Melissa projects: Next.js, Node/Express, TypeScript, Prisma/PostgreSQL, Redis).

## Working rules
- Add new features in new files/modules. Edit existing working files only when the feature needs it, and keep the diff small.
- Read the code you touch and its callers before editing. Follow the structure the project already has; do not add files the owner did not ask for.
- Ask one short question only when a wrong guess is expensive or irreversible. Otherwise pick the sensible default, say which one, and continue.
- Never report something as built, tested or secure unless it was actually run. State what was not checked.

## Done means
- `npm run build` and `npx tsc --noEmit` pass.
- Tests for new non-trivial logic exist and pass.
- No secrets in code; config goes in `.env` with a `.env.example`.

## Security baseline
- Validate every input at the boundary (Zod). Use Prisma/parameterized queries only.
- Auth and role checks on every protected route. Rate-limit public and auth endpoints.
- Passwords: Argon2id. Sessions/JWT: httpOnly cookies, rotating refresh tokens.
- Secure headers (CSP, HSTS, X-Content-Type-Options, frame protection) set in config.
- Sanitize HTML before rendering. Allowlist URLs for any server-side fetch (SSRF).
- Run `npm audit` and fix high/critical findings.

### Checklist: OWASP Top 10:2025 (owasp.org/Top10/2025)
A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions.
- A03: pin and review dependencies, commit the lockfile, no unvetted install scripts.
- A10: every error path fails closed (deny, not allow) and never leaks stack traces or internals to the client.

### Next.js (nextjs.org/docs/app/guides/data-security)
- Put all DB and `process.env` secret access in one server-only Data Access Layer (`import 'server-only'`). It authorizes, then returns minimal DTOs, never raw rows.
- Treat every Server Action and `route.ts` as a public HTTP endpoint: validate input and re-check auth inside each one.
- Client Component props take only the fields they render. Route params and searchParams are user input.
- Only `NEXT_PUBLIC_` env vars reach the browser; never put secrets there.
- Behind a reverse proxy, set `serverActions.allowedOrigins`. Mutations never happen during render.
- Audit `middleware.ts` and `route.ts` first.

## UI
- Use the existing design tokens and components. Cover loading, empty, error and success states.
- Respect `prefers-reduced-motion`; keep animation at 60fps (transform/opacity, instancing for 3D).

## More rules
Topic files live in `claude-rules/` (index: `claude-rules/master-manifest.md`). Open the one that matches the task; do not load all of them.

## Token use
- Show diffs or changed snippets, not whole files, unless the file is new.
- Read related files in one batch. Do not re-read unchanged files.
