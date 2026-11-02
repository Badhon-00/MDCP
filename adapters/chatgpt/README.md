# ChatGPT Project / Custom GPT Adapter

MDCP does not install a native ChatGPT plugin into an account. Use this adapter as portable project guidance.

## Setup
1. Open a ChatGPT Project or Custom GPT configuration that you control.
2. Copy the concise rules below into its instructions.
3. Add only the relevant sanitized project files as knowledge/context.
4. Connect external services only through connectors or actions actually available in your ChatGPT environment.
5. Keep credentials in the provider's secure connection flow; never paste secrets into repository files.

## Instructions
You are assisting with this repository. Read `MDCP_CONTEXT.md` when supplied. Inspect only files required by the current task. Use task-specific skills and connector tools only when available. Do not assume access to the user's GitHub, filesystem, terminal, cloud account or provider memory. Verify changes with tests. Summarize durable decisions in a short Markdown handoff that the user can save to the project.

## Important
ChatGPT Projects, Custom GPTs, connectors, actions and memory have separate availability and permission models. This repository cannot force them to install or permanently store context.
