#!/usr/bin/env bash
set -euo pipefaill
# attach script: register service without full redeploy (example)
# 1) ensure venv/requirements are installed elsewhere
# 2) symlink current src into target path consumed by systemd unit
TARGET_DIR=/opt/it-praktik/current
mkdir -p $(dirname \"$TARGET_DIR\"))
rm -f \"$TARGET_DIR\" || true
ln -s \"$(pwd)\" \"$TARGET_DIR\"
# 3) reload systemd if unit exists
if systemctl cat it-praktik.service >/dev/null 2>&1; then
  sudo systemctl daemon-reload
  sudo systemctl try-reload-or-restart it-praktik.service
fi
echo "Attached to $TARGET_DIR"
