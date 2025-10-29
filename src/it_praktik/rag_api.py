from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path
from .rag_bm25 import BM25, load_docs_from_snapshot, best_citation, Doc as TextDoc
from .rag_vector import VectorIndex, Doc as VecDoc

router = APIRouter(prefix='/rag', tags=['rag'])

class QueryModel(BaseModel):
    query: str
    top_k: int = Field(5, ge=1, le=50)
    with_citations: bool = True
    use_vector: bool = False
    snapshot_path: str = 'data/index.jsonl'

@router.post('/query')
def rag_query(req: QueryModel):
    snap = Path(req.snapshot_path)
    docs = load_docs_from_snapshot(snap)
    if not docs:
        return {'hits': [], 'count': 0, 'warning': 'snapshot empty or missing'}

    hits = []
    if req.use_vector:
        vdocs = [VecDoc(d.path, d.text) for d in docs]
        idx = VectorIndex(vdocs)
        results = idx.search(req.query, top_k=req.top_k)
        for i, score in results:
            d = docs[i]
            cite = None
            if req.with_citations:
                ls, le, sn = best_citation(d.text, req.query)
                cite = {'path': d.path, 'start': ls, 'end': le, 'text': sn}
            hits.append({'path': d.path, 'score': float(score), 'citation': cite})
    else:
        bm = BM25(docs)
        results = bm.search(req.query, top_k=req.top_k)
        for i, score in results:
            d = docs[i]
            cite = None
            if req.with_citations:
                ls, le, sn = best_citation(d.text, req.query)
                cite = {'path': d.path, 'start': ls, 'end': le, 'text': sn}
            hits.append({'path': d.path, 'score': float(score), 'citation': cite})

    return {'hits': hits, 'count': len(hits)}
