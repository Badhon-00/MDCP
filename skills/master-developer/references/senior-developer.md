# senior-developer.md: before coding

1. What exactly breaks if this is wrong? Data loss and exposure come first.
2. Who calls this code, and what do their tests expect?
3. What happens with empty input, huge input, a hostile user, a down database, two requests at once?
4. Is there already a helper, component or pattern for this in the repo? Use it.
5. What is the smallest change that fully solves it?

Avoid: `any`, `eval`, `innerHTML` without sanitizing, hardcoded secrets, copy-pasted code you do not understand, dependencies added for a few lines.
