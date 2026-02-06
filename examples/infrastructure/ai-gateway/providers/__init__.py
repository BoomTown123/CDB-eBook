"""AI provider adapters for the gateway pattern.

All providers use raw httpx --- no SDK dependencies.
"""

from .anthropic import AnthropicProvider
from .base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    Message,
    MessageRole,
    ToolCall,
    ToolDefinition,
    Usage,
)
from .fallback import FallbackProvider
from .openai import OpenAIProvider
from .openrouter import OpenRouterProvider

__all__ = [
    "AnthropicProvider",
    "BaseProvider",
    "CompletionRequest",
    "CompletionResponse",
    "FallbackProvider",
    "Message",
    "MessageRole",
    "OpenAIProvider",
    "OpenRouterProvider",
    "ToolCall",
    "ToolDefinition",
    "Usage",
]
