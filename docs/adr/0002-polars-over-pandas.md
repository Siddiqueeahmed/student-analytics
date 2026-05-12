# ADR 0002 — Polars over pandas

**Status:** Accepted  
**Date:** 2026-05-12

## Context

The ETL pipeline needs to read a CSV file, validate and type-cast columns, and load the result into DuckDB. Both pandas and Polars can perform these operations. The question is which library better fits the project's constraints.

pandas has dominated Python data science for 15 years and has extensive ecosystem support. However, it relies on NumPy's row-oriented memory layout, uses Python objects for nullable columns, and has a mutating API that encourages defensive copies. For a pipeline that reads once and loads into a database, pandas' OLTP-friendly design is a poor match.

Polars is built on Apache Arrow, uses a lazy execution engine, and exposes an immutable, expression-based API. Its scan → filter → select pattern is functionally pure and easy to test. Polars DataFrames can be passed directly to DuckDB via the Arrow interface without serialization, eliminating a copy step that pandas cannot avoid.

## Decision

Use Polars exclusively for all DataFrame operations in the ETL pipeline. pandas is not installed.

## Consequences

**Benefits:**
- 3–10× faster CSV ingest and filter compared to pandas on the same hardware.
- Arrow-native handoff to DuckDB (`conn.register("students", df)`) avoids round-trip through Python objects.
- Immutable expression API prevents accidental in-place mutation bugs that are common in pandas pipelines.
- Type annotations work cleanly: `pl.DataFrame`, `pl.LazyFrame`, and `pl.Series` are concrete types.

**Trade-offs:**
- Smaller ecosystem than pandas; some third-party libraries assume pandas input.
- Expression API has a learning curve for engineers familiar with pandas' index-based API.
- Polars' schema inference occasionally differs from pandas on edge cases (e.g., mixed-type CSV columns).
