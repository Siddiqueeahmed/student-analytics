"""Integration tests for GET /api/gpa/distribution."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_returns_buckets(api_client: TestClient) -> None:
    data = api_client.get("/api/gpa/distribution").json()
    assert len(data) > 0


def test_response_schema(api_client: TestClient) -> None:
    data = api_client.get("/api/gpa/distribution").json()
    for row in data:
        assert "bucket" in row
        assert "count" in row
        assert isinstance(row["count"], int)
        assert row["count"] > 0
        # bucket format: "X.X-Y.Y"
        assert "-" in row["bucket"]


def test_buckets_sorted_ascending(api_client: TestClient) -> None:
    data = api_client.get("/api/gpa/distribution").json()
    starts = [float(r["bucket"].split("-")[0]) for r in data]
    assert starts == sorted(starts)


def test_total_count_matches_fixture(api_client: TestClient) -> None:
    data = api_client.get("/api/gpa/distribution").json()
    assert sum(r["count"] for r in data) == 6  # 6 fixture rows


def test_filter_by_term_reduces_count(api_client: TestClient) -> None:
    all_data = api_client.get("/api/gpa/distribution").json()
    fall_data = api_client.get("/api/gpa/distribution?term=Fall2024").json()
    all_total = sum(r["count"] for r in all_data)
    fall_total = sum(r["count"] for r in fall_data)
    assert fall_total < all_total


def test_invalid_term_returns_422(api_client: TestClient) -> None:
    response = api_client.get("/api/gpa/distribution?term=INVALID")
    assert response.status_code == 422
