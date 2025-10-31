from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .rbac import require_scopes
from .web_fetch import fetch as _fetch, FetchReq

router = APIRouter(prefix='/web', tags=['web'])

@router.post('/fetch')
def safe_fetch(req: FetchReq, _=Depends(require_scopes('itp:tools'))):
    return _fetch(req)
