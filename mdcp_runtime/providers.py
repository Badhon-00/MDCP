from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Provider:
    name: str
    base_url: str
    model: str
    api_key_env: str

    @property
    def api_key(self) -> str:
        return os.getenv(self.api_key_env, "").strip()


def configured_providers() -> list[Provider]:
    raw = os.getenv("MDCP_PROVIDERS", "").strip()
    if raw:
        try:
            values = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("MDCP_PROVIDERS must be valid JSON") from exc
        if not isinstance(values, list):
            raise ValueError("MDCP_PROVIDERS must be a JSON array")
        providers = []
        for item in values:
            if not isinstance(item, dict):
                raise ValueError("Each MDCP_PROVIDERS entry must be an object")
            provider = Provider(
                name=str(item.get("name", "")).strip(),
                base_url=str(item.get("base_url", "")).rstrip("/"),
                model=str(item.get("model", "")).strip(),
                api_key_env=str(item.get("api_key_env", "")).strip(),
            )
            _validate_provider(provider)
            providers.append(provider)
        return providers

    return [
        Provider("groq", "https://api.groq.com/openai/v1", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), "GROQ_API_KEY"),
        Provider("openrouter", "https://openrouter.ai/api/v1", os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free"), "OPENROUTER_API_KEY"),
        Provider("together", "https://api.together.xyz/v1", os.getenv("TOGETHER_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"), "TOGETHER_API_KEY"),
    ]


def _validate_provider(provider: Provider) -> None:
    if not provider.name or not provider.model or not provider.api_key_env:
        raise ValueError("Provider name, model and api_key_env are required")
    if not provider.base_url.startswith("https://"):
        raise ValueError("Provider base_url must use HTTPS")


class ProviderError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, retry_after: float = 0):
        super().__init__(message)
        self.status = status
        self.retry_after = retry_after


class ProviderRouter:
    """OpenAI-compatible sequential failover with per-process cooldowns."""

    RETRYABLE = {408, 409, 425, 429, 500, 502, 503, 504}

    def __init__(self, providers: list[Provider] | None = None, timeout: float = 60, opener=None):
        self.providers = providers if providers is not None else configured_providers()
        self.timeout = timeout
        self.opener = opener or urllib.request.urlopen
        self.cooldowns: dict[str, float] = {}

    def complete(self, messages: list[dict[str, str]], max_tokens: int = 4096) -> dict[str, Any]:
        failures = []
        available = [p for p in self.providers if p.api_key and self.cooldowns.get(p.name, 0) <= time.monotonic()]
        missing = [p.name for p in self.providers if not p.api_key]
        for provider in available:
            request_data = json.dumps({
                "model": provider.model,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": max(1, min(int(max_tokens), 8192)),
            }).encode("utf-8")
            request = urllib.request.Request(
                provider.base_url + "/chat/completions",
                data=request_data,
                headers={
                    "Authorization": "Bearer " + provider.api_key,
                    "Content-Type": "application/json",
                    "User-Agent": "MDCP-Agent-Runtime/0.1",
                },
                method="POST",
            )
            try:
                with self.opener(request, timeout=self.timeout) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                content = payload.get("choices", [{}])[0].get("message", {}).get("content")
                if not isinstance(content, str) or not content.strip():
                    raise ProviderError("Provider returned an empty response")
                return {"provider": provider.name, "model": provider.model, "content": content, "failures": failures}
            except urllib.error.HTTPError as exc:
                retry_after = _retry_after(exc.headers.get("Retry-After"))
                failures.append({"provider": provider.name, "status": exc.code, "error": _safe_http_error(exc)})
                self.cooldowns[provider.name] = time.monotonic() + (max(retry_after, 2 if exc.code == 429 else 0) if exc.code in self.RETRYABLE else 300)
            except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, IndexError) as exc:
                failures.append({"provider": provider.name, "status": None, "error": type(exc).__name__})
                self.cooldowns[provider.name] = time.monotonic() + 15

        if missing:
            failures.extend({"provider": name, "status": None, "error": "missing_api_key"} for name in missing)
        error = ProviderError("No configured provider completed the request")
        error.failures = failures
        raise error


def _retry_after(value: str | None) -> float:
    try:
        return max(0.0, min(float(value or 0), 900.0))
    except ValueError:
        return 0.0


def _safe_http_error(exc: urllib.error.HTTPError) -> str:
    # Provider response bodies can contain user data; do not persist or log them.
    return {401: "unauthorized", 403: "forbidden", 408: "timeout", 429: "rate_limited"}.get(exc.code, "provider_http_error")
