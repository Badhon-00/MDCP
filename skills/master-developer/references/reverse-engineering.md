# reverse-engineering.md: REA (Reverse Engineer Anything)

REA is a separate MCP server for analyzing binaries, applications and runtime behavior. Source: https://github.com/morluto/rea (your copy: Badhon-00/Reverse-engine). It is not bundled here; install it from its own package.

```bash
npx rea-agents setup     # choose agents, review the proposed changes, approve, restart the agent
```

Linux needs a procps-compatible `ps` on PATH; see `docs/installation.md` in the REA repo.

## Use only for
Security research, malware and incident analysis, vulnerability research with coordinated disclosure, CTFs and education, interoperability, preservation, and debugging or auditing software you own or are authorized to examine.

## Do not use for
Bypassing DRM, license checks or anti-cheat; game cheats; defeating authentication or access controls on systems you are not authorized to test; copying proprietary code or assets; evading AI provider policies. This is the REA project's own disclaimer, and it applies here too.

## Working rules
- Confirm authorization and scope before touching a target. If unclear, ask.
- Analyze copies, in an isolated environment, never your daily machine, when the sample may be malicious.
- Record findings (what, where, evidence); do not hand over working exploits for software you do not own.
- For rebuilding an app's features, use the replica-* skills, which are clean-room and rebrand-before-launch.
