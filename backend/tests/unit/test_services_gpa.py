"""Unit tests for GPA distribution service — repo is mocked."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from app.models.gpa import GpaBucketResponse
from app.services import gpa as svc

_MOCK_ROWS = [
    {"bucket": "0.0-0.5", "count": 5},
    {"bucket": "2.5-3.0", "count": 120},
    {"bucket": "3.5-4.0", "count": 95},
]


@pytest.mark.asyncio
async def test_distribution_returns_validated_models() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS):
        result = await svc.distribution()
    assert len(result) == 3
    assert all(isinstance(r, GpaBucketResponse) for r in result)


@pytest.mark.asyncio
async def test_distribution_caches_result() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS) as mock:
        await svc.distribution(term="Fall2024")
        await svc.distribution(term="Fall2024")
    assert mock.call_count == 1


@pytest.mark.asyncio
async def test_distribution_different_classification_sets_dont_share_cache() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS) as mock:
        await svc.distribution(classifications=["Freshman"])
        await svc.distribution(classifications=["Senior"])
    assert mock.call_count == 2


@pytest.mark.asyncio
async def test_distribution_sorted_classifications_share_cache() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=_MOCK_ROWS) as mock:
        await svc.distribution(classifications=["Senior", "Freshman"])
        await svc.distribution(classifications=["Freshman", "Senior"])
    assert mock.call_count == 1


@pytest.mark.asyncio
async def test_distribution_empty_result() -> None:
    with patch("app.services.gpa._repo.distribution", return_value=[]):
        result = await svc.distribution()
    assert result == []
