from __future__ import annotations
from fastapi  import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
from .grep_dsl import parse_rules_yaml, build_commands, DslError


router = APIRouter(prefix="/grep", tags=["grep"])

class Rules(BaseModel):
    inline_yaml: str
    tool: Literal["rg", "grep"] = "rg"


class GrepSuggestRequest(BaseModel):
    paths: List[str]
    rules: Rules


@router.post("/suggest")
def grep_suggest(req: GrepSuggestRequest):
    try:
        rules = parse_rules_yaml(req.rules.inline_yaml)
        if not rules:
            return {"tool": req.rules.tool, "count": 0, "commands": [], "explain": "no rules matched/parsed"}
        cmds = build_commands(req.paths, rules, tool=req.rules.tool)
        return {"tool": req.rules.tool, "count": len(cmds), "commands": cmds}
    except DslError as e:
        raise HTTPException(status_code=400, detail=str(e))
