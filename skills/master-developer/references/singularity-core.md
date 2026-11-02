# singularity-core.md: how these files are used

- `CLAUDE.md` loads automatically in Claude Code. The other files do not; open one when the task matches (see master-manifest.md).
- Rules guide behavior; they are not enforcement. Enforcement is CI: build, typecheck, tests, scanners.
- Rules in `CLAUDE.md` win over any other file in this folder.
- If a rule here is wrong for a project, edit the file. Keep each rule short enough to be followed.
