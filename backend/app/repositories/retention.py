"""DB access — reads from mart_retention_by_classification (materialized KPI)."""
from __future__ import annotations

from app.core.database import cursor

_CLASSIFICATION_ORDER = {
    cls: i for i, cls in enumerate(["Freshman", "Sophomore", "Junior", "Senior"])
}


class RetentionRepository:
    def by_classification(
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
        # Compute weighted rate from pre-summed counts
        query = f"""
            SELECT
                classification,
                CAST(SUM(retained_count) AS DOUBLE) / SUM(student_count) AS retention_rate
            FROM mart_retention_by_classification
            {where}
            GROUP BY classification
        """

        with cursor() as conn:
            rows = conn.execute(query, params).fetchall()

        result: list[dict[str, object]] = [
            {"classification": row[0], "retention_rate": round(float(row[1]), 4)}
            for row in rows
        ]
        result.sort(key=lambda r: _CLASSIFICATION_ORDER.get(str(r["classification"]), 99))
        return result
