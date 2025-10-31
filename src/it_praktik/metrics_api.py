from __future__ import annotations

from fastapi import APIRouter, Response
from .metrics import export_prom

router = APIRouter(prefix='/metrics', tags=['metrics'])

@router.get('/export')
def export():
    text = export_prom()
    return Response(content=text, media_type='text/plain; version=0.0.4')
