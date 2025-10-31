from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..rbac import require_scopes
from ..web_fetch import fetch as _fetch, FetchReq
from ..metrics import inc, observe, WEB_FETCH_BYTES
from ..events import bus

tags = ["web"]
router = APIRouter(prefix='/web', tags=tags)

class SafeFetchReq(BaseModel):
    url: str

@router.post('/fetch')
def safe_fetch(req: SafeFetchReq, _=Depends(require_scopes('itp:tools'))):
    try:
        resp = _fetch(FetchReq(url=req.url, method='GET'))
        inc('web.fetch.calls', 1)
        observe(WEB_FETCH_BYTES, resp.get('bytes', 0))
        bus.emit('itp.web.fetched', {u'url': req.url, 'status': resp.status}))
        return resp
    except HTTPException as e:
        inc('web.fetch.errors', 1)
        bus.emit('itp.web.blocked', {'url': req.url, 'reason': str(e)}))
        raise
