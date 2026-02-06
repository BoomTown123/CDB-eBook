"""
Intent classification and routing logic for the agent hub.

The router is the hub's decision layer. It classifies user intent and
routes to the appropriate specialist agent. Uses a fast, cheap model
for routing decisions (not the full agent model).

From Chapter 6, Section 2: "The hub decides what agents can do;
agents decide how to do it."

Book reference: Chapter 6, Section 2 - The Agent Hub Pattern
"""

import json
import logging
import sys
from pathlib import Path

# Add shared library to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared import ChatMessage, LLMProvider, MessageRole
from shared.llm_exceptions import LLMException

from config import AgentHubConfig

logger = logging.getLogger(__name__)


ROUTING_PROMPT = """You are a request router. Classify the user's request and route it to the correct specialist agent.

Available agents:
- research: Finds information, answers factual questions, looks up data. Use for "what is", "find", "look up", "how does" requests.
- writer: Creates written content like emails, summaries, reports, blog posts. Use for "write", "draft", "compose", "summarize" requests.
- analyst: Analyzes data, computes metrics, compares numbers, identifies trends. Use for "analyze", "compare", "calculate", "what trends" requests.

Respond with JSON only:
{
    "agent": "research|writer|analyst",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}

If the request does not clearly match any agent, route to "research" with low confidence."""


class Router:
    """Routes user requests to specialist agents.

    The router uses a smaller, faster model than the specialist agents.
    Routing should be near-instant so the user does not wait for the
    classification step.
    """

    def __init__(self, config: AgentHubConfig, provider: LLMProvider) -> None:
        self.config = config
        self.provider = provider

    async def classify(self, user_message: str) -> dict:
        """Classify user intent and select a specialist agent.

        Returns:
            dict with keys: agent (str), confidence (float), reasoning (str)
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=ROUTING_PROMPT),
            ChatMessage(role=MessageRole.USER, content=user_message),
        ]

        try:
            response = await self.provider.chat(
                messages,
                model=self.config.router_model,
                max_tokens=200,
                temperature=0.0,  # Deterministic routing
            )
            content = response.content or "{}"
        except LLMException as exc:
            logger.error("Router LLM call failed: %s", exc)
            content = "{}"

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from response if model wrapped it
            result = {
                "agent": "research",
                "confidence": 0.0,
                "reasoning": "Failed to parse routing response.",
            }

        # Validate the selected agent
        selected = result.get("agent", "research")
        if selected not in self.config.available_agents:
            result["agent"] = "research"
            result["confidence"] = 0.0
            result["reasoning"] = (
                f"Unknown agent '{selected}', defaulting to research."
            )

        return result

    async def route(self, user_message: str) -> tuple[str, float, str]:
        """Classify and return (agent_name, confidence, reasoning).

        Retries classification if confidence is very low, up to
        max_routing_retries times.
        """
        best_result = None

        for attempt in range(self.config.max_routing_retries + 1):
            result = await self.classify(user_message)
            confidence = result.get("confidence", 0.0)

            if best_result is None or confidence > best_result.get(
                "confidence", 0.0
            ):
                best_result = result

            if confidence >= 0.7:
                break  # Confident enough

        agent = best_result.get("agent", "research")
        confidence = best_result.get("confidence", 0.0)
        reasoning = best_result.get("reasoning", "")

        return agent, confidence, reasoning
