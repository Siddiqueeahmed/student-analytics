"""Enrollment endpoint — thin handler, delegates to service."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from app.models.enrollment import CollegeEnrollmentResponse
from app.services import enrollment as svc

router = APIRouter(tags=["enrollment"])

_TERM_RE = r"^(Fall|Spring)\d{4}$"


@router.get("/enrollment/by-college", response_model=list[CollegeEnrollmentResponse])
def enrollment_by_college(
    term: Annotated[
        str | None,
        Query(pattern=_TERM_RE, description="Academic term, e.g. Fall2024"),
    ] = None,
    classification: Annotated[
        list[str] | None,
        Query(description="Filter by one or more classifications"),
    ] = None,
) -> list[CollegeEnrollmentResponse]:
    return svc.by_college(term=term, classifications=classification)
