# YouTube skill: context and token budget

MDCP uses one canonical skill and one operation-routed tool instead of a large always-loaded set of YouTube tools.

## Design
- One short entrypoint skill; deeper workflows are sections loaded only when relevant.
- One stable tool name (`youtube`) with a small operation enum.
- Deterministic API work, media transforms and quota checks run in code, not in model reasoning.
- Bounded result sizes: up to 50 video IDs per request; ask for compact summaries instead of raw payloads.
- Cache stable channel metadata and avoid polling unless a schedule/threshold is configured.
- Keep credentials, job state and quota state outside model context.

## Expected effect
This reduces repeated instructions and tool-description overhead. Actual token savings depend on the host, model, prompt caching, selected workflow, result sizes and conversation history. It is not zero-token operation and no percentage is guaranteed.

## Cloud requirements
Use secret-manager-backed OAuth, a shared durable quota ledger, a durable queue, idempotent job IDs, separate media workers, bounded retries, request timeouts and observability. Do not store refresh tokens in Git or expose them to the model. Public upload, playlist mutations and other external writes require explicit approval.
