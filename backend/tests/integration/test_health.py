"""Integration test for the health endpoint."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_returns_ok(api_client: TestClient) -> None:
    response = api_client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_sets_request_id_header(api_client: TestClient) -> None:
    response = api_client.get("/api/health")
    assert "x-request-id" in response.headers


def test_health_propagates_provided_request_id(api_client: TestClient) -> None:
    response = api_client.get("/api/health", headers={"X-Request-ID": "test-123"})
    assert response.headers["x-request-id"] == "test-123"
