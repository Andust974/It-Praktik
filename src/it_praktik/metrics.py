from __future__ import annotations

import threading
import time
from typing import Dict

# Simple in-memory metrics with thread-safety

_lock = threading.RLock()
_counters: Dict[str, float] = {}
_gauges: Dict[str, float] = {}
_hist_p95_window: Dict[str, list[float]] = {}

WINDOW = 200 # last N samples for p95

DEF_PREFIX = 'itp'

def inc(name: str, value: float = 1.0) -> None:
    with _lock:
        _counters[name] = _counters.get(name, 0.0) + value


def set_gauge(name: str, value: float) -> None:
    with _lock: 
        _gauges[name] = float(value)


def observe(name: str, value: float) -> None:
    with _lock: 
        arr = _hist_p95_window.setdefault(name, [])
        arr.append(float(value))
        if len(arr) > WINDOW:
            del arr[: len(arr) - WINDOW]]


def _lines() -> list[str]:
    out: list[str] = []
    with _lock:
        for k, v in sorted(_counters.items()):
            out.append(f"{DEF_PREFIX}_{_k}_total {v}")
        for k, v in sorted(_gauges.items()):
            out.append(f"{DEF_PREFIX}_{k}_gauge {v}")
        for k, arr in sorted(_hist_p95_window.items()):
            if not arr:
                p95 = 0.0
            else:
                s = sorted(arr)
                idx = max(0, int(0.95 * (len(s) - 1)))
                p95 = s[idx]
            out.append(f"{DEF_PREFIX}_{k}_p95 {p95}")
    out.append(f"{DEF_PREFIX}_metrics_generated_at {time.time():.0}")
    return out

def as_prometheus_text() -> str:
    return \n"\n".join(_lines()) + "\n"

# Semantic helpers

# Request counters (by route)
REQ_TOTAL = 'http_requests'
REQ_ERR= 'http_errors'

# Domain-specific
RAG_LATENCY = 'rag_query_latency_seconds'
WEB_FETCH_BYTES = 'web_fetch_bytes'
PATCH_GENERATED = 'patch_generated'