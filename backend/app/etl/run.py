"""ETL orchestrator — run as: python -m app.etl.run

Pipeline:
  1. extract   CSV → Polars DataFrame
  2. transform Polars validation + type casting
  3. load      Polars → DuckDB raw `students` table
  4. sql       stg → int → star schema → mart_* (layered SQL models)
  5. quality   data-quality gate (exits non-zero on violation)
  6. users     seed authentication users
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import passlib.hash  # type: ignore[import-untyped]

from app.core.config import settings
from app.etl.extract import extract
from app.etl.load import load
from app.etl.quality import enforce
from app.etl.transform import transform

_SQL_DIR = Path(__file__).parents[1] / "sql" / "models"

_SQL_FILES = [
    "stg_students.sql",
    "int_student_term.sql",
    "star_schema.sql",
    "mart_enrollment_by_college.sql",
    "mart_retention_by_classification.sql",
    "mart_gpa_distribution.sql",
]

_SEED_USERS = [
    ("viewer",   "viewer@example.com",   "viewer123",   "viewer"),
    ("analyst",  "analyst@example.com",  "analyst123",  "analyst"),
    ("admin",    "admin@example.com",    "admin123",    "admin"),
]


def _run_sql_layers(conn: duckdb.DuckDBPyConnection) -> None:
    for filename in _SQL_FILES:
        sql = (_SQL_DIR / filename).read_text(encoding="utf-8")
        print(f"[etl:sql] {filename}")
        conn.execute(sql)


def _seed_users(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id       VARCHAR PRIMARY KEY,
            email         VARCHAR NOT NULL UNIQUE,
            hashed_password VARCHAR NOT NULL,
            role          VARCHAR NOT NULL CHECK (role IN ('viewer','analyst','admin')),
            is_active     BOOLEAN NOT NULL DEFAULT TRUE
        )
    """)
    conn.execute("DELETE FROM users")
    for uid, email, password, role in _SEED_USERS:
        hashed = passlib.hash.bcrypt.hash(password)
        conn.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, TRUE)",
            [uid, email, hashed, role],
        )
    print(f"[etl:users] seeded {len(_SEED_USERS)} users")


def run() -> None:
    # --- Extract & Transform (Polars) ---
    print(f"[etl] extract  ← {settings.data_path}")
    raw = extract(settings.data_path)
    print(f"[etl]   {len(raw):,} rows extracted")

    cleaned = transform(raw)
    dropped = len(raw) - len(cleaned)
    print(f"[etl] transform → {len(cleaned):,} rows ({dropped} dropped)")

    # --- Load raw table (Polars → DuckDB) ---
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    count = load(cleaned, str(settings.db_path))
    print(f"[etl] load     → {count:,} rows in students table")

    # --- SQL layered models ---
    conn = duckdb.connect(str(settings.db_path))
    try:
        _run_sql_layers(conn)
        print("[etl] sql layers complete")

        # --- Data quality gate ---
        enforce(conn)

        # --- Seed users ---
        _seed_users(conn)
    finally:
        conn.close()

    print("[etl] done ✓")


if __name__ == "__main__":
    run()
    sys.exit(0)
