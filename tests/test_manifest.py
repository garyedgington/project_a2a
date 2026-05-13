"""Tests for the A2A discovery hub endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "a2a-hub"


def test_health_head():
    response = client.head("/health")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# /v1/capabilities
# ---------------------------------------------------------------------------

def test_capabilities_returns_200():
    response = client.get("/v1/capabilities")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")


def test_capabilities_structure():
    body = client.get("/v1/capabilities").json()
    assert "version" in body
    assert "services" in body
    assert isinstance(body["services"], list)
    assert len(body["services"]) >= 2


def test_capabilities_contains_formatter():
    services = client.get("/v1/capabilities").json()["services"]
    ids = [s["id"] for s in services]
    assert "formatter" in ids


def test_capabilities_contains_schema_checker():
    services = client.get("/v1/capabilities").json()["services"]
    ids = [s["id"] for s in services]
    assert "schema-checker" in ids


def test_capabilities_endpoints_are_strings():
    services = client.get("/v1/capabilities").json()["services"]
    for service in services:
        assert isinstance(service["endpoint"], str)
        assert service["endpoint"].startswith("http")


# ---------------------------------------------------------------------------
# /.well-known/x402
# ---------------------------------------------------------------------------

def test_well_known_returns_200():
    response = client.get("/.well-known/x402")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")


def test_well_known_structure():
    body = client.get("/.well-known/x402").json()
    assert body["version"] == 2
    assert isinstance(body["services"], list)
    assert len(body["services"]) >= 2


def test_well_known_has_endpoints():
    services = client.get("/.well-known/x402").json()["services"]
    for service in services:
        assert "endpoint" in service
        assert "description" in service


# ---------------------------------------------------------------------------
# /llms.txt
# ---------------------------------------------------------------------------

def test_llms_txt_returns_200():
    response = client.get("/llms.txt")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]


def test_llms_txt_contains_key_content():
    body = client.get("/llms.txt").text
    assert "x402" in body
    assert "formatter" in body.lower()
    assert "schema" in body.lower()
    assert "$0.005" in body


def test_request_id_propagated():
    response = client.get("/health", headers={"X-Request-ID": "test-a2a-123"})
    assert response.headers["X-Request-ID"] == "test-a2a-123"
