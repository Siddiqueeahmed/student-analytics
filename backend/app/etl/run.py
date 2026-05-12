"""ETL orchestrator — run as: python -m app.etl.run"""
from __future__ import annotations

import sys

from app.core.config import settings
from app.etl.extract import extract
from app.etl.load import load
from app.etl.transform import transform


def run() -> None:
    print(f"[etl] extract  ← {settings.data_path}")
    raw = extract(settings.data_path)
    print(f"[etl]   {len(raw):,} rows extracted")

    cleaned = transform(raw)
    dropped = len(raw) - len(cleaned)
    print(f"[etl] transform → {len(cleaned):,} rows ({dropped} dropped by validation)")

    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    count = load(cleaned, str(settings.db_path))
    print(f"[etl] load     → {count:,} rows in {settings.db_path}")


if __name__ == "__main__":
    run()
    sys.exit(0)
