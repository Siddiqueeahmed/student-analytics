"""Module-level DataFrame state for the Phase 1 in-memory CSV store."""
from __future__ import annotations

import polars as pl

_df: pl.DataFrame | None = None


def set_df(df: pl.DataFrame) -> None:
    global _df
    _df = df


def get_df() -> pl.DataFrame:
    if _df is None:
        raise RuntimeError("Student data has not been loaded; lifespan may not have run")
    return _df
