"""
Structured logging middleware for the AI Gateway.

Emits JSON-structured log lines for every request flowing through the
gateway. Structured logs (not print statements, not unstructured text)
are the foundation of AI observability: you cannot optimize what you
cannot query.

Reference: Chapter 4 - The Infrastructure Stack
"""

import json
import logging
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class GatewayLogEntry:
    """A single structured log line for a gateway request."""
    timestamp: str
    level: str
    event: str
    request_id: str = ""
    key_id: str = ""
    provider: str = ""
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    status: str = "ok"
    error: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


class StructuredFormatter(logging.Formatter):
    """Emit log records as single-line JSON."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Merge any extra structured fields attached to the record
        if hasattr(record, "structured"):
            entry.update(record.structured)  # type: ignore[attr-defined]

        return json.dumps(entry, default=str)


def configure_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up structured JSON logging for the gateway.

    Call this once at startup. Every logger under 'ai_gateway' will
    emit JSON to stdout --- ready for ingestion by any log aggregator
    (Datadog, ELK, CloudWatch, etc.).

    Usage:
        logger = configure_logging("INFO")
        logger.info("Gateway started", extra={"structured": {"port": 8000}})
    """
    logger = logging.getLogger("ai_gateway")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)

    return logger


class GatewayLogger:
    """
    High-level logging helper for gateway request lifecycle.

    Wraps Python's logging module with gateway-specific methods that
    produce consistent structured output. Use this instead of calling
    logger.info() directly to ensure every request has the same fields.

    Usage:
        gw_logger = GatewayLogger()
        gw_logger.log_request(request_id="req-123", key_id="key-001", model="gpt-4o")
        gw_logger.log_response(
            request_id="req-123",
            provider="openai",
            model="gpt-4o",
            input_tokens=500,
            output_tokens=200,
            latency_ms=1234.5,
            cost_usd=0.0032,
        )
    """

    def __init__(self, level: str = "INFO") -> None:
        self._logger = configure_logging(level)

    def log_request(
        self,
        request_id: str,
        key_id: str,
        model: str,
        **extra: Any,
    ) -> None:
        """Log an incoming request before it reaches the provider."""
        entry = GatewayLogEntry(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            level="INFO",
            event="request.received",
            request_id=request_id,
            key_id=key_id,
            model=model,
            extra=extra,
        )
        self._logger.info(
            "request.received",
            extra={"structured": asdict(entry)},
        )

    def log_response(
        self,
        request_id: str,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        cost_usd: float,
        **extra: Any,
    ) -> None:
        """Log a completed response after the provider returns."""
        entry = GatewayLogEntry(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            level="INFO",
            event="request.completed",
            request_id=request_id,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            extra=extra,
        )
        self._logger.info(
            "request.completed",
            extra={"structured": asdict(entry)},
        )

    def log_error(
        self,
        request_id: str,
        error: str,
        provider: str = "",
        model: str = "",
        **extra: Any,
    ) -> None:
        """Log a failed request."""
        entry = GatewayLogEntry(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            level="ERROR",
            event="request.failed",
            request_id=request_id,
            provider=provider,
            model=model,
            status="error",
            error=error,
            extra=extra,
        )
        self._logger.error(
            "request.failed",
            extra={"structured": asdict(entry)},
        )
