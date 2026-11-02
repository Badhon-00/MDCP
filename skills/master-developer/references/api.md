# api.md

- Route handlers or tRPC; pick one per project.
- Input: `schema.safeParse`; on failure return 400 with field errors.
- Response shape: `{ success, data?, error?: { code, message } }`.
- Status codes: 200, 201, 400, 401, 403, 404, 409, 429, 500. Return 403 vs 404 deliberately so you do not reveal what exists.
- Auth and object-level ownership check on every route that touches user data.
- Rate-limit public and auth routes; return `Retry-After` on 429.
- Version under `/api/v1/` once external clients exist.
- Never return raw DB rows; return DTOs.
