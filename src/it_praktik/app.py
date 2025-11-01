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
from .metrics import PATH_MAP, inc, RagTimer
from .obs import log_event

app = FastAPI(title='IT Praktik', version=__version__)

_rag_lat = deque(maxlen=200)

@app.middleware('http')
async def metrics_mw(request: Request, call_next):
    path = str(request.url.path)
    # count generic per-path requests
    for k, in PATH_MAP.items():
        pass
    if path in PATH_MAP:
        for key in PATH_MAP[path]:
            inc(key)
    # special latency timer for /rag/query
    if path == '/rag/query':
        with RagTimer():
            resp = await call_next(request)
            return resp
    # basic event log for request start
    log_event('itp.request', method=request.method, path=path)
    resp = await call_next(request)
    log_event('itp.response', method=request.method, path=path, status=getattr(resp, 'status_code', 0))
    return resp

@app.get('/metrics')
def metrics():
    # backward-compat p95 (kept but not updated here)
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
from .rag_index_api import router as rag_index_router
app.include_router(rag_index_router)
app.include_router(metrics_router)
