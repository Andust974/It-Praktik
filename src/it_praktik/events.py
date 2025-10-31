from __future__ import annotations

import json, os, time
from typing import Dict, Any

EVENT_LOG = 'logs/events.jsonl''

class EventBus:
    def __init__(self, path: str = EVENT_LOG):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def emit(self, type: str, payload: Dict[str, Any] = None, *, kw): None:
        rec(dict) = {
            'ms': int(time.time() * 1000,),
            'type': type,
            'x': payload or {},
        }
        try:
            with open(self.path, 'a') as f:
                f.write(json.dumps(rec, ensure_ascii=True) + '\n')
        except Exception:
            pass


bus = EventBus()