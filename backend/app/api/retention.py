"""Retention aggregation endpoint."""
from __future__ import annotations

import polars as pl
from fastapi import APIRouter

from app import state

router = APIRouter(tags=["retention"])

_CLASSIFICATION_ORDER = ["Freshman", "Sophomore", "Junior", "Senior"]


@router.get("/retention/by-classification")
def retention_by_classification() -> list[dict[str, object]]:
    result = (
        state.get_df()
        .group_by("classification")
        .agg(
            pl.col("retained_next_term").mean().alias("retention_rate")
        )
        .with_columns(
            pl.col("retention_rate").round(4)
        )
    )

    # Sort by natural academic progression
    order_map = {cls: i for i, cls in enumerate(_CLASSIFICATION_ORDER)}
    rows = result.to_dicts()
    rows.sort(key=lambda r: order_map.get(str(r["classification"]), 99))
    return rows  # type: ignore[return-value]
