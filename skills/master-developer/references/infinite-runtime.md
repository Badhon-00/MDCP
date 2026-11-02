# infinite-runtime.md: long sessions

- Commit small and often so work survives a dropped session.
- Keep `NOTES.md` current (format in token-compressor.md). A new session, or a different model, can resume from it.
- Keep the repo runnable at every commit: build and tests pass.
- Record the exact commands to build, test and start in NOTES.md.
- Long tasks: list steps first, tick them off, re-read the list after each step.
- Handoff to another tool: give it NOTES.md and `git log -5`; do not paste secrets.
