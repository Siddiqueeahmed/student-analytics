"""Students endpoint — returns paginated student records."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from app.models.student import StudentResponse
from app.services import gpa as svc

router = APIRouter(tags=["students"])


@router.get("/students", response_model=list[StudentResponse])
async def list_students(
    limit: Annotated[int, Query(ge=1, le=1000, description="Max rows to return")] = 500,
) -> list[StudentResponse]:
    rows = await svc.list_students(limit=limit)
    return [StudentResponse.model_validate(r) for r in rows]
