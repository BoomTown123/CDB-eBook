"""
Data analysis specialist agent.

Handles data analysis, metric computation, trend identification,
and comparisons. Uses low temperature for precision.

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


ANALYST_SYSTEM_PROMPT = """You are a data analysis specialist. Your job is to analyze data, compute
metrics, identify trends, and provide quantitative insights.

Guidelines:
- Be precise with numbers; do not round unless asked
- Show your reasoning step by step
- Distinguish between correlation and causation
- Present findings in structured format (tables, bullet points)
- Flag data quality issues or insufficient data
- When comparing, state the basis of comparison clearly"""


class AnalystAgent:
    """Specialist agent for data analysis.

    In production, this agent would have access to databases, analytics
    APIs, and computation tools (pandas, SQL, etc.).
    """

    name: str = "analyst"
    description: str = "Analyzes data, computes metrics, compares numbers, identifies trends."

    def __init__(self, config: AgentHubConfig, provider: LLMProvider) -> None:
        self.config = config
        self.provider = provider

    async def handle(self, user_message: str, context: str | None = None) -> str:
        """Process an analysis request and return findings.

        Args:
            user_message: The user's analysis request.
            context: Optional context from prior routing or conversation.
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=ANALYST_SYSTEM_PROMPT)
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
            temperature=0.2,  # Low temperature for analytical precision
        )

        return response.content or "(No response)"
