# MDCP YouTube Studio

Cloud-ready, opt-in YouTube creator toolkit. It combines the supplied `youtube-growth-toolkit` feature map with a host-neutral Node.js runtime using official Google APIs.

## Capabilities
- Public channel/video/playlist metadata and statistics through YouTube Data API v3.
- OAuth-backed resumable uploads and playlist operations; uploads default to **private**.
- YouTube Analytics API reports for authorized channel owners.
- SEO research workflows for topics, titles, descriptions, chapters, tags and thumbnail briefs.
- FFmpeg thumbnail/media helpers and optional yt-dlp download adapter for content the operator owns or is licensed to use.
- Channel monitoring, content calendar, publishing queue, approval gates and evidence-based growth experiments.

## Cloud deployment
The runtime is stateless except for a process-local quota fallback. Production deployments must inject a durable `quotaLedger.consume(units, operation)` implementation backed by a shared database, keep OAuth secrets in a secret manager, and run media rendering in a separate worker with FFmpeg installed. Long renders and large uploads should not run inside short-lived serverless request handlers.

Connect this package to an MCP server, API Anything connector, serverless function or agent tool adapter. It does not auto-install remote plugins or connect accounts.

## Setup
1. Enable YouTube Data API v3 and YouTube Analytics API in Google Cloud.
2. Create OAuth credentials and grant only required scopes.
3. Inject `YOUTUBE_API_KEY`, `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` via a secret manager.
4. Use Node.js 20+. Install FFmpeg/yt-dlp only for optional media jobs.
5. Read [the ecosystem guide](../../docs/YOUTUBE_ECOSYSTEM.md).

## Runtime exports
- `createYouTubeClient()`: quota-aware Data API client with OAuth refresh.
- `queryChannelAnalytics()`: OAuth-backed Analytics API report.
- `createThumbnail()`: FFmpeg thumbnail helper using a text file, not shell interpolation.
- `downloadOwnedMedia()`: HTTPS YouTube-only yt-dlp wrapper with rights reminder.

## Safety
Publishing, deletion, comments, playlist mutation and visibility changes require explicit user approval. No fake engagement, spam, policy evasion, copyright circumvention, quota bypass or unlicensed downloads. Public Data API statistics are not private channel analytics.

MDCP's repository license applies to original MDCP-authored files. Upstream projects retain their own licenses and trademarks; verify them before adopting or redistributing code.
