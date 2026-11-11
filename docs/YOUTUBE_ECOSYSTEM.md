# MDCP YouTube Cloud Ecosystem

MDCP provides a modular YouTube creator toolchain, not a blind merge of third-party repositories.

## Skill packs
| Skill | Scope |
|---|---|
| youtube-studio | End-to-end orchestration |
| youtube-channel-strategy | Audience, niche, pillars, calendar |
| youtube-video-production | Scripts, editing, captions, thumbnails, QA |
| youtube-seo-discovery | Search intent, titles, descriptions, tags, chapters |
| youtube-publishing-automation | OAuth, uploads, playlists, scheduling gates |
| youtube-analytics-monitoring | Channel health, metrics, alerts, experiments |

Canonical skills are in `skills/`. Portable agent mirrors are maintained in `.agents/skills/` and `.gpt/skills/`.

## Cloud architecture
```text
Agent / MCP host
  -> YouTube Studio tool adapter
      -> OAuth secret manager
      -> YouTube Data API / Analytics API
      -> durable quota + job store
      -> queue -> media worker (FFmpeg / yt-dlp)
      -> approval gate -> upload / schedule
      -> monitoring collector -> analytics store
```

Keep request handlers stateless. Use a durable queue for long-running jobs and a shared quota ledger across replicas. The runtime's in-memory quota counter is development-only. Never commit OAuth tokens.

## Uploaded toolkit review
The uploaded `youtube-growth-toolkit.zip` contained feature ideas for uploads, playlists, yt-dlp, FFmpeg audio/thumbnail processing, title/tag/description helpers, competitor search and view statistics. It had no LICENSE file, so MDCP integrates the feature map and provides a hardened runtime rather than copying source wholesale.

The adapter streams uploads instead of loading the full video into RAM, reads credentials from injected secrets, defaults uploads to private, supports durable quota accounting, launches FFmpeg without a shell, restricts yt-dlp URLs to HTTPS YouTube hosts, and calls private analytics through the OAuth-backed Analytics API.

## Limits
YouTube quotas and API availability can change. Some metrics cannot be combined in one report. Public statistics do not expose private retention or revenue. No tool can guarantee rankings, views, subscribers or monetization.
