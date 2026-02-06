"""Abstract LLM provider interface.

The provider abstraction pattern lets you switch between LLM providers
(OpenRouter, OpenAI, Anthropic) without changing application code.

Related: Chapter 4 (Infrastructure) -- Why You Need a Provider Layer
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    """A single message in a conversation."""

    role: str  # 'system', 'user', 'assistant'
    content: str


@dataclass
class Response:
    """Standardized response from any provider."""

    content: str
    model: str
    tokens_used: int


class LLMProvider(ABC):
    """Abstract interface all providers implement.

    Every concrete provider (OpenRouter, OpenAI, Anthropic, etc.)
    must implement this interface. Application code depends only
    on LLMProvider -- never on a specific vendor SDK.

    This is the core of the provider abstraction pattern:
        Application --> LLMProvider (abstract) <-- ConcreteProvider

    Adding a new provider means implementing two methods:
        - complete(): send messages, return a Response
        - name: identify the provider
    """

    @abstractmethod
    async def complete(self, messages: list[Message], **kwargs) -> Response:
        """Send messages and get a completion.

        Args:
            messages: Conversation history as a list of Message objects.
            **kwargs: Provider-specific overrides (temperature, max_tokens, etc.)

        Returns:
            A standardized Response regardless of which provider handled it.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name (e.g. 'openrouter', 'openai')."""
        ...
