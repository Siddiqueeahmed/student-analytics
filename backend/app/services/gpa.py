"""Business logic for GPA distribution with 5-min TTL cache."""
from __future__ import annotations

import asyncio
import threading
from typing import Union

from cachetools import TTLCache

from app.models.gpa import GpaBucketResponse
from app.repositories.gpa import GpaRepository, StudentRepository

_repo = GpaRepository()
_student_repo = StudentRepository()

_cache: TTLCache[
    tuple[str | None, str],
    Union[list[GpaBucketResponse], "asyncio.Future[list[GpaBucketResponse]]"],
] = TTLCache(maxsize=128, ttl=300)
_students_cache: TTLCache[
    int,
    Union[list[dict[str, object]], "asyncio.Future[list[dict[str, object]]]"],
] = TTLCache(maxsize=8, ttl=300)
_cache_lock = threading.Lock()


async def distribution(
    term: str | None = None,
    classifications: list[str] | None = None,
) -> list[GpaBucketResponse]:
    key = (term, ",".join(sorted(classifications or [])))

    with _cache_lock:
        entry = _cache.get(key)
        if entry is None:
            loop = asyncio.get_event_loop()
            future: asyncio.Future[list[GpaBucketResponse]] = loop.create_future()
            _cache[key] = future
            entry = None

    if entry is None:
        try:
            rows = await asyncio.to_thread(
                _repo.distribution, term=term, classifications=classifications
            )
            result = [GpaBucketResponse.model_validate(r) for r in rows]
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


async def list_students(limit: int = 500) -> list[dict[str, object]]:
    with _cache_lock:
        s_entry = _students_cache.get(limit)
        if s_entry is None:
            loop = asyncio.get_event_loop()
            s_future: asyncio.Future[list[dict[str, object]]] = loop.create_future()
            _students_cache[limit] = s_future
            s_entry = None

    if s_entry is None:
        try:
            rows = await asyncio.to_thread(_student_repo.list_students, limit)
            with _cache_lock:
                _students_cache[limit] = rows
            s_future.set_result(rows)
            return rows
        except Exception as exc:
            with _cache_lock:
                _students_cache.pop(limit, None)
            s_future.set_exception(exc)
            raise

    if isinstance(s_entry, asyncio.Future):
        return await s_entry
    return s_entry


def invalidate_cache() -> None:
    with _cache_lock:
        _cache.clear()
        _students_cache.clear()
