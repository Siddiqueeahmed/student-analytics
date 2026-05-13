"""Admin endpoints — ETL refresh, requires admin role."""
from __future__ import annotations

import asyncio
from pathlib import Path

import duckdb

from fastapi import APIRouter, Depends

from app.auth.dependencies import require_admin
from app.auth.models import TokenPayload
from app.core.config import settings
from app.core.database import cursor
from app.etl.extract import extract
from app.etl.load import load
from app.etl.quality import enforce
from app.etl.transform import transform

router = APIRouter(tags=["admin"])

_SQL_DIR = Path(__file__).parents[1] / "sql" / "models"

_SQL_FILES = [
    "stg_students.sql",
    "int_student_term.sql",
    "star_schema.sql",
    "mart_enrollment_by_college.sql",
    "mart_retention_by_classification.sql",
    "mart_gpa_distribution.sql",
]


def _refresh_in_place() -> None:
    """Run ETL using the existing singleton connection — no second file open."""
    raw = extract(settings.data_path)
    cleaned = transform(raw)

    with cursor() as conn:
        # Re-create the students table in the open connection
        conn.execute("CREATE OR REPLACE TABLE students AS SELECT * FROM _staging")
        conn.register("_staging", cleaned)
        conn.execute("CREATE OR REPLACE TABLE students AS SELECT * FROM _staging")
        conn.unregister("_staging")

        for filename in _SQL_FILES:
            sql = (_SQL_DIR / filename).read_text(encoding="utf-8")
            conn.execute(sql)

        enforce(conn)


@router.post("/admin/etl/refresh", response_model=dict[str, str])
async def trigger_etl_refresh(
    _: TokenPayload = Depends(require_admin),
) -> dict[str, str]:
    """Re-run the full ETL pipeline in-place (admin only). Invalidates all caches."""
    await asyncio.to_thread(_refresh_in_place)

    from app.services import enrollment, gpa, retention
    enrollment.invalidate_cache()
    retention.invalidate_cache()
    gpa.invalidate_cache()

    return {"status": "ok"}
