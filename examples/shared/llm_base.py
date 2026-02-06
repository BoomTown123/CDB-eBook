"""Base classes and interfaces for LLM providers.

Defines the abstract LLMProvider interface and shared data types used
by all provider implementations. Based on the production provider layer
at app/integrations/llm/base.py.

Related: Chapter 4 (Infrastructure) — Provider Abstraction Pattern
"""

import json
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from enum import Enum
from typing import Any


class MessageRole(str, Enum):
    """Message roles in a conversation."""

    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'
    TOOL = 'tool'


@dataclass
class ToolDefinition:
    """Definition of a tool available to the LLM.

    Follows the OpenAI function calling format, which OpenRouter
    also accepts for all providers.
    """

    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema
    server_name: str | None = None  # MCP server providing this tool

    def to_openai_format(self) -> dict[str, Any]:
        """Convert to OpenAI function calling format.

        This format is used by OpenRouter for all providers,
        not just OpenAI models.
        """
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': self.parameters,
            },
        }


@dataclass
class ToolCall:
    """A tool call requested by the LLM."""

    id: str
    name: str
    arguments: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'arguments': self.arguments,
        }


@dataclass
class ChatMessage:
    """A message in a chat conversation."""

    role: MessageRole
    content: str | None = None
    name: str | None = None
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API requests.

        Produces the OpenAI-compatible message format used by
        both OpenRouter and OpenAI directly.
        """
        msg: dict[str, Any] = {'role': self.role.value}

        if self.content is not None:
            msg['content'] = self.content

        if self.name is not None:
            msg['name'] = self.name

        if self.tool_calls:
            msg['tool_calls'] = [
                {
                    'id': tc.id,
                    'type': 'function',
                    'function': {
                        'name': tc.name,
                        'arguments': json.dumps(tc.arguments)
                        if isinstance(tc.arguments, dict)
                        else tc.arguments,
                    },
                }
                for tc in self.tool_calls
            ]

        if self.tool_call_id is not None:
            msg['tool_call_id'] = self.tool_call_id

        return msg


@dataclass
class UsageInfo:
    """Token usage information."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class ChatResponse:
    """Response from a chat completion."""

    content: str | None = None
    tool_calls: list[ToolCall] | None = None
    finish_reason: str | None = None
    usage: UsageInfo | None = None
    model: str | None = None

    @property
    def has_tool_calls(self) -> bool:
        """Check if response contains tool calls."""
        return self.tool_calls is not None and len(self.tool_calls) > 0


@dataclass
class StreamChunk:
    """A chunk from a streaming response."""

    content: str | None = None
    tool_calls: list[ToolCall] | None = None
    finish_reason: str | None = None
    is_final: bool = False


class LLMProvider(ABC):
    """Abstract base class for LLM providers.

    All providers (OpenRouter, OpenAI, etc.) implement this interface,
    allowing the application to switch providers without changing
    business logic. See Chapter 4: Provider Abstraction Pattern.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        model: str | None = None,
        default_max_tokens: int = 4096,
        default_temperature: float = 0.7,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.default_max_tokens = default_max_tokens
        self.default_temperature = default_temperature

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        ...

    @abstractmethod
    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        **kwargs,
    ) -> ChatResponse:
        """Send a chat completion request.

        Args:
            messages: List of messages in the conversation
            model: Model to use (overrides default)
            tools: Available tools for the model
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            ChatResponse with content and/or tool calls
        """
        ...

    @abstractmethod
    async def chat_stream(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        **kwargs,
    ) -> AsyncIterator[StreamChunk]:
        """Send a streaming chat completion request.

        Args:
            messages: List of messages in the conversation
            model: Model to use (overrides default)
            tools: Available tools for the model
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Yields:
            StreamChunk objects with content or tool calls
        """
        ...
        # Required for type checking: make this an async generator
        yield StreamChunk()  # pragma: no cover

    def _prepare_messages(self, messages: list[ChatMessage]) -> list[dict[str, Any]]:
        """Convert ChatMessage objects to API format."""
        return [msg.to_dict() for msg in messages]

    def _prepare_tools(
        self, tools: list[ToolDefinition] | None
    ) -> list[dict[str, Any]] | None:
        """Convert ToolDefinition objects to OpenAI-compatible format."""
        if not tools:
            return None
        return [tool.to_openai_format() for tool in tools]
