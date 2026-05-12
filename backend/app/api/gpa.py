"""GPA distribution endpoint."""
from __future__ import annotations

import polars as pl
from fastapi import APIRouter

from app import state

router = APIRouter(tags=["gpa"])


@router.get("/gpa/distribution")
def gpa_distribution() -> list[dict[str, object]]:
    result = (
        state.get_df()
        .with_columns(
            ((pl.col("gpa") / 0.5).floor() * 0.5).alias("bucket_start")
        )
        .group_by("bucket_start")
        .agg(pl.len().alias("count"))
        .sort("bucket_start")
        .with_columns(
            pl.col("bucket_start")
            .map_elements(
                lambda x: f"{x:.1f}-{x + 0.5:.1f}",
                return_dtype=pl.String,
            )
            .alias("bucket")
        )
        .select(["bucket", "count"])
    )
    return result.to_dicts()  # type: ignore[return-value]
