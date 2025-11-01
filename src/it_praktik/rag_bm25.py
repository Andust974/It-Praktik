from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict
import json
import re
from fnmatch import fnmatch

@dataclass
class Doc:
    path: str
    line: int
    text: str

def _tokenize(s: str) -> List[str]:
    return re.findall(r"[a-zA-Zа-яА-Я0-9_]{2,}", s.lower())

class BM25:
    def __init__(self, docs: List[Doc], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs = docs
        self.avgdl = 0.0
        self.df: Dict[str, int] = {}
        self.tf: List[Dict[str, int]] = []
        self.N = 0
        self._build()

    def _build(self) -> None:
        lengths = []
        for d in self.docs:
            toks = _tokenize(d.text)
            counts: Dict[str, int] = {}
            for t in toks:
                counts[t] = counts.get(t, 0) + 1
            self.tf.append(counts)
            lengths.append(len(toks))
            for t in counts:
                self.df[t] = self.df.get(t, 0) + 1
        self.avgdl = (sum(lengths) / len(lengths)) if lengths else 0.0
        self.N = len(self.docs)

    def _idf(self, t: str) -> float:
        n = self.df.get(t, 0)
        return max(0.0, ((self.N - n + 0.5) / (n + 0.5))) if self.N else 0.0

    def score(self, q: str, idx: int) -> float:
        qterms = _tokenize(q)
        tf = self.tf[idx]
        dl = sum(tf.values()) or 1
        score = 0.0
        for t in qterms:
            f = tf.get(t, 0)
            if not f:
                continue
            idf = self._idf(t)
            denom = f + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1))
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def topk(self, q: str, k: int = 5) -> List[Tuple[float, Doc]]:
        scored = [(self.score(q, i), self.docs[i]) for i in range(len(self.docs))]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:k]

def load_docs_from_snapshot(snapshot: Path) -> List[Doc]:
    data = json.loads(snapshot.read_text(encoding="utf-8"))
    out: List[Doc] = []
    for item in data.get("docs", []):
        out.append(Doc(path=item["path"], line=item["line"], text=item["text"]))
    return out

def best_citation(query: str, bm25: BM25, k: int = 3):
    res = []
    for score, d in bm25.topk(query, k=k):
        res.append({"path": d.path, "line": d.line, "score": score, "text": d.text})
    return res

def build_snapshot(root: Path, includes: List[str], ignores: List[str], out: Path):
    all_files: List[Path] = []
    for pat in includes:
        for p in root.rglob(pat):
            if p.is_file():
                all_files.append(p)

    def _ignored(p: Path) -> bool:
        rel = str(p.relative_to(root))
        return any(fnmatch(rel, g) for g in ignores)

    docs: List[Dict] = []
    for p in all_files:
        if _ignored(p):
            continue
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            line_s = line.strip()
            if not line_s:
                continue
            if len(line_s) > 1000:
                line_s = line_s[:1000]
            docs.append({"path": str(p), "line": i, "text": line_s})

    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"root": str(root), "docs": docs, "total": len(docs)}
    out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload
