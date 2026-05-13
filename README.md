# x402 A2A Hub

Capability discovery hub for the x402 micropayment task market. Exposes a unified manifest of all live services so agents can discover, price-check, and chain calls without hardcoded URLs.

**Live service:** `https://project-a2a-production.up.railway.app`

---

## Discovery endpoints

| Endpoint | Description |
|---|---|
| `GET /v1/capabilities` | Full JSON capability manifest — all services, endpoints, payment details, trial URLs |
| `GET /.well-known/x402` | x402 protocol discovery document |
| `GET /llms.txt` | Plain-text service descriptions optimised for LLM/agent semantic search |
| `GET /health` | Health check — `{"status":"ok","service":"a2a-hub"}` |

---

## Capability manifest

`GET /v1/capabilities` returns a structured manifest of every service in the pipeline:

```json
{
  "version": "1.0",
  "provider": "Gary Edgington",
  "description": "x402 micropayment task market — data transformation and validation pipeline.",
  "services": [
    {
      "id": "formatter",
      "name": "Data Formatter",
      "description": "Converts CSV to JSON, XML to JSON, or Markdown to HTML.",
      "endpoint": "https://project-formatter-production.up.railway.app/v1/format",
      "trial_endpoint": "https://project-formatter-production.up.railway.app/v1/format/trial",
      "payment": { "scheme": "x402", "network": "eip155:8453", "price_usd": 0.005 }
    },
    {
      "id": "schema-checker",
      "name": "JSON Schema Checker",
      "description": "Validates JSON payloads against JSON Schema Draft 7.",
      "endpoint": "https://projectx402-production.up.railway.app/v1/schema-check",
      "trial_endpoint": "https://projectx402-production.up.railway.app/v1/schema-check/trial",
      "payment": { "scheme": "x402", "network": "eip155:8453", "price_usd": 0.005 }
    }
  ]
}
```

---

## Pipeline

Agents can chain services discovered via this hub:

```
Raw Input → Formatter (/v1/format) → Schema Checker (/v1/schema-check)
```

Each hop settles independently on Base mainnet via x402. The A2A hub itself has no payment gate — it is permanently free to query.

---

## Stack

- FastAPI + Uvicorn
- No Claude API dependency (pure manifest/routing logic)
- Deployed on Railway

---

## Related

- **Data Formatter:** `https://project-formatter-production.up.railway.app`
  - MCP SSE: `/mcp/sse` — listed on [Smithery](https://smithery.ai/server/gary-edgington/x402-data-formatter)
- **Schema Checker:** `https://projectx402-production.up.railway.app`
