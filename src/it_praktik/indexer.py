from __future__ import annotations
import fnmatch, hashlib, json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Iterator, Tuple

@dataclass
class IndexProfile:
    root: str | None = None
    include_glob: List[str] | None = None
    ignore_glob: List[str] | None = None
    max_file_mb: float = 2.0
    snapshot_path: str = 'data/index.jsonl'
    def normalized(self, cwd: Path) -> 'IndexProfile':
        inc = self.include_glob or ['**/*.md','**/*.txt','**/*.json','**/*.yaml','**/*.yml','**/*.log','**/*.py','**/*.ts','**/*.js']
        ign = self.ignore_glob or ['**/.git/**','**/.venv/**','**/node_modules/**']
        root = Path(self.root) if self.root else cwd
        return IndexProfile(str(root), inc, ign, self.max_file_mb, self.snapshot_path)

@dataclass
class IndexItem:
    path: str; size: int; mtime: float; sha256: str

@dataclass
class IndexStats:
    total_seen: int=0; total_indexed: int=0; total_bytes: int=0; skipped_size: int=0

_CHUNK = 1048576

def _hash_file(p: Path) -> str:
    h=hashlib.sha256(); f=p.open('rb')
    try:
        while True:
            b=f.read(_CHUNK)
            if not b: break
            h.update(b)
    finally:
        f.close()
    return h.hexdigest()

def _match_any(pats: List[str], rel: str) -> bool:
    return any(fnmatch.fnmatch(rel, pat) for pat in pats)

def iter_paths(root: Path, include: List[str], ignore: List[str]) -> Iterator[Path]:
    for p in (x for x in root.rglob('*') if x.is_file()):
        rel=p.relative_to(root).as_posix()
        if ignore and _match_any(ignore, rel): continue
        if include and not _match_any(include, rel): continue
        yield p

def build_index(profile: IndexProfile) -> Tuple[list[IndexItem], IndexStats]:
    prof=profile.normalized(Path.cwd()); root=Path(prof.root).resolve(); maxb=int(prof.max_file_mb*1048576)
    stats=IndexStats(); items: list[IndexItem]=[]
    for p in iter_paths(root, prof.include_glob, prof.ignore_glob):
        stats.total_seen+=1
        st=p.stat(); size=int(st.st_size)
        if size>maxb: stats.skipped_size+=1; continue
        sha=_hash_file(p)
        items.append(IndexItem(str(p), size, st.st_mtime, sha))
        stats.total_indexed+=1; stats.total_bytes+=size
    return items, stats

def write_snapshot(items: list[IndexItem], snapshot: Path)->None:
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    with snapshot.open('w', encoding='utf-8') as f:
        for it in items: f.write(json.dumps(asdict(it), ensure_ascii=False)+'
')

def index_repo(profile: IndexProfile)->dict:
    items, stats = build_index(profile)
    snap=Path(profile.snapshot_path);
    if not snap.is_absolute(): snap=Path.cwd()/snap
    write_snapshot(items, snap)
    return {
        'stats': asdict(stats),
        'snapshot': str(snap),
        'preview': [asdict(i) for i in items[:5]],
        'count': len(items),
        'bytes': stats.total_bytes
    }
