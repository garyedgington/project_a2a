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
