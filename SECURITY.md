# Security policy

## What counts
- A skill or script in this repo that could harm a user: running code unprompted, sending data out, writing secrets, weakening security advice.
- A security rule that is wrong or dangerous.
- A credential committed by mistake.

## Report privately
Use GitHub's "Report a vulnerability" (Security tab of this repository). Please do not open a public issue for something exploitable. Include the file, what happens, and how to reproduce it.

You can expect a first reply within a week. This is a volunteer project; there is no bounty.

## Scope notes
- Third-party skills are included as published upstream and are not audited here. For a problem in the skill itself, also report it to its source (see THIRD_PARTY_NOTICES.md).
- `scripts/token-meter.py` only reads local transcript files and makes no network calls.
- No skill here should need your API keys. If one asks for a secret, treat that as a bug and report it.
