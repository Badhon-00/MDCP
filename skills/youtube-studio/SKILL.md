---
name: youtube-studio
description: One compact cross-agent skill for planning, producing, editing, optimizing, publishing and monitoring YouTube content through approved tools.
---

# YouTube Studio — unified skill

Use this as the single entrypoint for YouTube work. Do not load every reference or enumerate every tool. First classify the request, then load only the relevant section below. Use the single `youtube` MCP tool for API operations when connected; otherwise provide a clear plan or generate local artifacts.

## Fast router
- Channel strategy, audience, niche, schedule → **Strategy**
- Script, storyboard, editing, Shorts, subtitles, audio, thumbnail → **Production**
- Keywords, titles, descriptions, chapters, metadata → **Discovery**
- Upload, playlist, schedule, visibility → **Publishing**
- Views, watch time, subscribers, competitor and channel health → **Analytics**
- Full campaign → run the stages in order, with approval before any external mutation.

## Operating rules
1. Ask only for missing information that blocks the requested task. Prefer the channel URL/ID, audience, language, format and goal.
2. Research with attributable sources and retrieval dates. Separate observed metrics from estimates and recommendations.
3. Make deliverables concrete: script, shot list, edit decision list, captions, thumbnail brief, metadata and QA checklist.
4. Preserve source media; write outputs to new paths. Use FFmpeg/selected editor for deterministic editing; never claim a render happened unless the tool confirms it.
5. Never promise views, subscribers, ranking or monetization. Recommend measurable experiments, not engagement manipulation.
6. Never buy engagement, spam comments, scrape private data, evade platform limits, bypass copyright controls or download media without rights.
7. Uploads default to private. Require explicit user approval for upload, public publishing, visibility changes, deletion, comments and playlist changes. Do not interpret a general request to "automate" as approval to publish.

## Single-tool contract
Tool name: `youtube`. Supply exactly one `operation` per call:
- `search`: `query`, optional `maxResults`
- `video_stats`: `ids` (up to 50)
- `channel_overview`: optional `channelId`; omit for the authenticated channel
- `analytics`: `startDate`, `endDate`, optional `metrics`, `dimensions`
- `upload`: `filePath`, `title`, optional `description`, `tags`, `privacyStatus`; requires `approved:true`
- `playlist_add`: `playlistId`, `videoId`; requires `approved:true`
- `thumbnail`: `input`, `text`, optional `output`
- `download_owned`: `url`; requires `rightsAttested:true`

Never pass API keys, OAuth secrets or refresh tokens as tool arguments. They belong in the host's secret manager. Cloud deployments need a shared durable quota ledger and job queue; the process-local fallback is development-only.

## Strategy
Define one audience promise, 3–5 content pillars, a repeatable format and a sustainable publishing cadence. Build a 2–4 week calendar with topic, viewer intent, hook, format, production effort and success metric. Validate ideas against channel fit rather than raw search volume alone.

## Production
For each video create: brief → hook → script → storyboard/shot list → asset checklist → edit decision list → captions → audio/visual QA → export settings. For Shorts, prioritize vertical 9:16 framing, immediate context, readable captions and a clear payoff. Keep music, footage, fonts and images rights-cleared. Use FFmpeg for repeatable batch transforms; use a human editor for creative judgment. Preserve originals and render to a separate output path.

## Discovery and packaging
Map one primary viewer intent to each video. Generate accurate, distinct titles; avoid misleading claims. Put the promise and context early in the description, use chapters when useful, and add only relevant tags/hashtags. Thumbnail concepts should communicate one idea at mobile size. Test one packaging variable at a time and compare like-for-like traffic sources and time windows.

## Publishing
Run a preflight: title, description, thumbnail, captions, end screen/cards, audience setting, visibility, scheduled time, rights and policy checks. Show the final preview and obtain approval. Prefer resumable uploads, idempotency keys, retry-safe jobs and private-by-default visibility. Scheduling and public visibility are external mutations and require approval.

## Analytics and monitoring
Track views, watch time, average view duration, impressions/CTR where available, subscribers gained/lost and returning viewers where available. Compare equal windows and annotate publication dates, format, topic and packaging changes. Public Data API statistics do not expose private retention or revenue. Use authorized YouTube Analytics for channel-owner metrics. Alert on material deviations using configurable thresholds; avoid excessive polling and respect API quota.

## Token-efficient behavior
- Keep this skill as the only always-loaded YouTube entrypoint.
- Do not paste the entire channel history or all analytics into context; request bounded date ranges and summarize only deltas.
- Prefer IDs, URLs, compact tables and top-N results over raw API payloads.
- Cache stable channel metadata; refresh volatile metrics on demand or on a user-configured schedule.
- Load only the relevant workflow section. Ask the runtime to perform deterministic transforms rather than reasoning through large logs.
- Return a short decision summary plus artifact paths and evidence. Expand only when asked.
- No tool or skill can make inference-token use zero; these rules reduce unnecessary context and tool chatter.

## Output format
Return: **Goal**, **Recommended workflow**, **Deliverables**, **Risks/approvals**, **Next measurable check**. Keep the first response compact.
