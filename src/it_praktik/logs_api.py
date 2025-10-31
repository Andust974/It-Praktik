from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Literal
from .logs_parser import parse_logs
router = APIRouter(prefix='/logs', tags=['logs'])
class Source(BaseModel):
    type: Literal['jsonl','junit','text'] = 'jsonl'
    path: str
class Rules(BaseModel):
    inline_yaml: Optional[str] = None
class LogsParseRequest(BaseModel):
    sources: List[Source]
    rules: Optional[Rules] = None
@router.post('/parse')
def logs_parse(req: LogsParseRequest):
    inline_yaml = req.rules.inline_yaml if req.rules else None
    return parse_logs([s.model_dump() for s in req.sources], inline_rules_yaml=inline_yaml)