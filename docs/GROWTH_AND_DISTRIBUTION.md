# MDCP — Community Growth & Distribution Plan

MDCP is a curated toolkit for developers using Claude Code, Claude.ai workflows, ChatGPT, and Codex. It combines a Claude Code plugin with portable agent guidance, skills, and MCP setup notes. The project should be promoted on the strength of its real capabilities, clear compatibility boundaries, reproducible installs, and useful examples.

## Public positioning

**Suggested short description**

A curated developer toolkit with 82 skills, MCP setup guides, and cross-agent instructions for Claude Code, ChatGPT, and Codex—built for secure, tested software delivery.

**One-line value proposition**

Spend less time wiring AI coding agents and more time shipping reviewed, tested software.

**Who it helps**
- Developers who use AI coding agents across more than one platform.
- Teams that want repeatable security, testing, backend, frontend, and deployment workflows.
- Maintainers who want portable instructions without pretending every host supports every plugin format.

## What makes the project worth trying

1. A documented Claude Code marketplace installation.
2. A curated skill collection with upstream attribution and license notices.
3. Separate Codex and GPT companion guidance instead of overwriting vendor-specific files.
4. MCP setup notes that distinguish verified configuration from unverified provider support.
5. Validation scripts and CI for repository structure and metadata.

Do not advertise a feature as supported until it has a reproducible test and a documented host/version. Skills, plugins, MCP servers, and project instructions are different integration mechanisms.

## Repository discovery checklist

- [ ] Set a concise GitHub repository description matching the short description above.
- [ ] Set the homepage to the repository's best maintained documentation or demo page; do not use a dead or placeholder URL.
- [ ] Add focused topics: `ai-agents`, `agent-skills`, `claude-code`, `codex`, `chatgpt`, `mcp`, `developer-tools`, `developer-productivity`, `security`, `testing`.
- [ ] Enable GitHub Discussions in Settings → General → Features.
- [ ] Add a social preview image (1200×630) that shows the project name, the cross-agent use case, and a readable product screenshot/diagram.
- [ ] Keep the README's first screen focused on what it is, who it is for, and a copyable quick start.
- [ ] Publish versioned releases with concise notes and install/upgrade instructions.
- [ ] Keep CI status visible and make the validation command easy to run locally.
- [ ] Keep issue templates short and route questions to Discussions after Discussions are enabled.

## Distribution channels

Share the project where it is directly useful, with a short explanation and a link to the exact relevant section. Follow each community's self-promotion rules. Do not mass-post identical messages.

| Channel | Best content | Cadence |
|---|---|---|
| GitHub Discussions | Roadmap, setup questions, adoption stories, design decisions | Reply when there is a real update |
| Reddit communities for Claude Code, Codex, MCP, and developer tooling | A technical walkthrough, benchmark, or honest launch post | Only where self-promotion is allowed |
| Hacker News | A concise Show HN post with a concrete problem, demo, and limitations | One launch post; engage with comments |
| Dev.to / Hashnode | Tutorial: use one skill end-to-end, show commands and test results | One useful article per major capability |
| X / LinkedIn | Short demo clips, release notes, technical lessons | Only when there is something new |
| Skills/MCP directories | Accurate listing with canonical source and install instructions | Submit only after checking each directory's rules |

## 30-day organic launch plan

### Days 1–3: make adoption frictionless
- Test the documented installation on a clean environment.
- Record exact host versions and supported features.
- Add screenshots or a short terminal demo.
- Fix broken links, unclear prerequisites, and unsupported claims.
- Enable Discussions and add the categories in COMMUNITY_DISCUSSIONS.md.

### Days 4–7: launch with proof
- Publish a release with a useful changelog.
- Publish one technical walkthrough showing a real task from request to tests.
- Share a tailored announcement in a small number of relevant communities.
- Respond to every genuine question with reproducible steps.

### Week 2: invite contributors
- Label starter tasks as `good first issue` only when they are truly scoped.
- Publish a contributor guide and skill contribution checklist.
- Ask users which host, skill, or workflow they actually tested.
- Review incoming reports quickly; close duplicates respectfully.

### Week 3: demonstrate value
- Publish before/after examples and a reproducible validation run.
- Add an adoption story only with the user's permission.
- Improve the most-used install path based on issue/discussion feedback.

### Week 4: review and iterate
- Review GitHub traffic, clones, referrers, stars, forks, issues, and releases in Insights.
- Track conversion: visitor → README quick start → successful install → repeat use → contribution.
- Prioritize fixes that improve successful adoption, not vanity metrics.
- Publish a transparent monthly update with what changed and what remains unsupported.

## Metrics that matter

Track weekly:
- Unique visitors and clone count (GitHub Insights → Traffic).
- Referring sites and popular content.
- Release downloads, where available.
- Successful install reports and reproducible bug reports.
- First-time contributors and merged community PRs.
- Discussion questions answered and time to first maintainer response.
- Stars and forks as lagging indicators, not the product goal.

Never buy stars, exchange artificial engagement, run follow-for-follow schemes, create fake accounts, or script fake issues/discussions. These tactics damage trust and can violate platform rules.

## Release quality gate

Before every public release:
1. Run `python3 scripts/validate.py`.
2. Test the quick-start commands on a clean environment.
3. Verify every documented MCP endpoint and host configuration against current official provider docs.
4. Check licenses and preserve all upstream attribution.
5. State what was tested, on which versions, and what was not tested.
6. Link known limitations and provide a rollback/uninstall path.

## Maintainer actions still requiring GitHub settings

The repository currently needs its description, topics, social preview, and Discussions feature configured in GitHub repository settings. These are repository metadata/settings, not ordinary committed files. Enable Discussions first, then create the categories and seed posts described in COMMUNITY_DISCUSSIONS.md.
