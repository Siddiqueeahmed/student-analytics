"""Metadata endpoint — returns available filter dimensions."""
from __future__ import annotations

import asyncio

from fastapi import APIRouter

from app.core.database import cursor

router = APIRouter(tags=["meta"])


def _fetch_terms() -> list[str]:
    with cursor() as conn:
        rows = conn.execute(
            "SELECT DISTINCT term FROM mart_enrollment_by_college ORDER BY term DESC"
        ).fetchall()
    return [row[0] for row in rows]


@router.get("/meta/terms", response_model=list[str])
async def available_terms() -> list[str]:
    """Returns every term that has at least one enrollment record."""
    return await asyncio.to_thread(_fetch_terms)
