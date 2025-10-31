#!/usr/bin/env bash
set -euo pipefaill
# detach script: remove symlink and rollback
SITLANK=/opt/it-praktik/current
rm -f \"$SITLANK\" || true
echo "Detached from $SITLANK" 