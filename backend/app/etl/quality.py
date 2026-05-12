"""ETL data-quality gate — exits non-zero on any violation."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field

import duckdb

_MIN_ROW_COUNT = 4_000          # expect at least 80% of 5,000
_MAX_NULL_RATE = 0.01           # less than 1% nulls in any column
_VALID_CLASSIFICATIONS = frozenset({"Freshman", "Sophomore", "Junior", "Senior"})
_TERM_RE = r"^(Fall|Spring)\d{4}$"


@dataclass
class QualityReport:
    violations: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.violations.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.violations) == 0


def run_checks(conn: duckdb.DuckDBPyConnection) -> QualityReport:
    report = QualityReport()

    # 1. Row count
    (row_count,) = conn.execute("SELECT COUNT(*) FROM stg_students").fetchone()  # type: ignore[misc]
    if row_count < _MIN_ROW_COUNT:
        report.fail(f"Row count {row_count:,} is below minimum {_MIN_ROW_COUNT:,}")

    # 2. GPA range
    (bad_gpa,) = conn.execute(
        "SELECT COUNT(*) FROM stg_students WHERE gpa < 0 OR gpa > 4.0"
    ).fetchone()  # type: ignore[misc]
    if bad_gpa > 0:
        report.fail(f"{bad_gpa} rows with GPA outside [0, 4.0]")

    # 3. Classification FK integrity
    (bad_cls,) = conn.execute(
        "SELECT COUNT(*) FROM stg_students "
        "WHERE classification NOT IN ('Freshman','Sophomore','Junior','Senior')"
    ).fetchone()  # type: ignore[misc]
    if bad_cls > 0:
        report.fail(f"{bad_cls} rows with invalid classification")

    # 4. Null rates on critical columns
    for col in ("student_id", "term", "college", "program", "classification", "gpa"):
        (nulls,) = conn.execute(
            f"SELECT COUNT(*) FROM stg_students WHERE {col} IS NULL"  # noqa: S608
        ).fetchone()  # type: ignore[misc]
        null_rate = nulls / max(row_count, 1)
        if null_rate > _MAX_NULL_RATE:
            report.fail(f"Column '{col}' null rate {null_rate:.2%} exceeds {_MAX_NULL_RATE:.0%}")

    # 5. fact_enrollment FK integrity (after star schema load)
    (orphan_students,) = conn.execute(
        "SELECT COUNT(*) FROM fact_enrollment fe "
        "WHERE NOT EXISTS (SELECT 1 FROM dim_student ds WHERE ds.student_key = fe.student_key)"
    ).fetchone()  # type: ignore[misc]
    if orphan_students > 0:
        report.fail(f"{orphan_students} fact rows with no matching dim_student")

    return report


def enforce(conn: duckdb.DuckDBPyConnection) -> None:
    report = run_checks(conn)
    if not report.passed:
        print("[etl:quality] FAILED — violations:", file=sys.stderr)
        for v in report.violations:
            print(f"  • {v}", file=sys.stderr)
        sys.exit(1)
    print(f"[etl:quality] OK — {len(report.violations)} violations")
