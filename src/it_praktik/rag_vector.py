from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import math

# Simple hashing embeddings (no external deps)
DIM = 256

@dataclass
class Doc:
    path: str
    text: str

class EmbeddingsProvider:
    def embed(self, text: str) -> List[float]:
        raise NotImplementedError

class HashEmbeddings(EmbeddingsProvider):
    def embed(self, text: str) -> List[float]:
        v = [0.0]*DIM
        for tok in text.split():
            h = hash(tok) % DIM
            v[h] += 1.0
        # l2 normalize
        norm = math.sqrt(sum(x*x for x in v)) or 1.0
        return [x/norm for x in v]

class VectorIndex:
    def __init__(self, docs: List[Doc], provider: EmbeddingsProvider | None = None):
        self.docs = docs
        self.provider = provider or HashEmbeddings()
        self.vecs = [self.provider.embed(d.text) for d in docs]

    @staticmethod
    def _cos(a: List[float], b: List[float]) -> float:
        return sum(x*y for x,y in zip(a,b))

    def search(self, query: str, top_k: int = 5) -> List[Tuple[int,float]]:
        qv = self.provider.embed(query)
        scores = [(i, self._cos(qv, v)) for i, v in enumerate(self.vecs)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
