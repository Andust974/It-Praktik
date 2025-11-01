def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_ready(client):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json().get("ready") is True

def test_metrics(client):
    r = client.get("/metrics/export")
    assert r.status_code == 200
    assert "itp.rag.query_latency_p95_seconds" in r.text
