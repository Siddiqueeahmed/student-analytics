"""Business logic for retention aggregations with 5-min TTL cache."""
from __future__ import annotations

import asyncio
import threading

from cachetools import TTLCache

from app.models.retention import ClassificationRetentionResponse
from app.repositories.retention import RetentionRepository

_repo = RetentionRepository()
_cache: TTLCache[
    tuple[str | None, str],
    list[ClassificationRetentionResponse] | asyncio.Future[list[ClassificationRetentionResponse]],
] = TTLCache(maxsize=128, ttl=300)
_cache_lock = threading.Lock()


async def by_classification(
    term: str | None = None,
    classifications: list[str] | None = None,
) -> list[ClassificationRetentionResponse]:
    key = (term, ",".join(sorted(classifications or [])))

    with _cache_lock:
        entry = _cache.get(key)
        if entry is None:
            loop = asyncio.get_event_loop()
            future: asyncio.Future[list[ClassificationRetentionResponse]] = loop.create_future()
            _cache[key] = future
            entry = None

    if entry is None:
        try:
            rows = await asyncio.to_thread(
                _repo.by_classification, term=term, classifications=classifications
            )
            result = [ClassificationRetentionResponse.model_validate(r) for r in rows]
            with _cache_lock:
                _cache[key] = result
            future.set_result(result)
            return result
        except Exception as exc:
            with _cache_lock:
                _cache.pop(key, None)
            future.set_exception(exc)
            raise

    if isinstance(entry, asyncio.Future):
        return await entry
    return entry


def invalidate_cache() -> None:
    with _cache_lock:
        _cache.clear()
