"""Business logic for GPA distribution with 5-min LRU cache."""
from __future__ import annotations

import threading

from cachetools import TTLCache

from app.models.gpa import GpaBucketResponse
from app.repositories.gpa import GpaRepository

_repo = GpaRepository()
_cache: TTLCache[tuple[str | None, str], list[GpaBucketResponse]] = TTLCache(
    maxsize=128, ttl=300
)
_cache_lock = threading.Lock()


def distribution(
    term: str | None = None,
    classifications: list[str] | None = None,
) -> list[GpaBucketResponse]:
    key = (term, ",".join(sorted(classifications or [])))

    with _cache_lock:
        cached = _cache.get(key)
    if cached is not None:
        return cached

    rows = _repo.distribution(term=term, classifications=classifications)
    result = [GpaBucketResponse.model_validate(r) for r in rows]

    with _cache_lock:
        _cache[key] = result
    return result


def invalidate_cache() -> None:
    with _cache_lock:
        _cache.clear()
