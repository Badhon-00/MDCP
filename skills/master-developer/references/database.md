# database.md

- Prisma schema: explicit relations, `@@index` on foreign keys and filter columns, unique constraints for natural keys.
- Migrations: review the SQL, take a backup first, make destructive changes in two steps (stop using, then drop).
- Supabase: RLS enabled on every table in an exposed schema; write a policy per role (own rows, admin, public read) and test each with a non-owner.
- Never expose the service-role key to the browser.
- Secrets live in env or a vault, not in tables or code.
- Enable point-in-time recovery or scheduled backups and test a restore.
- Pool connections (pgBouncer/Prisma Accelerate) for serverless.
