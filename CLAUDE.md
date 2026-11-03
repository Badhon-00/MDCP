# MDCP — Claude-compatible workspace instructions

You are working in MDCP (Master Developer Claude Plugin).

## Repository rules

1. Inspect existing implementation and tests before editing.
2. Preserve existing architecture and third-party licenses. Do not claim bundled third-party code is exclusively owned by this repository's author.
3. Make the smallest complete change. Do not invent implemented feature counts, agents, routes, or integrations.
4. Use filesystem and Git tools only when the host actually provides them. Instructions cannot grant tools, background execution, MCP access, or GitHub permissions.
5. Never commit API keys, tokens, private checkpoints, or user secrets.
6. Run relevant tests, validation, lint, and type checks. Report actual commands and outcomes; never claim zero warnings without running them.
7. Do not push, publish, merge, delete, or change repository visibility unless the user explicitly authorizes that action.

## Provider fallback

MDCP supports provider routing for compatible API clients through configured gateways such as OmniRoute. The optional `free-llm-switcher.js` module is for a separately running Node.js application that has provider API keys.

Important boundaries:

- Claude.ai usage limits are enforced by Anthropic. Prompts, Artifacts, MCP memory, or this repository cannot bypass those limits.
- Claude.ai does not automatically execute external API calls when its hosted model limit is reached.
- Fallback works only when an independent client/agent calls the configured provider API.
- Free provider tiers are quota-limited, may require API keys, and can change model availability or terms.
- A successful fallback response is not proof that a coding task was implemented. The caller must apply changes, run tests, inspect diffs, and save checkpoints.
- Checkpoints are local application files, not Claude Memory or automatic GitHub commits.

## Task workflow

1. Inspect relevant files and current Git state.
2. Prepare a short plan.
3. Implement a focused patch.
4. Run targeted tests and repository validation.
5. Inspect the final diff for regressions and secrets.
6. Report changed files, test results, limitations, and manual setup.

Do not promise infinite loops, uninterrupted execution, autonomous background work, or automatic model switching inside Claude.ai.
