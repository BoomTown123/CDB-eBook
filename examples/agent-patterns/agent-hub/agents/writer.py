"""
Writing specialist agent.

Handles content creation: emails, summaries, reports, blog posts.
Each specialist has a domain-tuned system prompt and temperature.

Book reference: Chapter 6, Section 2 - The Agent Hub Pattern
"""

import logging
import sys
from pathlib import Path

# Add shared library to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared import ChatMessage, LLMProvider, MessageRole

from config import AgentHubConfig

logger = logging.getLogger(__name__)


WRITER_SYSTEM_PROMPT = """You are a writing specialist. Your job is to create clear, well-structured
written content.

Guidelines:
- Match tone to the requested format (formal for reports, conversational for blog posts)
- Use clear structure: introduction, body, conclusion where appropriate
- Keep sentences concise and vary their length
- Avoid jargon unless the audience expects it
- Ask clarifying questions if the request is vague about audience or tone"""


class WriterAgent:
    """Specialist agent for content creation.

    In production, this agent might have access to style guides,
    brand voice documents, and content templates.
    """

    name: str = "writer"
    description: str = "Creates written content like emails, summaries, reports, blog posts."

    def __init__(self, config: AgentHubConfig, provider: LLMProvider) -> None:
        self.config = config
        self.provider = provider

    async def handle(self, user_message: str, context: str | None = None) -> str:
        """Process a writing request and return the content.

        Args:
            user_message: The user's writing request.
            context: Optional context from prior routing or conversation.
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=WRITER_SYSTEM_PROMPT)
        ]

        if context:
            messages.append(
                ChatMessage(
                    role=MessageRole.SYSTEM, content=f"Context: {context}"
                )
            )

        messages.append(
            ChatMessage(role=MessageRole.USER, content=user_message)
        )

        response = await self.provider.chat(
            messages,
            model=self.config.agent_model,
            max_tokens=self.config.max_tokens_per_response,
            temperature=0.8,  # Higher temperature for creative writing
        )

        return response.content or "(No response)"
