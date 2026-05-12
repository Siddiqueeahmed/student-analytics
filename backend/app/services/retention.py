"""Business logic for retention aggregations with 5-min LRU cache."""
from __future__ import annotations

import threading

from cachetools import TTLCache

from app.models.retention import ClassificationRetentionResponse
from app.repositories.retention import RetentionRepository

_repo = RetentionRepository()
_cache: TTLCache[tuple[str | None, str], list[ClassificationRetentionResponse]] = TTLCache(
    maxsize=128, ttl=300
)
_cache_lock = threading.Lock()


def by_classification(
    term: str | None = None,
    classifications: list[str] | None = None,
) -> list[ClassificationRetentionResponse]:
    key = (term, ",".join(sorted(classifications or [])))

    with _cache_lock:
        cached = _cache.get(key)
    if cached is not None:
        return cached

    rows = _repo.by_classification(term=term, classifications=classifications)
    result = [ClassificationRetentionResponse.model_validate(r) for r in rows]

    with _cache_lock:
        _cache[key] = result
    return result


def invalidate_cache() -> None:
    with _cache_lock:
        _cache.clear()
