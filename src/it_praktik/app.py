from fastapi import FastAPI, Request
import time
from collections import deque
from . import __version__
from .rag_api import router as rag_router
from .logs_api import router as logs_router
from .grep_api import router as grep_router
from .tests_api import router as tests_router
from .web_api import router as web_router
from .diff_api import router as diff_router
from .metrics_api import router as metrics_router
from .metrics import observe, RAG_LATENCY, inc, REQ_TOTAL, REQ_ERR

app = FastAPI(title='IT Praktik', version=__version__)

_rag_lat = deque(maxlen=200)

@app.middleware('http')
async def rag_latency_mw(request: Request, call_next):
    inc(REQ_TOTAL, 1)
    start = time.perf_counter()
    try:
        resp = await call_next(request)
        return resp
    except Exception:
        inc(REQ_ERR, 1)
        raise
    finally:
        if request.url.path == '/rag/query':
            dt = time.perf_counter() - start
            _rag_lat.append(dt)
            observe(RAG_LATENCY, dt)

@app.get('/metrics')
def metrics():
    if _rag_lat:
        arr = sorted(_rag_lat)
        idx = max(0, int(0.95 * (len(arr)-1)))
        p95 = arr[idx]
    else:
        p95 = 0.0
    return f'itp_rag_query_latency_p95_seconds {p95:.6f}\n'

@app.get('/health')
def health():
    return {'status': 'ok', 'version': __version__}

@app.get('/ready')
def ready():
    return {'ready': True, 'checks': {'api': True}, 'version': __version__}

app.include_router(rag_router)
app.include_router(logs_router)
app.include_router(grep_router)
app.include_router(tests_router)
app.include_router(web_router)
app.include_router(diff_router)
app.include_router(metrics_router)
