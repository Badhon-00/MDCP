# Free Provider Guide

Free-tier details are mutable. This guide lists provider categories to look for, not guaranteed quotas or a permanent list of model IDs.

| Provider | Typical access model | Notes |
|---|---|---|
| Ollama | Local runtime | No hosted token quota; limited by device hardware, memory and power |
| Google Gemini API | API key / free tier where eligible | Model and region restrictions apply |
| Groq | API key / developer free tier | Rate limits and supported models change |
| Cerebras | API key / developer tier | Availability and daily/RPM caps can change |
| Cloudflare Workers AI | Cloudflare account | Free allocation and billing terms vary |
| NVIDIA NIM | Developer access | Per-model limits and access requirements vary |
| Hugging Face Inference | Account / free allowance | Credits, provider availability and rate limits vary |
| OpenRouter | Models marked `:free` | Availability, provider load and rate limits vary |

## Rules

1. Check the live OmniRoute provider catalog and official provider pricing/terms on the day of use.
2. Do not assume every free model supports tool calling, long context, coding agents or vision.
3. Use only accounts and keys the user is authorized to use.
4. Do not evade limits through account rotation or parallel identities.
5. If hosted free quotas are exhausted, wait for reset or use a local Ollama model.
6. Never send confidential code to a provider without reviewing its data handling terms.
