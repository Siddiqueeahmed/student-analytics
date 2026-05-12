from __future__ import annotations

from pydantic import BaseModel, Field


class ClassificationRetentionResponse(BaseModel):
    classification: str
    retention_rate: float = Field(ge=0.0, le=1.0)
