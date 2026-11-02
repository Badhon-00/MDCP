# Contributing

Thanks for helping. Small, focused changes are easiest to review.

## Good contributions
- Fix an outdated command, URL or version in a rule file or `mcp/`.
- Report or fix a wrong, unsafe or misleading instruction in a skill.
- Add a skill that is clearly useful, has an open license, and does not duplicate one already here.
- Improve the validator, CI or docs.

## Adding a third-party skill
1. The source must have an open license (MIT, Apache-2.0, BSD). No license means no.
2. Copy the skill folder unmodified (note any change you had to make).
3. Read it. Do not add skills that install hooks, start servers, fetch and run remote code, or send data elsewhere without clear, documented consent.
4. Add a row to `THIRD_PARTY_NOTICES.md` (source, license, exact skill names, anything changed or left out) and the license text to `licenses/`.
5. Add it to the README table and to `skills/master-developer/SKILL.md`.
6. Run `python3 scripts/validate.py`.

## Adding an original skill
`skills/<name>/SKILL.md` with frontmatter `name` (same as the folder) and a specific `description` that says when to use it. Keep SKILL.md short; put detail in files next to it.

## Rule files
Files in `skills/master-developer/references/` should be short, checkable and verified. Do not write guarantees ("100% secure"). Link the primary source for anything that changes over time.

## Pull requests
- One topic per PR. Say what changed and what you tested.
- CI must pass.
- By contributing you agree your work is released under this repository's license, or the original license for bundled third-party skills.

Be respectful. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
