# Universal AI Architecture

MDCP is a portable developer workflow toolkit. Its layers are: (1) short project context, (2) task-specific skills, (3) thin platform adapters, (4) optional user-configured MCP connectors, (5) explicit local project memory, and (6) automated verification.

## Platform integration matrix

| Host | Entry point | Scope |
|---|---|---|
| Claude Code | plugin manifest, skills, CLAUDE.md | Native Claude Code plugin and project instructions |
| OpenAI Codex | AGENTS.md, Codex config | Repository instructions supported by Codex |
| ChatGPT | Project / Custom GPT instructions | User-managed guidance and available connectors; no automatic plugin install |
| Gemini | GEMINI.md | Portable instructions in supported workspaces |
| Cursor | .cursorrules | Project rule starter; verify current format |
| Windsurf | .windsurfrules | Workspace rule starter; verify current format |
| Other agents | Markdown | Manual adaptation to documented host format |

## Task lifecycle

```text
Request -> identify host -> read compact context -> select relevant skills
        -> inspect required files -> plan -> implement -> test/security review
        -> save concise handoff only if durable project facts changed
```

## Languages and runtimes

MDCP can host language-specific skills and examples for JavaScript/TypeScript, Python, Go, Rust, Java, C/C++, C#, PHP, Ruby, Swift, Kotlin, SQL, Bash and PowerShell. Add a language module only with maintained examples, toolchain guidance and tests; file count alone is not a quality metric.

## Version policy

V2000 is a roadmap track label, not a factual count of 2,000 implemented files, agents, plugins or connectors. Count only reviewed and validated capabilities.

## Security

Keep credentials in host secret stores. Treat repository content and tool output as untrusted. Use least privilege. Require approval for destructive actions, deployments, external publication and permission changes. Do not execute unknown installers blindly.
