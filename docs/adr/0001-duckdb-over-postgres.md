# ADR 0001 — DuckDB over PostgreSQL

**Status:** Accepted  
**Date:** 2026-05-12

## Context

The analytics backend needs a query engine capable of aggregating 5,000+ student enrollment records with low operational overhead. The two main candidates considered were PostgreSQL and DuckDB.

PostgreSQL is a battle-tested OLTP database that many teams already operate. However, it requires a running server process, connection pooling (PgBouncer), schema migrations tooling (Alembic), and either a managed cloud database or a self-managed instance with backup infrastructure. For an analytics portfolio project, this operational surface area is disproportionate to the data volume.

DuckDB is an embedded OLAP database that runs in-process, stores state in a single file, and exposes an Arrow-native interface that integrates directly with Polars DataFrames. Because it is embedded, there is no server to provision, no connection string to manage in CI, and no port to expose. DuckDB's columnar execution engine is optimised for analytical GROUP BY and aggregation queries — exactly the workload in this project.

## Decision

Use DuckDB as the embedded OLAP query engine. The database file lives at `data/analytics.duckdb` and is written by the ETL pipeline on startup. All API queries target pre-materialized mart tables to minimise scan cost.

## Consequences

**Benefits:**
- Zero operational overhead — no server, no connection pool, no migration runner needed for CI.
- Sub-millisecond aggregation on <100 K rows with columnar execution.
- Native Polars/Arrow interop: ETL loads DataFrames via `register` without serialization.
- Single-file database makes the whole data layer reproducible from CSV.

**Trade-offs:**
- Single-writer constraint: DuckDB supports one writer at a time. Concurrent writes require serialization via a threading lock (implemented in `core/database.py`).
- Not suitable for OLTP workloads with high write concurrency or row-level locking.
- No built-in replication; backups must copy the `.duckdb` file directly.
