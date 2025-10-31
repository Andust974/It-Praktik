#!/usr/bin/env bash
set -euo pipefail

# Prepare runtime env for IT Praktik
mkdir -p logs tmp
: ${ITP_LOG_DIR:=logs}
: ${ITP_WEB_ALLOW:=raw.githubusercontent.com,example.com}
: ${ITP_WEB_MAX_BYTES:=1048576}

echo "[attach] LOG_DIR=$ITP_LOG_DIR"
echo "[attach] WEB_ALLOW=$ITP_WEB_ALLOW"
echo "[attach] WEB_MAX_BYTES=$ITP_WEB_MAX_BYTES"

# Example: export minimal token set for tools scope
if [ -z "${ITP_TOKENS:-}" ]; then
  export ITP_TOKENS='{"devtoken":["itp:tools"]}'
  echo "[attach] export ITP_TOKENS for devtoken"
fi

echo "[attach] done"
