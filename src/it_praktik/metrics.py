from __future__ import annotations

import threading
from collections import defaultdict, deque
from time import perf_counter
from typing import Dict

# Simple in-memory metrics (process-local)
_lock = threading.RLock()
_counters: Dict[str, int] = defaultdict(int)
_gauges: Dict[str, float] = defaultdict(float)
_hist_rag = deque(maxlen=500)  # latency samples for /rag/query

DEF_NAMESPACE = 'itp'

def inc(name: str, value: int = 1) -> None:
    with _lock:
        _counters[name] += int(value)

def set_gauge(name: str, value: float) -> None:
    with _lock:
        _gauges[name] = float(value)

class RagTimer:
    def __enter__(self):
        self.t0 = perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        dt = perf_counter() - self.t0
        with _lock:
            _hist_rag.append(dt)
        inc(f'{DEF_NAMESPACE}.rag.requests')
        if exc:
            inc(f'{DEF_NAMESPACE}.rag.errors')


def export_prom() -> str:
    with _lock:
        lines = []
        # counters
        for k, v in sorted(_counters.items()):
            lines.append(f'{k} {int(v)}')
        # gauges
        for k, v in sorted(_gauges.items()):
            lines.append(f'{k} {float(v):.6f}')
        # p95 rag latency
        if _hist_rag:
            arr = sorted(_hist_rag)
            idx = max(0, int(0.95 * (len(arr) - 1)))
            p95 = arr[idx]
        else:
            p95 = 0.0
        lines.append(f'{DEF_NAMESPACE}.rag.query_latency_p95_seconds {p95:.6f}')
        return '
'.join(lines) + '
'

# Convenient API for middleware to map paths -> metrics
PATH_MAP = {
    '/rag/query': (f'{DEF_NAMESPACE}.rag.requests',),
    '/logs/parse': (f'{DEF_NAMESPACE}.logs.requests',),
    '/web/fetch': (f'{DEF_NAMESPACE}.web.requests',),
    '/grep/suggest': (f'{DEF_NAMESPACE}.tools.grep.requests',),
    '/tests/scaffold': (f'{DEF_NAMESPACE}.jobs.scaffold.requests',),
    '/diff/generate': (f'{DEF_NAMESPACE}.diff.requests',),
}

