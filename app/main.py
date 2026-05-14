from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from app.config import get_settings
from app.manifest import build_capabilities, build_well_known, build_llms_txt
from app.telemetry import request_logging_middleware

settings = get_settings()
APP_VERSION = settings.app_version

app = FastAPI(
    title="x402 A2A Discovery Hub",
    version=APP_VERSION,
    description="Neutral discovery hub for the x402 task market. Points to all services via capabilities manifest, .well-known, and llms.txt.",
)

if settings.log_requests:
    app.middleware("http")(request_logging_middleware)

# Phase 4c: MCP channel
from app.mcp_server import mcp as _mcp_server
app.mount("/mcp", _mcp_server.sse_app())


@app.api_route("/health", methods=["GET", "HEAD"])
def health() -> dict:
    return {"status": "ok", "service": "a2a-hub", "version": APP_VERSION}


@app.get("/v1/capabilities")
def capabilities() -> dict:
    """Full capability manifest — one entry per live service."""
    return build_capabilities(get_settings())


@app.get("/.well-known/x402")
def well_known_x402() -> dict:
    """x402 discovery document for .well-known crawlers and x402scan."""
    return build_well_known(get_settings())


@app.get("/llms.txt", response_class=PlainTextResponse)
def llms_txt() -> str:
    """LLM-readable capability description."""
    return build_llms_txt(get_settings())


@app.get("/.well-known/mcp/server-card.json", include_in_schema=False)
def mcp_server_card():
    from fastapi.responses import JSONResponse
    return JSONResponse({
        "name": "x402-a2a-hub",
        "description": (
            "Discover all services in the x402 micropayment task market. "
            "Returns endpoint URLs, supported formats, x402 payment details, "
            "and free trial endpoints for all available agents."
        ),
        "version": APP_VERSION,
        "homepage": "https://project-a2a-production.up.railway.app",
        "tools": [
            {
                "name": "get_capabilities",
                "description": (
                    "Retrieve the full capability manifest for the x402 micropayment task market. "
                    "Returns every available service with its endpoint URL, supported input/output formats, "
                    "x402 payment details (network, price in USD, asset contract), and free trial endpoint. "
                    "Use this to discover what the pipeline can do before calling specific tools."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                },
                "outputSchema": {
                    "type": "object",
                    "properties": {
                        "version": {"type": "string", "description": "Manifest schema version"},
                        "provider": {"type": "string", "description": "Name of the service provider"},
                        "description": {"type": "string", "description": "Human-readable description of the task market"},
                        "services": {
                            "type": "array",
                            "description": "List of available services",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "endpoint": {"type": "string"},
                                    "method": {"type": "string"},
                                    "payment": {
                                        "type": "object",
                                        "properties": {
                                            "scheme": {"type": "string"},
                                            "version": {"type": "integer"},
                                            "network": {"type": "string"},
                                            "asset": {"type": "string"},
                                            "price_usd": {"type": "number"}
                                        }
                                    },
                                    "trial_endpoint": {"type": "string"},
                                    "supported_conversions": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "from": {"type": "string"},
                                                "to": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "annotations": {
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": False
                }
            }
        ]
    })
