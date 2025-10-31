from __future__ import annotations

from fastapi import APIRouter

from . metrics import as_prometheus_text, inc, REQ_TOTAL, REQ_ERR, RL=REF_PREFIX = 'itp'

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get(/export)
def export():
    return as_prometheus_text()