"""Capability manifest builder for the A2A discovery hub.

All service URLs are read from config so they can be swapped via env vars
without any code changes -- critical for pointing at live Railway URLs after deploy.
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
            "x402 micropayment task market -- data transformation, validation, and classification pipeline. "
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
            {
                "id": "classifier",
                "name": "Content Classifier",
                "description": (
                    "Classifies text or JSON input into a label with a confidence score using Claude AI. "
                    "Supports five presets: sentiment, topic, intent, urgency, and custom taxonomies. "
                    "Returns a ranked label list and optional reasoning."
                ),
                "endpoint": f"{s.classifier_url}/v1/classify",
                "method": "POST",
                "payment": {
                    "scheme": "x402",
                    "version": 2,
                    "network": "eip155:8453",
                    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                    "price_usd": 0.005,
                },
                "trial_endpoint": s.classifier_trial_url,
                "supported_presets": ["sentiment", "topic", "intent", "urgency", "custom"],
            },
            {
                "id": "summarizer",
                "name": "Text Summarizer",
                "description": (
                    "Compresses text, Markdown, or JSON to a structured summary using Claude AI. "
                    "Supports four output formats (prose, bullets, headline, tldr) and three length presets "
                    "(brief ~30 words, medium ~80 words, detailed ~200 words), "
                    "with an optional exact target word count. "
                    "Returns summary, word count, compression ratio, and optional omission notes."
                ),
                "endpoint": f"{s.summarizer_url}/v1/summarize",
                "method": "POST",
                "payment": {
                    "scheme": "x402",
                    "version": 2,
                    "network": "eip155:8453",
                    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                    "price_usd": 0.005,
                },
                "trial_endpoint": s.summarizer_trial_url,
                "supported_formats": ["prose", "bullets", "headline", "tldr"],
                "supported_lengths": ["brief", "medium", "detailed"],
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
                "description": "Data format conversion -- CSV/XML/Markdown to JSON/HTML with optional self-validation",
            },
            {
                "endpoint": f"{s.schema_checker_url}/v1/schema-check",
                "description": "JSON Schema validation with repair suggestions",
            },
            {
                "endpoint": f"{s.classifier_url}/v1/classify",
                "description": "AI-powered content classification -- sentiment, topic, intent, urgency, or custom taxonomy",
            },
            {
                "endpoint": f"{s.summarizer_url}/v1/summarize",
                "description": "AI-powered text summarization -- prose, bullets, headline, or TL;DR at brief/medium/detailed length",
            },
        ],
    }


def build_llms_txt(s: Settings) -> str:
    """Build the /llms.txt LLM-readable capability description."""
    return (
        "# x402 Task Market\n\n"
        "A collection of paid AI microservices using x402 micropayments on Base mainnet.\n"
        "Each service costs $0.005 USDC per call via x402 v2.\n"
        "Free trial endpoints available with size limits.\n\n"
        "## Services\n\n"
        "### Data Formatter\n"
        f"POST {s.formatter_url}/v1/format\n"
        "Converts CSV to JSON, XML to JSON, or Markdown to HTML.\n"
        "Append ?validate=true to receive structural validation: { valid, errors[] }.\n"
        f"Trial (free, 32KB limit): {s.formatter_trial_url}\n\n"
        "### JSON Schema Checker\n"
        f"POST {s.schema_checker_url}/v1/schema-check\n"
        "Validates JSON payloads against JSON Schema Draft 7.\n"
        "Returns { valid, errors[], suggested_payload } with optional repair suggestions.\n"
        f"Trial (free, 32KB limit): {s.schema_checker_trial_url}\n\n"
        "### Content Classifier\n"
        f"POST {s.classifier_url}/v1/classify\n"
        "Classifies text or JSON input using Claude AI. Presets: sentiment, topic, intent, urgency, custom.\n"
        "Returns label, confidence score, ranked label list, and optional reasoning.\n"
        f"Trial (free, 4KB limit, sentiment/topic only): {s.classifier_trial_url}\n\n"
        "### Text Summarizer\n"
        f"POST {s.summarizer_url}/v1/summarize\n"
        "Compresses text, Markdown, or JSON to a structured summary using Claude AI.\n"
        "Formats: prose (paragraph), bullets (list), headline (one sentence), tldr (TL;DR prefix).\n"
        "Length presets: brief (~30 words), medium (~80 words), detailed (~200 words).\n"
        "Optional target_words (1-500) overrides the length preset.\n"
        "Set explain=true to receive a notes field describing what was omitted.\n"
        "Returns summary, format, word_count, compression_ratio, and optional notes.\n"
        f"Trial (free, 4KB limit, prose format only, brief/medium only): {s.summarizer_trial_url}\n\n"
        "## Payment\n"
        "All paid endpoints use x402 v2 on Base mainnet (eip155:8453).\n"
        "USDC contract: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\n"
        "Price: $0.005 USDC per call (5000 atomic units).\n"
        "Receiving wallet: 0x8fC4006534801c17A3368075A1Fb3b3C511EdB1F\n\n"
        "## Pipeline\n"
        "Services chain naturally: raw input -> Formatter -> Schema-check -> Classifier -> Summarizer.\n"
        "Discovery: GET https://project-a2a-production.up.railway.app/v1/capabilities\n"
    )
