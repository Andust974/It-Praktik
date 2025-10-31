#!/usr/bin/env bash
set -euo pipefail

echo '[detach] nothing to stop; ensure your process manager handles service stop'
rm -rf tmp/.cache 2>/dev/null || true
echo '[detach] done'
