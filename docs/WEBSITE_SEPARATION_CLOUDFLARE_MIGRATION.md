# MDCP Website Separation and Cloudflare Pages Migration

**Core repository:** https://github.com/Badhon-00/MDCP  
**Website repository:** https://github.com/Badhon-00/MDCP-SITE  
**Hosting target:** Cloudflare Pages  
**Status:** Source migration completed. The original charcoal/white `site/` interface and SVG favicon were moved into MDCP-SITE; shared SVG brand assets are retained in this repository. Cloudflare Pages configuration and production deployment remain unverified.

## Repository boundaries

### MDCP (core)

Keep the core repository focused on:
- Skills and agent instructions
- Claude Code marketplace/plugin metadata
- Codex and other platform adapters
- MCP server and connector documentation
- OmniRoute integration guides
- CLI, validation and test tooling
- License notices and security policies

Do not make the core repository depend on the website build to publish skills or releases.

### MDCP-SITE (website)

The separate site repository should contain only:
- The public MDCP website and skill explorer UI
- Static documentation/catalog presentation
- Search and category navigation over published catalog data
- Responsive footer, accessibility and metadata
- Cloudflare Pages build configuration and deployment checks

The site must consume a pinned MDCP release, generated catalog artifact, or explicitly versioned public data source. It must not scrape arbitrary repository files at runtime or execute downloaded skill content in the browser.

## Suggested site structure

    MDCP-SITE/
    ├── public/
    │   ├── favicon.svg
    │   ├── robots.txt
    │   └── og/
    ├── src/
    │   ├── components/
    │   │   ├── Header.*
    │   │   ├── Footer.*
    │   │   ├── SkillCard.*
    │   │   └── Search.*
    │   ├── data/
    │   │   └── catalog.schema.json
    │   ├── pages/
    │   └── styles/
    ├── scripts/
    │   └── validate-catalog.*
    ├── tests/
    ├── .github/workflows/
    ├── LICENSE
    ├── THIRD_PARTY_NOTICES.md
    ├── README.md
    └── package.json

The migrated site intentionally preserves the original static HTML/CSS/JavaScript implementation rather than introducing a framework. Its build script reads `skills/*/SKILL.md` from the canonical MDCP repository and emits a static `catalog.json`. The personal `badhon-00.github.io` site and its server/API files were not changed.

## Footer information architecture

- **Product:** MDCP, Skill Explorer, Changelog
- **AI platforms:** Claude.ai, Claude Code, OpenAI Codex, ChatGPT, Gemini, Cursor, Windsurf
- **Developer resources:** Skills, MCP, Plugins, Agent adapters, API integrations
- **Project:** GitHub, Contributing, Roadmap, Releases
- **Trust:** Security, Privacy, License, Third-party notices
- **Community:** Discussions and issue tracker

Footer requirements:
- Responsive two-column mobile layout and wider desktop grid
- Accessible semantic navigation and visible keyboard focus
- SVG icons with accessible labels; avoid decorative emoji
- Correct external-link rel attributes
- Real repository/documentation URLs only
- Copyright and trademark notices that do not imply vendor endorsement

## Cloudflare Pages deployment contract

Connect the GitHub repository through Cloudflare Dashboard:
1. Open **Workers & Pages**.
2. Choose **Create application → Pages → Connect to Git**.
3. Authorize the Cloudflare Workers & Pages GitHub App for **only** the MDCP-SITE repository where possible.
4. Select Badhon-00/MDCP-SITE and production branch main.
5. Configure the framework's actual build command and output directory after the framework is chosen.
6. Configure preview branch behavior, build checks, custom domain and environment variables.
7. Deploy, then verify production URL, preview deployment, mobile layout, accessibility, 404 handling and build logs.

Do not add API keys or secrets to the repository. Set them only in Cloudflare's encrypted environment-variable settings if the site genuinely needs them.

**Important:** Cloudflare Pages Git integration cannot later be converted to Direct Upload. Choose Git integration intentionally. Scope the Cloudflare GitHub App to only the repository required for this site.

## GitHub Pages retirement checklist

The intended retirement scope is:
- Badhon-00/MDCP
- Badhon-00/badhon-00.github.io

Do not delete either repository. Do not delete branches, releases, tags, custom domains, DNS records, or source files as part of disabling Pages.

Before disabling:
1. Confirm which repository currently owns each Pages site and whether a custom domain is attached.
2. Deploy and test the replacement on Cloudflare Pages.
3. Confirm DNS and custom-domain ownership and prepare rollback.
4. Disable GitHub Pages using repository Settings → Pages (or the supported GitHub Pages API).
5. Verify the old GitHub Pages deployment is no longer serving content.
6. Keep all Git repositories and history intact.

The available GitHub connection used for this change can inspect repositories and commit files, but it does not expose the repository-administration action required to create a repository or change Pages settings. Therefore neither operation should be represented as completed until it is performed and verified in GitHub.

## Acceptance checklist

- [x] MDCP-SITE repository exists and is separate from MDCP
- [x] Original `MDCP/site/` page and favicon moved to MDCP-SITE root
- [x] Shared monochrome MDCP mark and wordmark added to both repositories
- [x] MDCP core source and personal website source/history remain intact
- [x] Website source validation workflow added (Cloudflare production build still pending)
- [ ] Footer links all resolve to real destinations
- [ ] Search, category filters and skill detail links work
- [ ] Mobile, tablet and desktop layouts pass
- [ ] Keyboard navigation and accessibility checks pass
- [ ] No secrets or private data in Git history
- [ ] Cloudflare Pages production deployment verified
- [ ] GitHub Pages disabled for both requested repositories
- [ ] Rollback procedure and DNS state documented
