"""Capability manifest builder for the A2A discovery hub.

All service URLs are read from config so they can be swapped via env vars
without any code changes — critical for pointing at live Railway URLs after deploy.
"""

from __future__ import annotations

from typing import Any

from app.config import Settings


def build_capabilities(s: Settings) -> dict[str, Any]:
    """Build the full /v1/capabilities JSON manifest."""
    return {
        "version": "1.0",
        "provider": "Gary Edgington",
        "description": (
            "x402 micropayment task market — data transformation and validation pipeline. "
            "Each service accepts $0.005 USDC per call via x402 v2 on Base mainnet."
        ),
        "services": [
            {
                "id": "formatter",
                "name": "Data Formatter",
                "description": (
                    "Converts CSV to JSON, XML to JSON, or Markdown to HTML. "
                    "Optional self-validation: append ?validate=true to get { valid, errors[] } in response."
                ),
                "endpoint": f"{s.formatter_url}/v1/format",
                "method": "POST",
                "payment": {
                    "scheme": "x402",
                    "version": 2,
                    "network": "eip155:8453",
                    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                    "price_usd": 0.005,
                },
                "trial_endpoint": s.formatter_trial_url,
                "supported_conversions": [
                    {"from": "csv",      "to": "json"},
                    {"from": "xml",      "to": "json"},
                    {"from": "markdown", "to": "html"},
                ],
            },
            {
                "id": "schema-checker",
                "name": "JSON Schema Checker",
                "description": (
                    "Validates JSON payloads against JSON Schema Draft 7. "
                    "Returns valid/invalid with field-level error paths and optional repair suggestions."
                ),
                "endpoint": f"{s.schema_checker_url}/v1/schema-check",
                "method": "POST",
                "payment": {
                    "scheme": "x402",
                    "version": 2,
                    "network": "eip155:8453",
                    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                    "price_usd": 0.005,
                },
                "trial_endpoint": s.schema_checker_trial_url,
            },
        ],
    }


def build_well_known(s: Settings) -> dict[str, Any]:
    """Build the /.well-known/x402 discovery document."""
    return {
        "version": 2,
        "services": [
            {
                "endpoint": f"{s.formatter_url}/v1/format",
                "description": "Data format conversion — CSV/XML/Markdown to JSON/HTML with optional self-validation",
            },
            {
                "endpoint": f"{s.schema_checker_url}/v1/schema-check",
                "description": "JSON Schema validation with repair suggestions",
            },
        ],
    }


def build_llms_txt(s: Settings) -> str:
    """Build the /llms.txt LLM-readable capability description.

    Description quality directly affects Bazaar semantic search ranking —
    write to match agent query patterns, not developer documentation language.
    """
    return f"""\
# x402 Task Market

A collection of paid AI microservices using x402 micropayments on Base mainnet.
Each service costs $0.005 USDC per call via x402 v2.
Free trial endpoints available with size limits.

## Services

### Data Formatter
POST {s.formatter_url}/v1/format
Converts CSV to JSON, XML to JSON, or Markdown to HTML.
Append ?validate=true to receive structural validation: {{ valid, errors[] }}.
Trial (free, 32KB limit): {s.formatter_trial_url}

### JSON Schema Checker
POST {s.schema_checker_url}/v1/schema-check
Validates JSON payloads against JSON Schema Draft 7.
Returns {{ valid, errors[], suggested_payload }} with optional repair suggestions.
Trial (free, 32KB limit): {s.schema_checker_trial_url}

## Payment
All paid endpoints use x402 v2 on Base mainnet (eip155:8453).
USDC contract: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
Price: $0.005 USDC per call (5000 atomic units).
Receiving wallet: 0x8fC4006534801c17A3368075A1Fb3b3C511EdB1F

## Pipeline
Services chain naturally: CSV/XML/Markdown → Formatter → Schema-check (validator).
"""
