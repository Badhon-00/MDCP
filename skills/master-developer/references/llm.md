# llm.md: reading and context

- Read a file once per task; do not re-read unchanged files.
- Batch related reads in one step.
- Grep for the symbol before opening a large file.
- At about 70% context, write a summary to NOTES.md (goal, decisions, files touched, next step) and continue from it.
- Prefer official docs over memory for library APIs; check the installed version in package.json first.
