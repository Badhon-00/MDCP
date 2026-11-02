# web-analysis-shield.md

Checks for common web attack paths:

- Headers: CSP (nonce-based, avoid `unsafe-inline` for scripts), HSTS, `X-Content-Type-Options: nosniff`, `frame-ancestors`, Referrer-Policy, Permissions-Policy.
- Cookies: httpOnly, Secure, SameSite=Lax or Strict.
- CORS: explicit allowlist, no `*` with credentials.
- SSRF: allowlist hosts, block private and link-local ranges, resolve DNS then check the IP, no redirects to internal hosts.
- Prototype pollution: reject `__proto__`, `constructor`, `prototype` keys; use `Object.create(null)` or Maps for user-keyed data.
- Deserialization: parse JSON only, validate with Zod; never `eval`, `Function` or unsafe YAML loaders.
- JWT: pinned algorithm, verified claims, rotation.
- BOLA: every object lookup includes the owner or tenant in the query.
- Races: unique constraints, transactions, idempotency keys.
- File uploads: check type by content, cap size, store outside the web root, randomize names.
