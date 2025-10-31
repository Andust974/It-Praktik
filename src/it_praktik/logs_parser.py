from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Set
from .logs_core import LogEvent
from .logs_jsonl import parse_jsonl
from .logs_junit import parse_junit_xml
from .logs_rules import load_rules_text, apply_rules

def parse_logs(sources: List[Dict[str, Any]], inline_rules_yaml: str | None = None) -> Dict[str, Any]:
    events: List[LogEvent] = []; files: Set[str] = set()
    for s in (sources or []):
        t = str(s.get('type') or 'jsonl').lower(); p = Path(str(s.get('path') or ''))
        if not p.exists(): continue
        files.add(str(p))
        if t == 'jsonl': events += parse_jsonl(p)
        elif t == 'junit': events += parse_junit_xml(p)
    rules = load_rules_text(inline_rules_yaml)
    rf = [Path(str(s.get('path'))) for s in (sources or []) if str(s.get('type') or '').lower() in ('jsonl','text')]
    events += apply_rules(rf, rules)
    summ = {'errors': sum(1 for e in events if (e.severity or '').lower()=='error' or e.type in ('test-failure','log-error')),'warnings': sum(1 for e in events if (e.severity or '').lower()=='warning' or e.type=='log-warning'),'rule_matches': sum(1 for e in events if e.type=='rule-match'),'files': len(files),'total': len(events)}
    return {'summary': summ, 'events': [e.to_dict() for e in events]}