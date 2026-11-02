# deployment.md: release gate

- [ ] `npm run build`, `tsc --noEmit`, lint, tests pass in CI
- [ ] `npm audit` has no high/critical production issues
- [ ] Env vars documented in `.env.example`; none committed
- [ ] Security headers set (CSP, HSTS, nosniff, frame protection, referrer policy)
- [ ] Rate limiting on public and auth routes
- [ ] Auth and ownership checks on protected routes
- [ ] Database migrations reviewed; backup taken first; rollback plan written
- [ ] Row Level Security on every exposed table (if Supabase)
- [ ] Error tracking and logs working in production
- [ ] Health check endpoint; smoke test after deploy
