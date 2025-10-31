from __future__ import annotations
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET
from .logs_core import LogEvent

def parse_junit_xml(path: Path) -> List[LogEvent]:
    out: List[LogEvent] = []
    if not path.exists():
        return out
    try:
        root = ET.parse(path).getroot()
    except Exception:
        return out
    for case in root.iter('testcase'):
        bad = None
        for child in list(case):
            if child.tag in ('failure','error'):
                bad = child; break
        if bad is not None:
            name = case.get('name') or ''
            cls  = case.get('classname') or ''
            reason = (bad.get('message') or '').strip() or (bad.text or '').strip() or 'test failed'
            out.append(LogEvent('test-failure', str(path), None, f'{cls}::{name} - {reason}', fix='fix failing test', severity='error'))
    return out