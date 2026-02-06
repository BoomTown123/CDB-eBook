"""
Base provider interface for the AI Gateway.

All provider adapters implement this interface so the gateway can route
requests to any backend without changing calling code. This is the
abstraction layer that makes provider-switching a config change rather
than a code change.

No SDK dependencies --- every provider uses raw httpx so you control
the HTTP layer and can swap providers without installing anything new.

Reference: Chapter 4 - The AI Tool Gateway Pattern
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator


class MessageRole(str, Enum):
    """Standard roles across all providers."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class ToolDefinition:
    """A tool the model can call (function-calling / tool-use)."""
    name: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolCall:
    """A tool invocation returned by the model."""
    id: str
    name: str
    arguments: str  # JSON string


@dataclass
class Message:
    """A single message in a conversation."""
    role: MessageRole
    content: str
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None


@dataclass
class CompletionRequest:
    """Provider-agnostic completion request."""
    messages: list[Message]
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024
    stream: bool = False
    tools: list[ToolDefinition] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Usage:
    """Token usage for a single completion."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class CompletionResponse:
    """Provider-agnostic completion response."""
    content: str
    model: str
    provider: str
    usage: Usage = field(default_factory=Usage)
    tool_calls: list[ToolCall] | None = None
    latency_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseProvider(ABC):
    """
    Abstract base for all AI provider adapters.

    Each provider (OpenAI, Anthropic, etc.) implements this interface.
    The gateway routes requests through whichever provider is configured
    without the caller needing to know which backend is handling the request.

    This is the core abstraction that makes the gateway pattern work:
    one interface, many backends, zero calling-code changes when you switch.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier (e.g., 'openai', 'anthropic')."""
        ...

    @property
    @abstractmethod
    def available_models(self) -> list[str]:
        """Models this provider supports."""
        ...

    @abstractmethod
    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Send a completion request and return the response."""
        ...

    @abstractmethod
    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream a completion response token by token."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if the provider is reachable and responding."""
        ...

    def supports_model(self, model: str) -> bool:
        """Check whether this provider handles the given model."""
        return model in self.available_models
