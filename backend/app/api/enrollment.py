"""Enrollment aggregation endpoint."""
from __future__ import annotations

import polars as pl
from fastapi import APIRouter

from app import state

router = APIRouter(tags=["enrollment"])


@router.get("/enrollment/by-college")
def enrollment_by_college() -> list[dict[str, object]]:
    result = (
        state.get_df()
        .group_by("college")
        .agg(pl.len().alias("count"))
        .sort("college")
    )
    return result.to_dicts()  # type: ignore[return-value]
