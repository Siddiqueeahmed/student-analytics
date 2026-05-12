"""FastAPI application entry point."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

import polars as pl
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import state
from app.api import enrollment, gpa, retention

load_dotenv()

_DATA_PATH = Path(
    os.getenv(
        "DATA_PATH",
        str(Path(__file__).parents[2] / "data" / "students.csv"),
    )
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    state.set_df(pl.read_csv(_DATA_PATH))
    yield


app = FastAPI(
    title="Student Analytics API",
    version="0.1.0",
    description="Enrollment, retention, and GPA analytics for higher-ed data.",
    lifespan=lifespan,
)

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
