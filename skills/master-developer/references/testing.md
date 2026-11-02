# testing.md

- Unit (Vitest): pure logic, Zod schemas, crypto helpers, permission rules.
- Integration: API routes with a test database; cover 401, 403, 400, 429 and the happy path.
- E2E (Playwright): sign-in, the main user flow, one mobile viewport.
- Security tests: access another user's object, send malformed and oversized input, replay a token.
- Accessibility: axe checks plus a keyboard-only pass.
- A bug fix ships with a test that failed before the fix.
- Report which tests ran. If something was not run, say so.
