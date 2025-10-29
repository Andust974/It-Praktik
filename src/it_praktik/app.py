from fastapi import FastAPI
from . import __version__
from .rag_api import router as rag_router

app = FastAPI(title="IT Praktik", version=__version__)

@app.get('/health')
def health():
    return {'status': 'ok', 'version': __version__}

@app.get('/ready')
def ready():
    return {'ready': True, 'checks': {'api': True}, 'version': __version__}

app.include_router(rag_router)
