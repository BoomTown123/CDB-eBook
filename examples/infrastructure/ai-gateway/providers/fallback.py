"""
Fallback and retry logic for the AI Gateway.

Implements the resilience layer: if the primary provider fails, the
gateway automatically retries and then falls back to an alternate
provider. This is why multi-provider support matters --- not for
cost optimization on day one, but for reliability.

Reference: Chapter 4 - The AI Tool Gateway Pattern
"""

import asyncio
import logging
from typing import AsyncIterator

from .base import BaseProvider, CompletionRequest, CompletionResponse

logger = logging.getLogger("ai_gateway.fallback")


class FallbackProvider(BaseProvider):
    """
    Wraps multiple providers with retry + fallback logic.

    Order matters: the first provider in the list is the primary. If it
    fails after retries, the gateway moves to the next provider. This
    gives you provider redundancy without manual intervention.

    Usage:
        provider = FallbackProvider(
            providers=[openai_provider, anthropic_provider],
            max_retries=2,
            retry_delay=1.0,
        )
    """

    def __init__(
        self,
        providers: list[BaseProvider],
        max_retries: int = 2,
        retry_delay: float = 1.0,
    ) -> None:
        if not providers:
            raise ValueError("At least one provider is required")
        self._providers = providers
        self._max_retries = max_retries
        self._retry_delay = retry_delay

    @property
    def name(self) -> str:
        names = [p.name for p in self._providers]
        return f"fallback({', '.join(names)})"

    @property
    def available_models(self) -> list[str]:
        models: list[str] = []
        for provider in self._providers:
            models.extend(provider.available_models)
        return models

    def _find_provider_for_model(self, model: str) -> list[BaseProvider]:
        """Return providers that support the given model, in priority order."""
        return [p for p in self._providers if p.supports_model(model)]

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """
        Try each provider in order with retries.

        On each provider: retry up to max_retries times with exponential
        backoff. If all retries fail, move to the next provider. If all
        providers fail, raise the last exception.
        """
        candidates = self._find_provider_for_model(request.model)
        if not candidates:
            candidates = self._providers  # Fall back to all if no model match

        last_error: Exception | None = None

        for provider in candidates:
            for attempt in range(self._max_retries + 1):
                try:
                    logger.info(
                        "Trying provider=%s model=%s attempt=%d",
                        provider.name,
                        request.model,
                        attempt + 1,
                    )
                    return await provider.complete(request)

                except Exception as exc:
                    last_error = exc
                    logger.warning(
                        "Provider %s failed (attempt %d/%d): %s",
                        provider.name,
                        attempt + 1,
                        self._max_retries + 1,
                        str(exc),
                    )
                    if attempt < self._max_retries:
                        delay = self._retry_delay * (2 ** attempt)
                        await asyncio.sleep(delay)

            logger.error(
                "Provider %s exhausted all retries, falling back", provider.name
            )

        raise RuntimeError(
            f"All providers failed. Last error: {last_error}"
        )

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """
        Stream with fallback.

        Streaming is harder to retry mid-stream, so we attempt each
        provider once. If the stream fails, we try the next provider
        from the beginning.
        """
        candidates = self._find_provider_for_model(request.model)
        if not candidates:
            candidates = self._providers

        last_error: Exception | None = None

        for provider in candidates:
            try:
                async for token in provider.stream(request):
                    yield token
                return  # Successful stream completed
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Stream from %s failed, trying next provider: %s",
                    provider.name,
                    str(exc),
                )

        raise RuntimeError(
            f"All providers failed to stream. Last error: {last_error}"
        )

    async def health_check(self) -> bool:
        """Return True if at least one provider is healthy."""
        for provider in self._providers:
            if await provider.health_check():
                return True
        return False
