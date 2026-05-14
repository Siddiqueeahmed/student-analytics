"""DB access — reads from mart_gpa_distribution (materialized KPI)."""
from __future__ import annotations

from app.core.database import cursor


class GpaRepository:
    def distribution(
        self,
        term: str | None,
        classifications: list[str] | None,
    ) -> list[dict[str, object]]:
        params: list[object] = []
        filters: list[str] = []

        if term is not None:
            filters.append("term = ?")
            params.append(term)

        if classifications:
            placeholders = ", ".join("?" for _ in classifications)
            filters.append(f"classification IN ({placeholders})")
            params.extend(classifications)

        where = f"WHERE {' AND '.join(filters)}" if filters else ""
        query = f"""
            SELECT bucket_start, SUM(count) AS count
            FROM mart_gpa_distribution
            {where}
            GROUP BY bucket_start
            ORDER BY bucket_start
        """

        with cursor() as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            {
                "bucket": f"{float(row[0]):.1f}-{min(float(row[0]) + 0.5, 4.0):.1f}",
                "count": row[1],
            }
            for row in rows
        ]


class StudentRepository:
    def list_students(self, limit: int = 500) -> list[dict[str, object]]:
        query = """
            SELECT
                ds.student_id,
                dt.term_name        AS term,
                dc.college_name     AS college,
                dp.program_name     AS program,
                fe.classification,
                fe.gpa,
                fe.credit_hours_attempted,
                fe.credit_hours_earned,
                fe.retained_next_term
            FROM fact_enrollment fe
            JOIN dim_student  ds ON fe.student_key  = ds.student_key
            JOIN dim_term     dt ON fe.term_key     = dt.term_key
            JOIN dim_college  dc ON fe.college_key  = dc.college_key
            JOIN dim_program  dp ON fe.program_key  = dp.program_key
            ORDER BY ds.student_id
            LIMIT ?
        """
        with cursor() as conn:
            rows = conn.execute(query, [limit]).fetchall()

        cols = [
            "student_id", "term", "college", "program", "classification",
            "gpa", "credit_hours_attempted", "credit_hours_earned", "retained_next_term",
        ]
        return [dict(zip(cols, row, strict=False)) for row in rows]
