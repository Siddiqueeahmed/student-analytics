"""DB access for GPA distribution aggregations."""
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
            SELECT
                FLOOR(gpa / 0.5) * 0.5 AS bucket_start,
                COUNT(*) AS count
            FROM students
            {where}
            GROUP BY bucket_start
            ORDER BY bucket_start
        """

        with cursor() as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            {"bucket": f"{float(row[0]):.1f}-{float(row[0]) + 0.5:.1f}", "count": row[1]}
            for row in rows
        ]
