# performance.md

Targets (Core Web Vitals, 75th percentile): LCP <= 2.5s, INP <= 200ms, CLS <= 0.1.

- Measure first (Lighthouse, WebPageTest, real-user data). Do not guess.
- Frontend: `next/image`, `next/font`, dynamic import for heavy components (3D, charts), avoid layout shift, defer third-party scripts.
- Bundle: analyze with `@next/bundle-analyzer`; remove unused dependencies; import only what you use.
- Backend: fix N+1 queries, add indexes for slow queries (check `EXPLAIN`), paginate, cache with TTL.
- 3D: see threejs.md.
