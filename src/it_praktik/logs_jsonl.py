from __future__ import annotations
from pathlib import Path
from typing import List
import json
from .logs_core import LogEvent

def parse_jsonl(path: Path) -> List[LogEvent]:
    out: List[LogEvent] = []
    if not path.exists():
        return out
    with path.open('r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            lvl = str(obj.get('level') or obj.get('lvl') or obj.get('severity') or '').lower()
            msg = str(obj.get('message') or obj.get('msg') or '')
            if not msg:
                continue
            if lvl in ('error','err','e'):
                out.append(LogEvent('log-error', str(path), i, msg, fix='inspect error', severity='error'))
            elif lvl in ('warn','warning','w'):
                out.append(LogEvent('log-warning', str(path), i, msg, fix='review warning', severity='warning'))
    return out