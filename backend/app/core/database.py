"""Thread-safe DuckDB connection singleton."""
from __future__ import annotations

import threading
from contextlib import contextmanager
from collections.abc import Generator

import duckdb

_conn: duckdb.DuckDBPyConnection | None = None
_lock: threading.Lock = threading.Lock()


def init(path: str) -> None:
    """Open the database. No-op if already initialised (allows test injection)."""
    global _conn
    with _lock:
        if _conn is not None:
            return
        _conn = duckdb.connect(path)


def close() -> None:
    """Close and release the connection."""
    global _conn
    with _lock:
        if _conn is not None:
            _conn.close()
            _conn = None


@contextmanager
def cursor() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Yield the shared connection under the global lock."""
    if _conn is None:
        raise RuntimeError("Database not initialised; call init() first")
    with _lock:
        yield _conn
