"""FastAPI application entry point — Phase 2: DuckDB-backed."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import enrollment, gpa, retention
from app.core import database
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.request_id import RequestIdMiddleware

configure_logging()
logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("startup", db_path=str(settings.db_path))
    database.init(str(settings.db_path))
    yield
    database.close()
    logger.info("shutdown")


app = FastAPI(
    title="Student Analytics API",
    version="0.2.0",
    description="Enrollment, retention, and GPA analytics for higher-ed data.",
    lifespan=lifespan,
)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(enrollment.router, prefix="/api")
app.include_router(retention.router, prefix="/api")
app.include_router(gpa.router, prefix="/api")


@app.get("/api/health", tags=["ops"])
def health() -> dict[str, str]:
    return {"status": "ok"}
