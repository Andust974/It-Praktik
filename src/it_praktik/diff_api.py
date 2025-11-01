from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import difflib

router = APIRouter(prefix="/diff", tags=["diff"])

class DiffReq(BaseModel):
    base: str
    new: str
    filename: str | None = "file.txt"

@router.post("/generate")
def generate(req: DiffReq):
    try:
        base_lines = req.base.splitlines(keepends=True)
        new_lines = req.new.splitlines(keepends=True)
        patch = difflib.unified_diff(
            base_lines,
            new_lines,
            fromfile=f"a/{req.filename}",
            tofile=f"b/{req.filename}",
        )
        bundle = "".join(patch)
        return {"bundle": bundle}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"diff error: {e}")
