"""
Cost tracking middleware for the AI Gateway.

Tracks per-request and per-key cost based on token usage and model
pricing. This is the "basic observability" the book flags as non-optional
on day one: without early cost tracking, AI spend grows faster than
usage and you miss optimization opportunities that compound over time.

Reference: Chapter 4 - The Infrastructure Stack (Day 1 requirements)
"""

import time
from dataclasses import dataclass, field


# Per-1K-token pricing --- mirrors config.yaml. In production, load
# these from config or a pricing API so updates don't require code changes.
DEFAULT_PRICING: dict[str, dict[str, float]] = {
    "gpt-4o":                     {"input": 0.0025,  "output": 0.01},
    "gpt-4o-mini":                {"input": 0.00015, "output": 0.0006},
    "o3-mini":                    {"input": 0.0011,  "output": 0.0044},
    "claude-opus-4-5-20251101":   {"input": 0.015,   "output": 0.075},
    "claude-sonnet-4-20250514":   {"input": 0.003,   "output": 0.015},
    "claude-haiku-3-5-20241022":  {"input": 0.0008,  "output": 0.004},
}


@dataclass
class RequestCost:
    """Cost breakdown for a single request."""
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class KeyUsageSummary:
    """Aggregate cost summary for an API key."""
    key_id: str
    total_requests: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    costs_by_model: dict[str, float] = field(default_factory=dict)


class CostTracker:
    """
    Track AI spend per request and per API key.

    Every request that flows through the gateway gets a cost estimate
    based on token counts and model pricing. This data feeds dashboards,
    alerts, and budget controls.

    Usage:
        tracker = CostTracker()
        cost = tracker.record(
            key_id="key-std-001",
            model="gpt-4o-mini",
            input_tokens=500,
            output_tokens=200,
        )
        print(f"Request cost: ${cost.total_cost:.6f}")

        summary = tracker.get_summary("key-std-001")
        print(f"Total spend: ${summary.total_cost:.4f}")
    """

    def __init__(
        self,
        pricing: dict[str, dict[str, float]] | None = None,
    ) -> None:
        self._pricing = pricing or DEFAULT_PRICING
        self._records: dict[str, list[RequestCost]] = {}

    def _cost_for_tokens(
        self, model: str, input_tokens: int, output_tokens: int
    ) -> tuple[float, float]:
        """Calculate input and output cost for a given model and token count."""
        prices = self._pricing.get(model, {"input": 0.0, "output": 0.0})
        input_cost = (input_tokens / 1000) * prices["input"]
        output_cost = (output_tokens / 1000) * prices["output"]
        return input_cost, output_cost

    def record(
        self,
        key_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> RequestCost:
        """
        Record a completed request and return its cost breakdown.

        Call this from the gateway after every successful completion,
        regardless of provider. The cost tracker doesn't care which
        provider served the request --- only which model and how many tokens.
        """
        input_cost, output_cost = self._cost_for_tokens(
            model, input_tokens, output_tokens
        )

        cost = RequestCost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=input_cost + output_cost,
        )

        if key_id not in self._records:
            self._records[key_id] = []
        self._records[key_id].append(cost)

        return cost

    def get_summary(self, key_id: str) -> KeyUsageSummary:
        """Aggregate cost data for a single key."""
        records = self._records.get(key_id, [])
        summary = KeyUsageSummary(key_id=key_id)

        for rec in records:
            summary.total_requests += 1
            summary.total_input_tokens += rec.input_tokens
            summary.total_output_tokens += rec.output_tokens
            summary.total_cost += rec.total_cost
            summary.costs_by_model[rec.model] = (
                summary.costs_by_model.get(rec.model, 0.0) + rec.total_cost
            )

        return summary

    def get_all_summaries(self) -> list[KeyUsageSummary]:
        """Return usage summaries for every tracked key."""
        return [self.get_summary(key_id) for key_id in self._records]

    def total_spend(self) -> float:
        """Total spend across all keys --- the number your CFO cares about."""
        return sum(s.total_cost for s in self.get_all_summaries())
