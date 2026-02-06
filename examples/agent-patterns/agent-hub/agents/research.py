"""
Research specialist agent.

Handles factual questions, information lookup, and knowledge retrieval.
Each specialist agent has its own system prompt tuned for its domain.

From Chapter 6, Section 2: "Centralize control plane, distribute data
plane." The hub routes; this agent does the domain-specific work.

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


RESEARCH_SYSTEM_PROMPT = """You are a research specialist. Your job is to answer factual questions
accurately and thoroughly.

Guidelines:
- Cite sources when possible (or note when you cannot verify)
- Distinguish between established facts and your analysis
- If you are unsure, say so clearly rather than guessing
- Structure longer answers with clear sections
- Keep answers concise unless the user asks for detail"""


class ResearchAgent:
    """Specialist agent for research and information retrieval.

    In production, this agent would have access to search tools,
    knowledge bases, and RAG pipelines. This example demonstrates
    the agent interface pattern.
    """

    name: str = "research"
    description: str = "Finds information, answers factual questions, looks up data."

    def __init__(self, config: AgentHubConfig, provider: LLMProvider) -> None:
        self.config = config
        self.provider = provider

    async def handle(self, user_message: str, context: str | None = None) -> str:
        """Process a research request and return the answer.

        Args:
            user_message: The user's question or request.
            context: Optional context from prior routing or conversation.
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=RESEARCH_SYSTEM_PROMPT)
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
            temperature=0.3,  # Lower temperature for factual accuracy
        )

        return response.content or "(No response)"
