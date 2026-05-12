"""Pydantic response model for individual student records."""
from __future__ import annotations

from pydantic import BaseModel, Field


class StudentResponse(BaseModel):
    student_id: int
    term: str
    college: str
    program: str
    classification: str
    gpa: float = Field(ge=0.0, le=4.0)
    credit_hours_attempted: int = Field(ge=0)
    credit_hours_earned: int = Field(ge=0)
    retained_next_term: bool
