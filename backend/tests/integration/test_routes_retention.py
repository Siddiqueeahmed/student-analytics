"""Integration tests for GET /api/retention/by-classification."""
from __future__ import annotations

from fastapi.testclient import TestClient

_EXPECTED_ORDER = ["Freshman", "Sophomore", "Junior", "Senior"]


def test_returns_all_classifications(api_client: TestClient) -> None:
    data = api_client.get("/api/retention/by-classification").json()
    classifications = {r["classification"] for r in data}
    assert classifications == {"Freshman", "Sophomore", "Junior", "Senior"}


def test_response_schema(api_client: TestClient) -> None:
    data = api_client.get("/api/retention/by-classification").json()
    for row in data:
        assert "classification" in row
        assert "retention_rate" in row
        assert 0.0 <= row["retention_rate"] <= 1.0


def test_sorted_by_academic_progression(api_client: TestClient) -> None:
    data = api_client.get("/api/retention/by-classification").json()
    classifications = [r["classification"] for r in data]
    assert classifications == _EXPECTED_ORDER


def test_filter_by_term(api_client: TestClient) -> None:
    response = api_client.get("/api/retention/by-classification?term=Fall2024")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_freshman_retention_matches_fixture(api_client: TestClient) -> None:
    # Fixture: rows 1 (retained=True) and 5 (retained=False) are Freshman
    data = api_client.get(
        "/api/retention/by-classification?classification=Freshman"
    ).json()
    assert len(data) == 1
    assert data[0]["classification"] == "Freshman"
    assert abs(data[0]["retention_rate"] - 0.5) < 0.001  # 1 of 2 retained


def test_invalid_term_returns_422(api_client: TestClient) -> None:
    response = api_client.get("/api/retention/by-classification?term=bad")
    assert response.status_code == 422
