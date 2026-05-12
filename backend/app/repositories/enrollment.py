"""DB access for enrollment aggregations."""
from __future__ import annotations

from app.core.database import cursor

# Filter columns come from validated query-param enums, never raw user strings.
# The WHERE clause *structure* uses string building; VALUES use ? placeholders.


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
        query = f"""
            SELECT college, COUNT(*) AS count
            FROM students
            {where}
            GROUP BY college
            ORDER BY college
        """

        with cursor() as conn:
            rows = conn.execute(query, params).fetchall()

        return [{"college": row[0], "count": row[1]} for row in rows]
