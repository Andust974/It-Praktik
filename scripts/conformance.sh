#!/usr/bin/env bash
set -euo pipefail
BASE=${BASE:-http://127.0.0.1:8000}

echo "[conformance] /health"
curl -fsS $BASE/health >/dev/null

echo "[conformance] /ready"
curl -fsS $BASE/ready >/dev/null

echo "[conformance] /metrics/export"
curl -fsS $BASE/metrics/export | grep -q 'itp.rag.query_latency_p95_seconds'

echo "[conformance] basic checks OK"
