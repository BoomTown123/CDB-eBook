"""
OpenAI provider adapter for the AI Gateway.

Uses raw httpx instead of the openai SDK so the gateway has zero
provider-specific dependencies. This keeps the install lightweight
and gives you full control over HTTP behavior (timeouts, retries,
connection pooling).

Reference: Chapter 4 - The AI Tool Gateway Pattern
"""

import json
import logging
import os
import time
from typing import AsyncIterator

import httpx

from .base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ToolCall,
    Usage,
)

logger = logging.getLogger("ai_gateway.openai")

_BASE_URL = "https://api.openai.com/v1"


class OpenAIProvider(BaseProvider):
    """
    OpenAI adapter using raw httpx.

    Translates gateway-standard CompletionRequest/CompletionResponse
    into OpenAI's chat completions API format and back. No SDK needed ---
    just HTTP POST with JSON.
    """

    def __init__(self) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable is required")
        self._api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=_BASE_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
        )

    @property
    def name(self) -> str:
        return "openai"

    @property
    def available_models(self) -> list[str]:
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "o1",
            "o1-mini",
            "o3-mini",
        ]

    def _build_payload(self, request: CompletionRequest, stream: bool = False) -> dict:
        """Build the JSON payload for chat/completions."""
        messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in request.messages
        ]
        payload: dict = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if stream:
            payload["stream"] = True
        if request.tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    },
                }
                for t in request.tools
            ]
        return payload

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Send a completion request to OpenAI via raw HTTP."""
        start = time.monotonic()

        payload = self._build_payload(request)
        resp = await self._client.post("/chat/completions", json=payload)

        if resp.status_code != 200:
            body = resp.text
            logger.error("OpenAI API error %d: %s", resp.status_code, body)
            raise RuntimeError(
                f"OpenAI API returned {resp.status_code}: {body}"
            )

        data = resp.json()
        latency_ms = (time.monotonic() - start) * 1000

        choice = data["choices"][0]
        message = choice["message"]
        usage_data = data.get("usage", {})

        # Parse tool calls if present
        tool_calls = None
        if message.get("tool_calls"):
            tool_calls = [
                ToolCall(
                    id=tc["id"],
                    name=tc["function"]["name"],
                    arguments=tc["function"]["arguments"],
                )
                for tc in message["tool_calls"]
            ]

        return CompletionResponse(
            content=message.get("content") or "",
            model=data.get("model", request.model),
            provider=self.name,
            usage=Usage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0),
            ),
            tool_calls=tool_calls,
            latency_ms=latency_ms,
        )

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream tokens from OpenAI using server-sent events."""
        payload = self._build_payload(request, stream=True)

        async with self._client.stream(
            "POST", "/chat/completions", json=payload
        ) as resp:
            if resp.status_code != 200:
                body = await resp.aread()
                raise RuntimeError(
                    f"OpenAI API returned {resp.status_code}: {body.decode()}"
                )

            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data_str = line[len("data: "):]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content")
                    if content:
                        yield content
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

    async def health_check(self) -> bool:
        """Verify OpenAI is reachable with a lightweight models list call."""
        try:
            resp = await self._client.get("/models")
            return resp.status_code == 200
        except Exception:
            return False
