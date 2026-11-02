# auto-installer.md: tools to install

Run only what the project needs. Check each package's page before installing.

```bash
# app dependencies
npm i zod argon2 isomorphic-dompurify server-only
npm i -D vitest @playwright/test eslint-plugin-security @next/bundle-analyzer

# scanners
npm audit --omit=dev
npx gitleaks detect          # or: brew install gitleaks
pipx install semgrep         # then: semgrep --config auto
```

Never run install scripts from packages you have not reviewed.
