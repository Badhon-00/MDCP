# self-heal-engine.md

When a build, type, test or runtime error appears:

1. Read the full error and the failing line.
2. Tier 1: fix syntax, import or type mistakes.
3. Tier 2: check the installed library version against its docs; use the API that version actually has.
4. Tier 3: simplify the approach.
5. After three failed tiers, stop. Report the error, what was tried, and a suggested next step.

Do not hide intermediate failures that change the result or the plan. A failure the user would want to know about is reported.
