"""Retention endpoint — thin async handler, delegates to service."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from app.models.retention import ClassificationRetentionResponse
from app.services import retention as svc

router = APIRouter(tags=["retention"])

_TERM_RE = r"^(Fall|Spring)\d{4}$"


@router.get("/retention/by-classification", response_model=list[ClassificationRetentionResponse])
async def retention_by_classification(
    term: Annotated[
        str | None,
        Query(pattern=_TERM_RE, description="Academic term, e.g. Fall2024"),
    ] = None,
    classification: Annotated[
        list[str] | None,
        Query(description="Filter by one or more classifications"),
    ] = None,
) -> list[ClassificationRetentionResponse]:
    return await svc.by_classification(term=term, classifications=classification)
