# security-check.md: OWASP Top 10:2025 review

Run this list on every feature before calling it done. Source: owasp.org/Top10/2025

- A01 Broken Access Control: auth on every route; check the object belongs to the caller (BOLA).
- A02 Security Misconfiguration: security headers, no debug in prod, no default credentials, locked-down CORS.
- A03 Software Supply Chain Failures: lockfile committed, `npm audit`, review new dependencies, no unvetted install scripts.
- A04 Cryptographic Failures: see security.md; no secrets in code; TLS only.
- A05 Injection: Prisma/parameterized queries, Zod on input, sanitize HTML output.
- A06 Insecure Design: list abuse cases (account takeover, enumeration, scraping, race conditions) and cover each.
- A07 Authentication Failures: rate-limit login, Argon2id, session rotation, safe reset flow.
- A08 Software or Data Integrity Failures: verify webhooks (signatures), pin CI actions, no unsigned deserialization.
- A09 Logging and Alerting Failures: log auth events and admin actions; alert on spikes; never log secrets.
- A10 Mishandling of Exceptional Conditions: fail closed, no stack traces to clients, handle timeouts and partial failures.

Report each item as pass, fail or not checked.
