"""Admin endpoints — ETL refresh, requires admin role."""
from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends

from app.auth.dependencies import require_admin
from app.auth.models import TokenPayload

router = APIRouter(tags=["admin"])


def _run_etl() -> str:
    from app.etl import run as etl_run
    etl_run.run()
    return "ok"


@router.post("/admin/etl/refresh", response_model=dict[str, str])
async def trigger_etl_refresh(
    _: TokenPayload = Depends(require_admin),
) -> dict[str, str]:
    """Re-run the full ETL pipeline (admin only). Invalidates all caches."""
    await asyncio.to_thread(_run_etl)

    from app.services import enrollment, gpa, retention
    enrollment.invalidate_cache()
    retention.invalidate_cache()
    gpa.invalidate_cache()

    return {"status": "ok"}
