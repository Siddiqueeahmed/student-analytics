"""DB access — reads from mart_enrollment_by_college (materialized KPI)."""
from __future__ import annotations

from app.core.database import cursor


class EnrollmentRepository:
    def by_college(
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
        # SUM over the pre-aggregated mart — no full-table scan
        query = f"""
            SELECT college, SUM(count) AS count
            FROM mart_enrollment_by_college
            {where}
            GROUP BY college
            ORDER BY college
        """

        with cursor() as conn:
            rows = conn.execute(query, params).fetchall()

        return [{"college": row[0], "count": row[1]} for row in rows]
