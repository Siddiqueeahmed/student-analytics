"""GPA distribution endpoint — thin async handler, delegates to service."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from app.models.gpa import GpaBucketResponse
from app.services import gpa as svc

router = APIRouter(tags=["gpa"])

_TERM_RE = r"^(Fall|Spring)\d{4}$"


@router.get("/gpa/distribution", response_model=list[GpaBucketResponse])
async def gpa_distribution(
    term: Annotated[
        str | None,
        Query(pattern=_TERM_RE, description="Academic term, e.g. Fall2024"),
    ] = None,
    classification: Annotated[
        list[str] | None,
        Query(description="Filter by one or more classifications"),
    ] = None,
) -> list[GpaBucketResponse]:
    return await svc.distribution(term=term, classifications=classification)
