# Token Efficiency and Project Memory

MDCP aims to reduce repeated context loading. It cannot make model inference free, guarantee an 80–90% saving, or write permanently to a provider's private memory. Actual savings depend on the model, prompt cache, repository size, task and host.

## What the memory layer does

- Stores explicit project decisions and handoff notes in a local SQLite database.
- Generates a bounded context pack from short instruction files and selected memory records.
- Deduplicates repeated memory entries by content hash.
- Keeps secrets out of memory by policy.
- Lets a developer inspect, export, back up and delete local memory.

## Recommended workflow

1. Keep stable project facts in `MDCP_CONTEXT.md` (short, curated, reviewed).
2. Keep durable decisions in `.mdcp/memory.sqlite3` using `tools/mdcp_memory.py remember`.
3. Before a task, run `python3 tools/mdcp_memory.py pack --root . --max-chars 12000`.
4. Paste or attach the generated context to the coding agent, or configure the host to load it.
5. After a meaningful change, save a concise decision or handoff note.
6. Rebuild the pack only when source files change; do not dump the entire repository into every prompt.

## Memory is not model training

Local project memory is not the same as ChatGPT Memory, Claude memory, Codex session state, or another provider's private storage. The CLI cannot silently write to those services. Each provider controls its own memory, retention, permissions and context limits.

## Practical savings

The tools reduce avoidable repeated reads by selecting a small set of project facts and keeping notes concise. They do not guarantee a percentage. Measure token usage with the host's own usage meter before and after adopting the workflow.

## Files and privacy

- `.mdcp/` is ignored by Git by default; commit only intentionally shareable, sanitized summaries.
- Do not store credentials, access tokens, private customer data, production dumps or secrets.
- Back up the SQLite database securely if it contains important project decisions.
- Use `forget` to remove a memory record and `export` to inspect the stored data.
