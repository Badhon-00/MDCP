# Platform Adapters

Adapters are small host-specific entry points. They should link to the portable project context and avoid duplicating the full documentation.

| Platform | Entry point | Setup |
|---|---|---|
| Claude Code | `CLAUDE.md` | Keep the file at repository root; use the existing MDCP marketplace plugin |
| OpenAI Codex | `AGENTS.md` | Codex reads repository agent instructions according to its documented discovery rules |
| ChatGPT | `adapters/chatgpt/README.md` | Copy the concise instructions into a Project or Custom GPT; connect tools through supported settings |
| Gemini | `adapters/gemini/GEMINI.md` | Add the instructions to the supported Gemini workspace or project |
| Cursor | `adapters/cursor/.cursorrules` | Import into project rules; migrate to the current supported rules format if needed |
| Windsurf | `adapters/windsurf/.windsurfrules` | Add as workspace rules where supported |

These files are starter templates. They do not install software, authenticate accounts, or guarantee that every host reads the same path. Verify each host's current documentation before relying on automatic discovery.
