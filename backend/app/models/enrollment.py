from __future__ import annotations

from pydantic import BaseModel, Field


class CollegeEnrollmentResponse(BaseModel):
    college: str
    count: int = Field(ge=0)
