"""Unit tests for retention service — repo is mocked."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from app.models.retention import ClassificationRetentionResponse
from app.services import retention as svc

_MOCK_ROWS = [
    {"classification": "Freshman",  "retention_rate": 0.72},
    {"classification": "Sophomore", "retention_rate": 0.81},
    {"classification": "Junior",    "retention_rate": 0.85},
    {"classification": "Senior",    "retention_rate": 0.90},
]


@pytest.mark.asyncio
async def test_by_classification_returns_validated_models() -> None:
    with patch("app.services.retention._repo.by_classification", return_value=_MOCK_ROWS):
        result = await svc.by_classification()
    assert len(result) == 4
    assert all(isinstance(r, ClassificationRetentionResponse) for r in result)


@pytest.mark.asyncio
async def test_by_classification_retention_rate_in_range() -> None:
    with patch("app.services.retention._repo.by_classification", return_value=_MOCK_ROWS):
        result = await svc.by_classification()
    for r in result:
        assert 0.0 <= r.retention_rate <= 1.0


@pytest.mark.asyncio
async def test_by_classification_caches_result() -> None:
    with patch("app.services.retention._repo.by_classification", return_value=_MOCK_ROWS) as mock:
        await svc.by_classification(term="Fall2024")
        await svc.by_classification(term="Fall2024")
    assert mock.call_count == 1


@pytest.mark.asyncio
async def test_by_classification_passes_filters() -> None:
    with patch("app.services.retention._repo.by_classification", return_value=_MOCK_ROWS) as mock:
        await svc.by_classification(term="Fall2024", classifications=["Junior"])
    mock.assert_called_once_with(term="Fall2024", classifications=["Junior"])
