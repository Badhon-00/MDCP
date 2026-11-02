# Token Efficiency and Project Memory

MDCP reduces avoidable repeated context preparation; it cannot make inference free, promise zero tokens, or guarantee 80–90% savings. Savings depend on provider caching, model, prompt size, task and host.

## Workflow

1. Keep stable facts in the short, reviewed `MDCP_CONTEXT.md`.
2. Save durable decisions in local SQLite with `python3 tools/mdcp_memory.py remember "Title" "Decision"`.
3. Generate a bounded pack using `python3 tools/mdcp_memory.py pack --root . --max-chars 12000`.
4. Provide the pack to the coding agent or configure the host to load it.
5. Update notes only when facts change; do not attach the whole repository on every task.

## Boundaries

The SQLite database is local project memory, not ChatGPT Memory, Claude memory, Codex session state or model training. This script cannot silently write to provider-private memory. It stores only notes explicitly submitted by the user/workflow.

## Privacy

The database is under `.mdcp/`, ignored by Git. Do not store credentials, customer data, production dumps or secrets. Export to inspect; use `forget ID` to delete one record. Back up securely if needed.
