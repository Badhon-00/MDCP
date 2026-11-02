# zero-error-validator.md: gates

Before reporting a change as done, run and report:

```bash
npx tsc --noEmit
npx eslint .
npm test
npm run build
```

- `tsconfig`: `"strict": true`, `"noUncheckedIndexedAccess": true`.
- Warnings that hide real bugs (unused vars, floating promises) are errors.
- If a gate cannot run (missing script, no network), say which one and why.
