# ADR 0003 — SQL Layered Models (stg → int → star → mart)

**Status:** Accepted  
**Date:** 2026-05-12

## Context

After the raw `students` table is loaded from CSV, several transformation steps are needed: type casting, derived columns, dimensional modeling, and pre-aggregated KPI tables. These transformations could be done entirely in Polars, entirely in SQL, or as a hybrid.

A dbt-style layered approach separates concerns: staging cleans and casts raw data; intermediate adds business logic; star schema normalizes into dimensions and facts; mart tables pre-aggregate for fast API queries. Each layer builds on the previous one, making the lineage explicit and each layer independently testable.

Running the SQL files in order inside a single DuckDB connection is semantically equivalent to dbt's `ref()` graph — without requiring dbt as a dependency.

## Decision

Execute six SQL model files in order during the ETL run: `stg_students.sql` → `int_student_term.sql` → `star_schema.sql` → `mart_enrollment_by_college.sql` → `mart_retention_by_classification.sql` → `mart_gpa_distribution.sql`.

## Consequences

**Benefits:**
- Lineage is explicit: each `.sql` file has a single responsibility and a stable output schema.
- Mart tables act as a query cache: API endpoints do `SUM(count)` over pre-aggregated rows instead of scanning the full fact table.
- SQL is version-controlled and readable without running any code.
- Adding a new KPI means adding one SQL file and one repository method — no Polars changes needed.

**Trade-offs:**
- ETL must re-run all layers from scratch on each refresh (no incremental models).
- Ordering is implicit (file list in `run.py`) rather than declared via a DAG; adding a new layer requires manual placement in the list.
- For very large datasets, a full `CREATE OR REPLACE TABLE` per layer would be slow. At 5 K rows, this is negligible.
