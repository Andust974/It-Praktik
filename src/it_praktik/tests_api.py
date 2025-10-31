from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from .tests_scaffold import scaffold

router = APIRouter(prefix='/tests', tags=['tests'])

class ScaffoldReq(BaseModel):
    mode: Literal['dry-run','write'] = 'dry-run'

@router.post('/scaffold')
def tests_scaffold(req: ScaffoldReq):
    try:
        res = scaffold(dry_run=(req.mode=='dry-run'))
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
