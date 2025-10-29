from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from .indexer import IndexProfile, index_repo

router = APIRouter(prefix='/rag', tags=['rag'])

class IndexProfileModel(BaseModel):
    root: Optional[str] = None
    include_glob: Optional[List[str]] = None
    ignore_glob: Optional[List[str]] = None
    max_file_mb: float = Field(2.0, ge=0.1, le=50)
    snapshot_path: str = 'data/index.jsonl'

@router.post('/index')
def rag_index(profile: IndexProfileModel):
    p = IndexProfile(**profile.model_dump())
    res = index_repo(p)
    return res
