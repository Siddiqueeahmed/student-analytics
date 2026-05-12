"""Unit tests for enrollment service — repo is mocked."""
from __future__ import annotations

from unittest.mock import patch

from app.models.enrollment import CollegeEnrollmentResponse
from app.services import enrollment as svc

_MOCK_ROWS = [
    {"college": "Engineering", "count": 300},
    {"college": "Business", "count": 200},
]


def test_by_college_returns_validated_models() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS):
        result = svc.by_college()
    assert len(result) == 2
    assert all(isinstance(r, CollegeEnrollmentResponse) for r in result)


def test_by_college_passes_filters_to_repo() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS) as mock:
        svc.by_college(term="Fall2024", classifications=["Freshman"])
    mock.assert_called_once_with(term="Fall2024", classifications=["Freshman"])


def test_by_college_caches_result() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS) as mock:
        svc.by_college(term="Fall2024")
        svc.by_college(term="Fall2024")  # second call — should hit cache
    assert mock.call_count == 1  # repo called only once


def test_by_college_different_keys_dont_share_cache() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS) as mock:
        svc.by_college(term="Fall2024")
        svc.by_college(term="Spring2024")
    assert mock.call_count == 2


def test_by_college_empty_result() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=[]):
        result = svc.by_college()
    assert result == []
