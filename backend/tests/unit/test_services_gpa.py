"""Unit tests for GPA distribution service — repo is mocked."""
from __future__ import annotations

from unittest.mock import patch

from app.models.gpa import GpaBucketResponse
from app.services import gpa as svc

_MOCK_ROWS = [
    {"bucket": "0.0-0.5", "count": 5},
    {"bucket": "2.5-3.0", "count": 120},
    {"bucket": "3.5-4.0", "count": 95},
]


def test_distribution_returns_validated_models() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS):
        result = svc.distribution()
    assert len(result) == 3
    assert all(isinstance(r, GpaBucketResponse) for r in result)


def test_distribution_caches_result() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS) as mock:
        svc.distribution(term="Fall2024")
        svc.distribution(term="Fall2024")
    assert mock.call_count == 1


def test_distribution_different_classification_sets_dont_share_cache() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS) as mock:
        svc.distribution(classifications=["Freshman"])
        svc.distribution(classifications=["Senior"])
    assert mock.call_count == 2


def test_distribution_sorted_classifications_share_cache() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS) as mock:
        svc.distribution(classifications=["Senior", "Freshman"])
        svc.distribution(classifications=["Freshman", "Senior"])
    assert mock.call_count == 1  # same key after sorting


def test_distribution_empty_result() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=[]):
        result = svc.distribution()
    assert result == []
