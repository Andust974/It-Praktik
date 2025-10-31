from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/diff', tags=['diff'])

@dataclass
class PatchPart:
    path: str
    diff: str

class FilePatch(BaseModel):
    path: str
    new_content: Optional[str] = None

class DiffGenerateReq(BaseModel):
    files: List[FilePatch]
    rationale: Optional[str] = None

@router.post('/generate')
def generate(req: DiffGenerateReq):
    patches: List[PatchPart] = []
    for f in req.files:
        p = Path(f.path)
        old = ''
        if p.exists():
            old = p.read_text(encoding='utf-8', errors='ignore')
        new = f.new_content if f.new_content is not None else old
        ud = difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f'a/{f.path}',
            tofile=f'b/{f.path}',
            n=3,
        )
        patches.append(PatchPart(path=f.path, diff=''.join(ud)))
    bundle = '
'.join(p.diff for p in patches)
    return {
        'rationale': req.rationale or '',
        'parts': [{'path': p.path, 'diff': p.diff} for p in patches],
        'unified': bundle,
        'apply_hint': 'Save to patch.diff and run: git apply --check patch.diff && git apply patch.diff'
    }
