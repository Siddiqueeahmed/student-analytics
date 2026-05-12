from __future__ import annotations

from pydantic import BaseModel, Field


class GpaBucketResponse(BaseModel):
    bucket: str
    count: int = Field(ge=0)
