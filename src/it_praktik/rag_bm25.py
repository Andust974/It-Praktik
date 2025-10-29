import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

_WORD = re.compile(r'[A-Za-z0-9_]+')

@dataclass
class Doc:
    path: str
    text: str

class BM25:
    def __init__(self, docs: List[Doc], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1; self.b = b; self.docs = docs; self.N = len(docs)
        self.avgdl = 0.0; self.df: Dict[str,int] = defaultdict(int); self.tf: List[Dict[str,int]] = []; self.doc_len: List[int] = []
        self._build()
    @staticmethod
    def _tok(s: str) -> List[str]:
        return [t.lower() for t in _WORD.findall(s)]
    def _build(self) -> None:
        total_len = 0
        for d in self.docs:
            toks = self._tok(d.text)
            c = Counter(toks); self.tf.append(c); self.doc_len.append(len(toks)); total_len += len(toks)
            for w in c.keys(): self.df[w] += 1
        self.avgdl = (total_len / self.N) if self.N else 0.0
    def _idf(self, q: str) -> float:
        n_q = self.df.get(q, 0)
        if n_q == 0: return 0.0
        return math.log(1 + (self.N - n_q + 0.5) / (n_q + 0.5))
    def score(self, i: int, query_toks: List[str]) -> float:
        dl = self.doc_len[i] or 1
        K = self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1))
        s = 0.0; tf_i = self.tf[i]
        for q in query_toks:
            f = tf_i.get(q, 0)
            if f == 0: continue
            idf = self._idf(q); s += idf * (f * (self.k1 + 1)) / (f + K)
        return s
    def search(self, query: str, top_k: int = 5) -> List[Tuple[int,float]]:
        q_toks = [t for t in self._tok(query) if t]
        scores = [(i, self.score(i, q_toks)) for i in range(self.N)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [x for x in scores[:top_k] if x[1] > 0]

import json

def load_docs_from_snapshot(snapshot_path: Path, max_chars: int = 200000) -> List[Doc]:
    docs: List[Doc] = []
    if not snapshot_path.exists(): return docs
    for line in snapshot_path.read_text(encoding='utf-8', errors='ignore').splitlines():
        if not line.strip(): continue
        try:
            obj = json.loads(line); p = Path(obj['path'])
            if not p.exists(): continue
            txt = p.read_text(encoding='utf-8', errors='ignore')[:max_chars]
            docs.append(Doc(str(p), txt))
        except Exception:
            continue
    return docs


def best_citation(text: str, query: str, window: int = 3) -> Tuple[int,int,str]:
    lines = text.splitlines(); toks = set(BM25._tok(query)); best = (0,0,0)
    for i in range(len(lines)):
        for j in range(i, min(len(lines), i+window)):
            chunk = '
'.join(lines[i:j+1]); score = sum(1 for t in toks if t in chunk.lower())
            if score > best[0]: best = (score,i,j)
    start, end = best[1], best[2]; snippet = '
'.join(lines[start:end+1])
    return start+1, end+1, snippet
