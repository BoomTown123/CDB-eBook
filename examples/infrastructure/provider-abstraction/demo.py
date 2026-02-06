#!/usr/bin/env python3
"""Demo: Same prompt, different providers.

Shows how the provider abstraction lets you switch models
without changing your application code.

Usage:
    # Default (OpenRouter)
    python demo.py

    # Specific provider
    python demo.py --provider openai

    # Compare both providers side-by-side
    python demo.py --compare

    # Custom prompt
    python demo.py --prompt "Explain microservices in one sentence."

    # Verbose logging
    python demo.py --compare -v
"""

import argparse
import asyncio
import logging
import sys
import time
from pathlib import Path

# Load .env file if present (for local development)
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenv is optional; env vars can be set directly

from factory import get_provider, get_default_provider_name, list_available_providers
from providers import Message

logger = logging.getLogger(__name__)

# ── Default prompt ──────────────────────────────────────────────────
DEFAULT_PROMPT = (
    "What are the three most important things to consider when building "
    "an AI-first company? Answer in 2-3 concise sentences."
)

# ── Display helpers ─────────────────────────────────────────────────

SEPARATOR = "-" * 60


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_result(provider_name: str, response, elapsed: float) -> None:
    """Print a formatted result from a single provider."""
    print(f"\n{SEPARATOR}")
    print(f"  Provider : {provider_name}")
    print(f"  Model    : {response.model}")
    print(f"  Tokens   : {response.tokens_used}")
    print(f"  Time     : {elapsed:.2f}s")
    print(SEPARATOR)
    print()
    print(response.content)
    print()


# ── Core logic ──────────────────────────────────────────────────────

async def run_single(provider_name: str, prompt: str) -> None:
    """Run the prompt through a single provider and display the result."""
    print_header(f"Provider: {provider_name}")

    try:
        provider = get_provider(provider_name)
    except ValueError as exc:
        print(f"\n  Error: {exc}")
        sys.exit(1)

    messages = [
        Message(role="system", content="You are a helpful, concise advisor for technology leaders."),
        Message(role="user", content=prompt),
    ]

    print(f"\n  Prompt: {prompt}")
    print(f"\n  Sending request to {provider_name}...")

    start = time.perf_counter()
    try:
        response = await provider.complete(messages, temperature=0.7, max_tokens=300)
    except Exception as exc:
        print(f"\n  Request failed: {exc}")
        sys.exit(1)
    elapsed = time.perf_counter() - start

    print_result(provider_name, response, elapsed)


async def run_compare(prompt: str) -> None:
    """Run the same prompt through all available providers and compare.

    This is the key demonstration: the exact same application code
    (same messages, same parameters) works with any provider.
    """
    print_header("Provider Comparison")
    print(f"\n  Prompt: {prompt}")
    print(f"\n  Sending the same prompt to all available providers...\n")

    available = list_available_providers()
    results: list[tuple[str, object, float]] = []
    errors: list[tuple[str, str]] = []

    for name in available:
        try:
            provider = get_provider(name)
        except ValueError as exc:
            errors.append((name, str(exc)))
            continue

        messages = [
            Message(role="system", content="You are a helpful, concise advisor for technology leaders."),
            Message(role="user", content=prompt),
        ]

        print(f"  [{name}] Sending request...")
        start = time.perf_counter()
        try:
            response = await provider.complete(messages, temperature=0.7, max_tokens=300)
            elapsed = time.perf_counter() - start
            results.append((name, response, elapsed))
        except Exception as exc:
            elapsed = time.perf_counter() - start
            errors.append((name, f"{exc} ({elapsed:.2f}s)"))
            print(f"  [{name}] Failed: {exc}")

    # Display results
    for name, response, elapsed in results:
        print_result(name, response, elapsed)

    # Summary table
    if results:
        print_header("Summary")
        print(f"\n  {'Provider':<15} {'Model':<35} {'Tokens':>8} {'Time':>8}")
        print(f"  {'-' * 15} {'-' * 35} {'-' * 8} {'-' * 8}")
        for name, response, elapsed in results:
            print(
                f"  {name:<15} {response.model:<35} {response.tokens_used:>8} {elapsed:>7.2f}s"
            )
        print()

    if errors:
        print("\n  Providers that failed:")
        for name, err in errors:
            print(f"    - {name}: {err}")
        print()

    # The lesson
    if len(results) >= 2:
        print(SEPARATOR)
        print("  KEY INSIGHT: The application code was identical for every")
        print("  provider. Only the factory argument changed. This is the")
        print("  provider abstraction pattern in action.")
        print(SEPARATOR)
        print()


# ── CLI entry point ─────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Demo: Provider abstraction pattern for LLM APIs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python demo.py                          # Use default provider (OpenRouter)
  python demo.py --provider openai        # Use OpenAI directly
  python demo.py --compare                # Compare all providers
  python demo.py --compare --prompt "Explain RAG in one sentence."
        """,
    )
    parser.add_argument(
        "--provider",
        default=None,
        help=f"Provider to use. Available: {', '.join(list_available_providers())}. "
        f"Default: auto-detected from env vars.",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run the prompt through ALL available providers and compare results.",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Custom prompt to send. Defaults to a question about AI-first companies.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (shows HTTP requests, timing details).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Configure logging
    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    print("\n  Provider Abstraction Pattern -- Demo")
    print("  From: Blueprint for an AI-First Company, Chapter 4\n")

    if args.compare:
        asyncio.run(run_compare(args.prompt))
    else:
        provider_name = args.provider or get_default_provider_name()
        asyncio.run(run_single(provider_name, args.prompt))


if __name__ == "__main__":
    main()
