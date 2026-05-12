"""ETL — Load: sink a Polars DataFrame into DuckDB."""
from __future__ import annotations

import duckdb
import polars as pl

_DDL = """
CREATE OR REPLACE TABLE students (
    student_id  BIGINT  NOT NULL,
    term        VARCHAR NOT NULL,
    college     VARCHAR NOT NULL,
    program     VARCHAR NOT NULL,
    classification VARCHAR NOT NULL,
    gpa         DOUBLE  NOT NULL,
    credit_hours_attempted INTEGER NOT NULL,
    credit_hours_earned    INTEGER NOT NULL,
    enrolled           BOOLEAN NOT NULL,
    retained_next_term BOOLEAN NOT NULL
);
"""


def load(df: pl.DataFrame, db_path: str) -> int:
    """Write *df* to the students table; returns the final row count."""
    conn = duckdb.connect(db_path)
    try:
        conn.execute(_DDL)
        # DuckDB can read a Polars DataFrame directly via Arrow protocol
        conn.register("_staging", df)
        conn.execute("INSERT INTO students SELECT * FROM _staging")
        count: int = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]  # type: ignore[index]
    finally:
        conn.close()
    return count
