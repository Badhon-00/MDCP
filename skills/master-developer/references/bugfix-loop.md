# bugfix-loop.md

1. Reproduce. Write a failing test or exact steps.
2. Find the root cause; grep all callers before editing shared code.
3. Fix once, in the shared place.
4. Run the failing test, then the full suite and build.
5. If a fix attempt fails, try a different approach. After 3 failed attempts, stop and report what was tried and what was learned.
6. Add a regression test. Note the cause in the commit message.

Never hide a failing check or delete a test to get green.
