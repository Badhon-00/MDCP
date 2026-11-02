# omni-creator.md: building a new thing

Defaults when the request is short ("build a portfolio / site / app / bot"):

- Portfolio or site: one page, real content from the owner's projects, own design tokens, responsive, accessible, motion respects reduced-motion.
- Web app: Next.js (App Router) + TypeScript strict + Zod + Prisma/PostgreSQL; auth and rate limiting from day one.
- Bot (WhatsApp, Instagram, Messenger): follow the project's existing handler/command structure; keep credentials in config files that are git-ignored; add per-user cooldowns.
- Use only the owner's own facts. Never invent projects, jobs or numbers; mark placeholders clearly.
- Deliver something that runs, then list shortcuts and what is not done.
