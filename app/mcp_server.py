"""
MCP server adapter — Phase 4c.

Single tool: get_capabilities
Calls build_capabilities() directly from app.manifest — no HTTP self-loop.

Transport: SSE, mounted in FastAPI via app.mount("/mcp", mcp.sse_app())
Smithery listing: x402 A2A Hub
"""

import json

from mcp.server.fastmcp import FastMCP

from app.config import get_settings
from app.manifest import build_capabilities

# ── FastMCP instance ───────────────────────────────────────────────────────────

mcp = FastMCP(
    name="x402-a2a-hub",
    instructions=(
        "This MCP server is the discovery hub for the x402 micropayment task market. "
        "Call get_capabilities to retrieve every available service with its endpoint URL, "
        "supported formats, x402 payment details, and free trial endpoint. "
        "Use it as the first step before calling any specific service tool."
    ),
)


# ── Tool: get_capabilities ─────────────────────────────────────────────────────

@mcp.tool(
    description=(
        "Retrieve the full capability manifest for the x402 micropayment task market. "
        "Returns every available service with its endpoint URL, supported input/output formats, "
        "x402 payment details (network, price in USD, asset contract), and free trial endpoint. "
        "Use this to discover what the pipeline can do before calling specific tools."
    )
)
def get_capabilities() -> str:
    """
    Return the A2A hub capability manifest.

    Returns:
        JSON-encoded capability manifest with all services and their metadata.
        On error: {"error": "<description>"}
    """
    try:
        manifest = build_capabilities(get_settings())
        return json.dumps(manifest)
    except Exception as exc:
        return json.dumps({"error": f"get_capabilities failed: {exc}"})
