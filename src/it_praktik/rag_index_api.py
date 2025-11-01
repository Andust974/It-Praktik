from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .rag_bm25 import build_snapshot

router = APIRouter(prefix="/rag", tags=["rag"])

class IndexReq(BaseModel):
    root: Optional[str] = "."
    include: List[str] = ["**/*.py", "**/*.md", "**/*.txt"]
    ignore: List[str] = ["**/.venv/**", "**/__pycache__/**", "**/.git/**"]
    out: Optional[str] = ".cache/rag_snapshot.json"

@router.post("/index")
def index(req: IndexReq):
    root = Path(req.root or ".").resolve()
    out = Path(req.out or ".cache/rag_snapshot.json")
    try:
        payload = build_snapshot(root, req.include, req.ignore, out)
        return {"ok": True, "snapshot": str(out), "total": payload.get("total", 0)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"index error: {e}")
