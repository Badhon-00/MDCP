# MDCP provider fallback and session continuity

## What this does

This guide describes a provider fallback layer for applications and coding agents that call LLM APIs. It can try configured OpenAI-compatible providers in order when a provider request is temporarily unavailable, rate-limited, or fails with a server/network error. It can persist a local checkpoint so an external runner can resume a task later.

## What this does not do

- It does **not** bypass, extend, or reset Claude.ai subscription/usage limits.
- A Claude.ai browser session or Artifact cannot silently become a Groq/OpenRouter/Together API client.
- It does not provide 67 guaranteed free models, 230 implemented routes, infinite execution, background work, or automatic access to another provider's credentials.
- Free-tier quotas, model identifiers, regions, and eligibility are controlled by each provider and may change.
- A fallback model may produce different quality or behavior. Review and test generated changes before merging.

If Claude.ai itself reaches its usage limit, continue only from a separately running client/agent that you have configured with provider API credentials. Otherwise save the task/checkpoint and resume when Claude.ai is available again.

## Included implementation

`free-llm-switcher.js` is a Node.js CommonJS module that:
- uses provider API keys supplied through environment variables;
- attempts configured OpenAI-compatible endpoints in priority order;
- moves on after rate limits, authentication/configuration failures, network errors, timeouts, and server errors;
- avoids retrying malformed requests that return ordinary 4xx validation errors;
- returns the selected provider/model with the generated text;
- optionally writes a local JSON checkpoint atomically;
- never stores API keys in the checkpoint.

## Setup

Use Node.js 18 or later. Set only the keys for providers you have accounts with:

```bash
export GROQ_API_KEY="..."
export OPENROUTER_API_KEY="..."
export TOGETHER_API_KEY="..."
```

Do not commit a `.env` file or paste keys into prompts, GitHub issues, or chat. Use a secret manager in deployed environments.

Example:

```js
const { continueWithFallback } = require("./free-llm-switcher");

const result = await continueWithFallback({
  task: "Review this patch and list concrete issues.",
  messages: [{ role: "user", content: "Review the patch..." }],
  progressPath: "./.mdcp/progress.json",
  taskId: "patch-review-001"
});

console.log(result.provider, result.model, result.content);
```

The caller must supply the actual task/context and decide whether to apply or commit returned code. This module does not modify repositories or push to GitHub.

## Resume model

A checkpoint is local application state, not provider memory. A separate runner must read it and explicitly submit the next task. Store checkpoints in a private working directory, exclude them from Git, and avoid including secrets or sensitive user data. Do not assume an LLM response is a complete patch merely because an API call succeeded.

## Model list

The defaults in the switcher are examples, not availability guarantees. Check each provider's current model catalogue and free-tier terms before use. The configured model can be overridden with environment variables.
