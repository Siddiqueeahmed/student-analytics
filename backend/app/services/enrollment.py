"""Business logic for enrollment aggregations with 5-min TTL cache."""
from __future__ import annotations

import asyncio
import threading

from cachetools import TTLCache

from app.models.enrollment import CollegeEnrollmentResponse
from app.repositories.enrollment import EnrollmentRepository

_repo = EnrollmentRepository()
_cache: TTLCache[tuple[str | None, str], list[CollegeEnrollmentResponse]] = TTLCache(
    maxsize=128, ttl=300
)
_cache_lock = threading.Lock()


async def by_college(
    term: str | None = None,
    classifications: list[str] | None = None,
) -> list[CollegeEnrollmentResponse]:
    key = (term, ",".join(sorted(classifications or [])))

    with _cache_lock:
        cached = _cache.get(key)
    if cached is not None:
        return cached

    rows = await asyncio.to_thread(_repo.by_college, term=term, classifications=classifications)
    result = [CollegeEnrollmentResponse.model_validate(r) for r in rows]

    with _cache_lock:
        _cache[key] = result
    return result


def invalidate_cache() -> None:
    with _cache_lock:
        _cache.clear()
