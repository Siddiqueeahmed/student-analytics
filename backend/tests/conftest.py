"""Shared pytest fixtures — in-memory DuckDB with mart tables for integration tests."""
from __future__ import annotations

from pathlib import Path

import duckdb
import pytest
from fastapi.testclient import TestClient

_SQL_DIR = Path(__file__).parents[1] / "app" / "sql" / "models"

_DDL_STUDENTS = """
CREATE TABLE students (
    student_id             BIGINT  NOT NULL,
    term                   VARCHAR NOT NULL,
    college                VARCHAR NOT NULL,
    program                VARCHAR NOT NULL,
    classification         VARCHAR NOT NULL,
    gpa                    DOUBLE  NOT NULL,
    credit_hours_attempted INTEGER NOT NULL,
    credit_hours_earned    INTEGER NOT NULL,
    enrolled               BOOLEAN NOT NULL,
    retained_next_term     BOOLEAN NOT NULL
)
"""

_ROWS: list[tuple[object, ...]] = [
    (1, "Fall2024",   "Engineering",  "CS",         "Freshman",  3.5, 15, 15, True,  True),
    (2, "Fall2024",   "Business",     "Finance",    "Sophomore", 2.8, 15, 15, True,  True),
    (3, "Spring2024", "Engineering",  "CS",         "Junior",    3.2, 16, 16, True,  False),
    (4, "Fall2024",   "Liberal Arts", "English",    "Senior",    3.8, 12, 12, True,  True),
    (5, "Spring2024", "Business",     "Accounting", "Freshman",  1.5, 15, 10, True,  False),
    (6, "Fall2024",   "Engineering",  "CS",         "Sophomore", 3.0, 15, 15, True,  True),
]

_SQL_FILES = [
    "stg_students.sql",
    "int_student_term.sql",
    "star_schema.sql",
    "mart_enrollment_by_college.sql",
    "mart_retention_by_classification.sql",
    "mart_gpa_distribution.sql",
]


def _build_db() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(":memory:")
    conn.execute(_DDL_STUDENTS)
    conn.executemany("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)", _ROWS)
    for filename in _SQL_FILES:
        sql = (_SQL_DIR / filename).read_text(encoding="utf-8")
        conn.execute(sql)
    return conn


@pytest.fixture(scope="session")
def mem_conn() -> duckdb.DuckDBPyConnection:
    return _build_db()


@pytest.fixture(scope="session")
def api_client(mem_conn: duckdb.DuckDBPyConnection) -> TestClient:
    import app.core.database as db

    db._conn = mem_conn  # noqa: SLF001

    from app.main import app as fastapi_app

    from app.services import enrollment, gpa, retention

    enrollment.invalidate_cache()
    retention.invalidate_cache()
    gpa.invalidate_cache()

    return TestClient(fastapi_app, raise_server_exceptions=True)


@pytest.fixture(autouse=True)
def clear_caches() -> None:
    from app.services import enrollment, gpa, retention

    enrollment.invalidate_cache()
    retention.invalidate_cache()
    gpa.invalidate_cache()
