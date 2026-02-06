"""
AI metrics collection: latency, tokens, cost, and quality.

Collects the four categories of AI-specific metrics that the book
identifies as non-optional from day one. Traditional APM tools track
HTTP latency and error rates --- but AI workloads need token-level
cost tracking, model-specific latency percentiles, and quality signals
that don't exist in conventional software.

Without early tracking, AI costs grow faster than usage and you miss
optimization opportunities that compound over time.

Reference: Chapter 4 - The Infrastructure Stack ("Basic observability")
"""

import statistics
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MetricType(str, Enum):
    """Categories of AI-specific metrics."""
    LATENCY = "latency"
    TOKENS = "tokens"
    COST = "cost"
    QUALITY = "quality"


@dataclass
class AIMetricPoint:
    """A single metric data point."""
    timestamp: float
    metric_type: MetricType
    name: str
    value: float
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class RequestMetrics:
    """Metrics captured for a single AI request."""
    request_id: str
    model: str
    provider: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    timestamp: float = field(default_factory=time.time)
    quality_score: float | None = None
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class ModelStats:
    """Aggregate statistics for a single model."""
    model: str
    request_count: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    latencies_ms: list[float] = field(default_factory=list)
    quality_scores: list[float] = field(default_factory=list)

    @property
    def avg_latency_ms(self) -> float:
        return statistics.mean(self.latencies_ms) if self.latencies_ms else 0.0

    @property
    def p50_latency_ms(self) -> float:
        return statistics.median(self.latencies_ms) if self.latencies_ms else 0.0

    @property
    def p95_latency_ms(self) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_lats = sorted(self.latencies_ms)
        idx = int(len(sorted_lats) * 0.95)
        return sorted_lats[min(idx, len(sorted_lats) - 1)]

    @property
    def p99_latency_ms(self) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_lats = sorted(self.latencies_ms)
        idx = int(len(sorted_lats) * 0.99)
        return sorted_lats[min(idx, len(sorted_lats) - 1)]

    @property
    def avg_quality(self) -> float | None:
        return statistics.mean(self.quality_scores) if self.quality_scores else None

    @property
    def avg_cost_per_request(self) -> float:
        return self.total_cost_usd / self.request_count if self.request_count else 0.0

    @property
    def tokens_per_request(self) -> float:
        total = self.total_input_tokens + self.total_output_tokens
        return total / self.request_count if self.request_count else 0.0


class AIMetricsCollector:
    """
    Collect and aggregate AI-specific metrics.

    Tracks four metric categories:
    - **Latency**: Per-model response times with percentile breakdowns
    - **Tokens**: Input/output token counts per model and per key
    - **Cost**: Per-request and aggregate spend tracking
    - **Quality**: Optional quality scores for response evaluation

    In production, export these to your observability stack (Datadog,
    Prometheus, Helicone, Langfuse, etc.). This example stores in
    memory for demonstration.

    Usage:
        collector = AIMetricsCollector()

        # Record a completed request
        collector.record_request(RequestMetrics(
            request_id="req-123",
            model="gpt-4o-mini",
            provider="openai",
            latency_ms=1234.5,
            input_tokens=500,
            output_tokens=200,
            total_tokens=700,
            cost_usd=0.000195,
            quality_score=0.92,
            tags={"feature": "search", "team": "product"},
        ))

        # Get model-level stats
        stats = collector.get_model_stats("gpt-4o-mini")
        print(f"p95 latency: {stats.p95_latency_ms:.0f}ms")
        print(f"avg cost/req: ${stats.avg_cost_per_request:.6f}")

        # Get cost breakdown
        breakdown = collector.cost_breakdown()
    """

    def __init__(self) -> None:
        self._requests: list[RequestMetrics] = []
        self._model_stats: dict[str, ModelStats] = {}
        self._tag_costs: dict[str, float] = {}

    def record_request(self, metrics: RequestMetrics) -> None:
        """Record metrics for a completed AI request."""
        self._requests.append(metrics)

        # Update model-level aggregates
        if metrics.model not in self._model_stats:
            self._model_stats[metrics.model] = ModelStats(model=metrics.model)

        stats = self._model_stats[metrics.model]
        stats.request_count += 1
        stats.total_input_tokens += metrics.input_tokens
        stats.total_output_tokens += metrics.output_tokens
        stats.total_cost_usd += metrics.cost_usd
        stats.latencies_ms.append(metrics.latency_ms)

        if metrics.quality_score is not None:
            stats.quality_scores.append(metrics.quality_score)

        # Track cost by tags (feature, team, etc.)
        for key, value in metrics.tags.items():
            tag_key = f"{key}:{value}"
            self._tag_costs[tag_key] = self._tag_costs.get(tag_key, 0.0) + metrics.cost_usd

    def get_model_stats(self, model: str) -> ModelStats:
        """Get aggregate statistics for a specific model."""
        return self._model_stats.get(model, ModelStats(model=model))

    def get_all_model_stats(self) -> dict[str, ModelStats]:
        """Get statistics for all models."""
        return dict(self._model_stats)

    def cost_breakdown(self) -> dict[str, Any]:
        """
        Break down cost by model and by tags.

        This is the view your CFO needs: where is the AI spend going,
        broken down by model, by feature, by team.
        """
        by_model = {
            model: stats.total_cost_usd
            for model, stats in self._model_stats.items()
        }
        total = sum(by_model.values())

        return {
            "total_cost_usd": total,
            "by_model": by_model,
            "by_tag": dict(self._tag_costs),
            "request_count": sum(s.request_count for s in self._model_stats.values()),
        }

    def latency_summary(self) -> dict[str, dict[str, float]]:
        """Per-model latency percentiles."""
        summary: dict[str, dict[str, float]] = {}
        for model, stats in self._model_stats.items():
            summary[model] = {
                "avg_ms": stats.avg_latency_ms,
                "p50_ms": stats.p50_latency_ms,
                "p95_ms": stats.p95_latency_ms,
                "p99_ms": stats.p99_latency_ms,
                "count": stats.request_count,
            }
        return summary

    def export_points(self) -> list[AIMetricPoint]:
        """
        Export all current stats as metric points.

        In production, push these to Prometheus, Datadog, or your
        preferred metrics backend on a regular interval.
        """
        now = time.time()
        points: list[AIMetricPoint] = []

        for model, stats in self._model_stats.items():
            tags = {"model": model}
            points.extend([
                AIMetricPoint(now, MetricType.LATENCY, "ai.latency.p50", stats.p50_latency_ms, tags),
                AIMetricPoint(now, MetricType.LATENCY, "ai.latency.p95", stats.p95_latency_ms, tags),
                AIMetricPoint(now, MetricType.LATENCY, "ai.latency.p99", stats.p99_latency_ms, tags),
                AIMetricPoint(now, MetricType.TOKENS, "ai.tokens.input.total", float(stats.total_input_tokens), tags),
                AIMetricPoint(now, MetricType.TOKENS, "ai.tokens.output.total", float(stats.total_output_tokens), tags),
                AIMetricPoint(now, MetricType.COST, "ai.cost.total", stats.total_cost_usd, tags),
                AIMetricPoint(now, MetricType.COST, "ai.cost.per_request", stats.avg_cost_per_request, tags),
            ])
            if stats.avg_quality is not None:
                points.append(
                    AIMetricPoint(now, MetricType.QUALITY, "ai.quality.avg", stats.avg_quality, tags)
                )

        return points


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo() -> None:
    """Demonstrate AI metrics collection and aggregation."""
    import random

    collector = AIMetricsCollector()
    print("=== AI Metrics Demo ===\n")

    # Simulate 50 requests across two models (via OpenRouter)
    # Pricing per 1K tokens (input, output) — verify at openrouter.ai/models
    models = [
        ("google/gemini-2.5-flash", "openrouter", 0.00015, 0.0006),
        ("anthropic/claude-sonnet-4.5", "openrouter", 0.003, 0.015),
    ]
    features = ["search", "summarize", "chat"]

    for i in range(50):
        model, provider, input_price, output_price = random.choice(models)
        input_tokens = random.randint(100, 2000)
        output_tokens = random.randint(50, 1000)
        cost = (input_tokens / 1000) * input_price + (output_tokens / 1000) * output_price
        latency = random.uniform(200, 3000)
        quality = random.uniform(0.7, 1.0)

        collector.record_request(RequestMetrics(
            request_id=f"req-{i:03d}",
            model=model,
            provider=provider,
            latency_ms=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost_usd=cost,
            quality_score=quality,
            tags={"feature": random.choice(features), "team": "product"},
        ))

    # Show results
    print("--- Cost Breakdown ---")
    breakdown = collector.cost_breakdown()
    print(f"Total cost: ${breakdown['total_cost_usd']:.4f}")
    print(f"Requests:   {breakdown['request_count']}")
    for model, cost in breakdown["by_model"].items():
        print(f"  {model}: ${cost:.4f}")
    print()

    print("--- Latency Summary ---")
    for model, lat in collector.latency_summary().items():
        print(f"  {model}:")
        print(f"    p50={lat['p50_ms']:.0f}ms  p95={lat['p95_ms']:.0f}ms  p99={lat['p99_ms']:.0f}ms")
    print()

    print("--- Cost by Tag ---")
    for tag, cost in breakdown["by_tag"].items():
        print(f"  {tag}: ${cost:.4f}")


if __name__ == "__main__":
    demo()
