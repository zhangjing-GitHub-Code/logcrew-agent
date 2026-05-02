"""LLM client with retry and fallback support."""

import asyncio
from typing import Any

import httpx

from logcrew.config import LLM_API_KEY, LLM_BASE_URL


class LLMClient:
    """Async LLM client with exponential-backoff retry and model fallback."""

    def __init__(
        self,
        base_url: str = LLM_BASE_URL,
        api_key: str = LLM_API_KEY,
        fallback_url: str | None = None,
        max_retries: int = 3,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.fallback_url = fallback_url.rstrip("/") if fallback_url else None
        self.max_retries = max_retries
        self._client = httpx.AsyncClient(timeout=30.0)

    async def chat(self, messages: list[dict[str, str]], model: str = "") -> dict[str, Any]:
        """Call chat completions with retry and optional fallback endpoint."""
        payload = {
            "model": model or "claude-3-5-sonnet",
            "messages": messages,
            "temperature": 0.2,
        }
        return await self._request_with_retry("/v1/chat/completions", payload)

    async def _request_with_retry(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        urls = [self.base_url]
        if self.fallback_url:
            urls.append(self.fallback_url)

        last_err: Exception | None = None

        for url in urls:
            for attempt in range(1, self.max_retries + 1):
                try:
                    response = await self._client.post(
                        f"{url}{path}",
                        json=payload,
                        headers={"Authorization": f"Bearer {self.api_key}"},
                    )
                    response.raise_for_status()
                    return response.json()
                except (httpx.HTTPStatusError, httpx.NetworkError, httpx.TimeoutException) as exc:
                    last_err = exc
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)

        raise last_err or RuntimeError("All LLM endpoints failed")

    async def close(self) -> None:
        await self._client.aclose()
