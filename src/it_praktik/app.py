from fastapi import FastAPI
from it_praktik import __version__

app = FastAPI(title="IT Praktik", version=__version__)

@app.get("/health")
def health():
    return {"status": "ok", "version": __version__}

@app.get("/ready")
def ready():
    checks = {
        "api": True,
        "cli": True,
    }
    is_ready = all(checks.values())
    return {"ready": is_ready, "checks": checks, "version": __version__}
