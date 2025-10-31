from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from .logs_core import LogEvent
try:
    import yaml  # type: ignore
except Exception:
    yaml = None

def load_rules_text(inline_yaml: str | None) -> List[Dict[str, Any]]:
    if yaml is None or not inline_yaml:
        return []
    try:
        data = yaml.safe_load(inline_yaml) or {}
        rules = data.get('rules') or []
        return rules if isinstance(rules, list) else []
    except Exception:
        return []

def apply_rules(paths: List[Path], rules: List[Dict[str, Any]]) -> List[LogEvent]:
    out: List[LogEvent] = []
    if not rules:
        return out
    for p in paths:
        if not (p.exists() and p.is_file()):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for r in rules:
                pats = r.get('if_contains') or []
                if not isinstance(pats, list):
                    continue
                for pat in pats:
                    s = str(pat)
                    if s and s.lower() in line.lower():
                        out.append(LogEvent('rule-match', str(p), i, str(r.get('reason') or ('match: '+s)), fix=str(r.get('fix') or ''), severity=str(r.get('severity') or 'info')))
                        break
    return out