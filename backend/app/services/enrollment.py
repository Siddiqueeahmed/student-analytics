"""Business logic for enrollment aggregations with 5-min TTL cache."""
from __future__ import annotations

import asyncio
import threading
from typing import Union

from cachetools import TTLCache

from app.models.enrollment import CollegeEnrollmentResponse
from app.repositories.enrollment import EnrollmentRepository

_repo = EnrollmentRepository()
# Cache stores either the result list or a Future representing an in-flight query.
# This prevents the thundering herd: concurrent requests on the same cold key
# await the same Future instead of each dispatching a separate DB query.
_cache: TTLCache[
    tuple[str | None, str],
    Union[list[CollegeEnrollmentResponse], "asyncio.Future[list[CollegeEnrollmentResponse]]"],
] = TTLCache(maxsize=128, ttl=300)
_cache_lock = threading.Lock()


async def by_college(
    term: str | None = None,
    classifications: list[str] | None = None,
) -> list[CollegeEnrollmentResponse]:
    key = (term, ",".join(sorted(classifications or [])))

    with _cache_lock:
        entry = _cache.get(key)
        if entry is not None:
            pass  # will handle below, outside the lock
        else:
            # First request for this key: plant a Future so others can wait on it
            loop = asyncio.get_event_loop()
            future: asyncio.Future[list[CollegeEnrollmentResponse]] = loop.create_future()
            _cache[key] = future
            entry = None  # signal that we own the fetch

    if entry is None:
        # We own the fetch
        try:
            rows = await asyncio.to_thread(
                _repo.by_college, term=term, classifications=classifications
            )
            result = [CollegeEnrollmentResponse.model_validate(r) for r in rows]
            with _cache_lock:
                _cache[key] = result
            future.set_result(result)
            return result
        except Exception as exc:
            with _cache_lock:
                _cache.pop(key, None)
            future.set_exception(exc)
            raise

    # Another coroutine already owns the fetch
    if isinstance(entry, asyncio.Future):
        return await entry
    return entry


def invalidate_cache() -> None:
    with _cache_lock:
        _cache.clear()
