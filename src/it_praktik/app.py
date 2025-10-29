from fastapi import FastAPI, Request
import time
from collections import deque
from . import __version__
from .rag_api import router as rag_router

app = FastAPI(title='IT Praktik', version=__version__)

# --- Metrics (rag query p95) ---
_rag_lat = deque(maxlen=200)

@app.middleware('http')
async def rag_latency_mw(request: Request, call_next):
    if request.url.path == '/rag/query':
        t0 = time.perf_counter()
        resp = await call_next(request)
        dt = time.perf_counter() - t0
        _rag_lat.append(dt)
        return resp
    return await call_next(request)

@app.get('/metrics')
def metrics():
    if _rag_lat:
        arr = sorted(_rag_lat)
        idx = max(0, int(0.95 * (len(arr)-1)))
        p95 = arr[idx]
    else:
        p95 = 0.0
    # Prometheus-like text
    body = f'itp_rag_query_latency_p95_seconds {p95:.6f}
'
    return body

@app.get('/health')
def health():
    return {'status': 'ok', 'version': __version__}

@app.get('/ready')
def ready():
    return {'ready': True, 'checks': {'api': True}, 'version': __version__}

app.include_router(rag_router)
