"""Unit tests for enrollment service — repo is mocked."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.models.enrollment import CollegeEnrollmentResponse
from app.services import enrollment as svc

_MOCK_ROWS = [
    {"college": "Engineering", "count": 300},
    {"college": "Business", "count": 200},
]


@pytest.mark.asyncio
async def test_by_college_returns_validated_models() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS):
        result = await svc.by_college()
    assert len(result) == 2
    assert all(isinstance(r, CollegeEnrollmentResponse) for r in result)


@pytest.mark.asyncio
async def test_by_college_passes_filters_to_repo() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS) as mock:
        await svc.by_college(term="Fall2024", classifications=["Freshman"])
    mock.assert_called_once_with(term="Fall2024", classifications=["Freshman"])


@pytest.mark.asyncio
async def test_by_college_caches_result() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS) as mock:
        await svc.by_college(term="Fall2024")
        await svc.by_college(term="Fall2024")
    assert mock.call_count == 1


@pytest.mark.asyncio
async def test_by_college_different_keys_dont_share_cache() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=_MOCK_ROWS) as mock:
        await svc.by_college(term="Fall2024")
        await svc.by_college(term="Spring2024")
    assert mock.call_count == 2


@pytest.mark.asyncio
async def test_by_college_empty_result() -> None:
    with patch("app.services.enrollment._repo.by_college", return_value=[]):
        result = await svc.by_college()
    assert result == []
