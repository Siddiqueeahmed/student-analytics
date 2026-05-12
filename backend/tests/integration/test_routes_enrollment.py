"""Integration tests for GET /api/enrollment/by-college."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_returns_all_colleges(api_client: TestClient) -> None:
    response = api_client.get("/api/enrollment/by-college")
    assert response.status_code == 200
    data = response.json()
    colleges = {row["college"] for row in data}
    assert colleges == {"Engineering", "Business", "Liberal Arts"}


def test_response_schema(api_client: TestClient) -> None:
    data = api_client.get("/api/enrollment/by-college").json()
    for row in data:
        assert "college" in row
        assert "count" in row
        assert isinstance(row["count"], int)
        assert row["count"] > 0


def test_filter_by_term(api_client: TestClient) -> None:
    fall = api_client.get("/api/enrollment/by-college?term=Fall2024").json()
    spring = api_client.get("/api/enrollment/by-college?term=Spring2024").json()
    fall_total = sum(r["count"] for r in fall)
    spring_total = sum(r["count"] for r in spring)
    assert fall_total + spring_total == 6  # matches fixture rows


def test_filter_by_classification(api_client: TestClient) -> None:
    response = api_client.get("/api/enrollment/by-college?classification=Freshman")
    assert response.status_code == 200
    data = response.json()
    total = sum(r["count"] for r in data)
    assert total == 2  # rows 1 and 5 are Freshman


def test_filter_by_multiple_classifications(api_client: TestClient) -> None:
    response = api_client.get(
        "/api/enrollment/by-college?classification=Freshman&classification=Senior"
    )
    assert response.status_code == 200
    total = sum(r["count"] for r in response.json())
    assert total == 3  # rows 1, 4, 5


def test_invalid_term_format_returns_422(api_client: TestClient) -> None:
    response = api_client.get("/api/enrollment/by-college?term=NotATerm")
    assert response.status_code == 422


def test_results_sorted_by_college(api_client: TestClient) -> None:
    data = api_client.get("/api/enrollment/by-college").json()
    colleges = [r["college"] for r in data]
    assert colleges == sorted(colleges)
