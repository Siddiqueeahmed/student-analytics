"""ETL — Extract: read the raw CSV with Polars."""
from __future__ import annotations

from pathlib import Path

import polars as pl


def extract(csv_path: Path) -> pl.DataFrame:
    return pl.read_csv(csv_path)
