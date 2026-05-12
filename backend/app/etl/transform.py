"""ETL — Transform: validate and cast types with Polars."""
from __future__ import annotations

import polars as pl

_VALID_CLASSIFICATIONS = frozenset({"Freshman", "Sophomore", "Junior", "Senior"})


def transform(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.with_columns(
            pl.col("gpa").cast(pl.Float64),
            pl.col("credit_hours_attempted").cast(pl.Int32),
            pl.col("credit_hours_earned").cast(pl.Int32),
            pl.col("student_id").cast(pl.Int64),
            pl.col("enrolled").cast(pl.Boolean),
            pl.col("retained_next_term").cast(pl.Boolean),
        )
        .filter(pl.col("gpa").is_between(0.0, 4.0))
        .filter(pl.col("credit_hours_attempted") > 0)
        .filter(pl.col("classification").is_in(list(_VALID_CLASSIFICATIONS)))
        .filter(pl.col("term").str.contains(r"^(Fall|Spring)\d{4}$"))
    )
