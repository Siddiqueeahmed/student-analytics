"""FastAPI application entry point — Phase 3: async, auth, observability."""
from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api import admin, auth, enrollment, gpa, meta, retention, students
from app.core import database
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.telemetry import configure_tracing
from app.middleware.request_id import RequestIdMiddleware

configure_logging()
logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("startup", db_path=str(settings.db_path))
    database.init(str(settings.db_path))
    yield
    database.close()
    logger.info("shutdown")


app = FastAPI(
    title="Student Analytics API",
    version="0.3.0",
    description="Enrollment, retention, and GPA analytics for higher-ed data.",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(enrollment.router, prefix="/api")
app.include_router(retention.router, prefix="/api")
app.include_router(gpa.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(meta.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

# Prometheus /metrics (mounted as sub-app so it doesn't appear in OpenAPI)
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

configure_tracing(app)


@app.get("/api/health", tags=["ops"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
