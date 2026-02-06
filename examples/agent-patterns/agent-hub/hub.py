"""
Agent Hub - Central orchestrator that routes requests to specialist agents.

Demonstrates the Agent Hub pattern from Chapter 6, Section 2:
- Centralized routing: one entry point classifies and dispatches
- Distributed execution: specialist agents do the domain work
- Unified observability: the hub logs every routing decision
- Control plane / data plane separation

The hub handles: routing, permissions, observability, rate limiting.
The agents handle: domain logic, response generation.

Two-model architecture:
- Router uses a cheap/fast model (e.g. Gemini Flash) for intent classification
- Agents use a capable model (e.g. Claude Sonnet) for execution
Both models go through OpenRouter -- only the model ID differs.

Run:
    python hub.py

Book reference: Chapter 6, Section 2 - The Agent Hub Pattern
"""

import asyncio
import json
import logging
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

# Add shared library to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared import get_provider
from shared.llm_exceptions import LLMException

from config import AgentHubConfig
from router import Router
from agents.research import ResearchAgent
from agents.writer import WriterAgent
from agents.analyst import AnalystAgent

logger = logging.getLogger(__name__)


@dataclass
class RoutingLog:
    """Record of a routing decision for observability."""

    user_message: str
    selected_agent: str
    confidence: float
    reasoning: str
    response_time_ms: float
    timestamp: float = field(default_factory=time.time)


class AgentHub:
    """Central hub that routes user requests to specialist agents.

    From Chapter 6, Section 2:
    "The Agent Hub is a control plane for AI agents -- architecturally
    similar to an API gateway, service mesh, or Kubernetes control plane.
    Same separation of concerns: centralized policy, distributed execution."

    Six responsibilities:
    1. Permission management (simplified here)
    2. Unified observability (routing logs)
    3. Lifecycle management (agent initialization)
    4. Tool registry (agent registry)
    5. Rate limiting (request counting)
    6. Circuit breakers (error tracking)
    """

    def __init__(self, config: AgentHubConfig) -> None:
        self.config = config

        # Create two provider instances: cheap model for routing,
        # capable model for agent execution. Both go through the same
        # provider (OpenRouter) -- only the model ID differs.
        router_provider = get_provider(
            provider_name=config.provider_name,
            model=config.router_model,
            api_key=config.api_key,
        )
        agent_provider = get_provider(
            provider_name=config.provider_name,
            model=config.agent_model,
            api_key=config.api_key,
        )

        self.router = Router(config, router_provider)

        # Initialize specialist agents (lifecycle management)
        self.agents: dict[str, ResearchAgent | WriterAgent | AnalystAgent] = {
            "research": ResearchAgent(config, agent_provider),
            "writer": WriterAgent(config, agent_provider),
            "analyst": AnalystAgent(config, agent_provider),
        }

        # Observability
        self.routing_log: list[RoutingLog] = []

        # Rate limiting (simple counter)
        self._request_count: int = 0
        self._max_requests_per_session: int = config.rate_limit

        # Circuit breaker (simple error counter per agent)
        self._error_counts: dict[str, int] = {name: 0 for name in self.agents}
        self._circuit_breaker_threshold: int = config.circuit_breaker_threshold

    async def handle_request(self, user_message: str) -> str:
        """Route a user request to the appropriate specialist agent.

        Workflow:
        1. Check rate limit
        2. Classify intent via router (cheap model)
        3. Check circuit breaker for selected agent
        4. Dispatch to specialist agent (capable model)
        5. Log the routing decision
        6. Return the response
        """
        # Rate limiting
        self._request_count += 1
        if self._request_count > self._max_requests_per_session:
            return "[Hub] Rate limit exceeded. Please try again later."

        # Route the request (cheap model)
        start_time = time.time()
        agent_name, confidence, reasoning = await self.router.route(
            user_message
        )
        routing_time_ms = (time.time() - start_time) * 1000

        print(
            f"  [Hub] Routed to '{agent_name}' "
            f"(confidence: {confidence:.2f}, {routing_time_ms:.0f}ms)"
        )
        print(f"  [Hub] Reasoning: {reasoning}")

        # Circuit breaker check
        if (
            self._error_counts.get(agent_name, 0)
            >= self._circuit_breaker_threshold
        ):
            fallback = "research" if agent_name != "research" else "writer"
            print(
                f"  [Hub] Circuit breaker OPEN for '{agent_name}'. "
                f"Falling back to '{fallback}'."
            )
            agent_name = fallback

        # Dispatch to specialist agent (capable model)
        agent = self.agents.get(agent_name)
        if not agent:
            return f"[Hub] Agent '{agent_name}' not available."

        try:
            response = await agent.handle(user_message)
            # Reset error count on success
            self._error_counts[agent_name] = 0
        except LLMException as exc:
            self._error_counts[agent_name] = (
                self._error_counts.get(agent_name, 0) + 1
            )
            logger.error("Agent '%s' LLM error: %s", agent_name, exc)
            return (
                f"[Hub] The {agent_name} agent encountered an error. "
                "Please try again."
            )
        except Exception as exc:
            self._error_counts[agent_name] = (
                self._error_counts.get(agent_name, 0) + 1
            )
            logger.error("Agent '%s' error: %s", agent_name, exc)
            return (
                f"[Hub] The {agent_name} agent encountered an error. "
                "Please try again."
            )

        # Log routing decision (unified observability)
        self.routing_log.append(
            RoutingLog(
                user_message=user_message[:200],
                selected_agent=agent_name,
                confidence=confidence,
                reasoning=reasoning,
                response_time_ms=routing_time_ms,
            )
        )

        return response

    def get_observability_summary(self) -> dict:
        """Return a summary of hub activity for dashboards."""
        agent_counts: dict[str, int] = {}
        total_routing_time = 0.0

        for log in self.routing_log:
            agent_counts[log.selected_agent] = (
                agent_counts.get(log.selected_agent, 0) + 1
            )
            total_routing_time += log.response_time_ms

        avg_routing_time = (
            total_routing_time / len(self.routing_log)
            if self.routing_log
            else 0
        )

        return {
            "total_requests": self._request_count,
            "requests_by_agent": agent_counts,
            "avg_routing_time_ms": round(avg_routing_time, 1),
            "circuit_breaker_status": {
                name: (
                    "OPEN"
                    if count >= self._circuit_breaker_threshold
                    else "CLOSED"
                )
                for name, count in self._error_counts.items()
            },
            "router_model": self.config.router_model,
            "agent_model": self.config.agent_model,
        }


async def async_main() -> None:
    """Run the agent hub in interactive mode.

    The hub acts as the single entry point. Users interact with the hub,
    not directly with specialist agents.
    """
    try:
        config = AgentHubConfig.from_env()
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)

    hub = AgentHub(config)

    print("Agent Hub ready. Type 'quit' to exit, 'status' for hub metrics.")
    print(
        f"Router model: {config.router_model} | "
        f"Agent model: {config.agent_model}"
    )
    print(f"Provider: {config.provider_name}")
    print(f"Available agents: {', '.join(config.available_agents)}")
    print("-" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("\nHub summary:")
            print(json.dumps(hub.get_observability_summary(), indent=2))
            print("Goodbye.")
            break

        if user_input.lower() == "status":
            print(json.dumps(hub.get_observability_summary(), indent=2))
            continue

        response = await hub.handle_request(user_input)
        print(f"\nAgent: {response}")


def main() -> None:
    """Entry point -- run the async main loop."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
