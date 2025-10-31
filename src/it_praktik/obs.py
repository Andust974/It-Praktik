from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

LOG_DIR = Path(os.getenv('ITP_LOG_DIR', 'logs'))
LOG_FILE = LOG_DIR / 'itp.jsonl'

LOG_DIR.mkdir(parents=True, exist_ok=True)

# Structured JSONL writer (best-effort, process-local)

def log_event(ev_type: str, *, level: str = 'INFO', **fields: Any) -> None:
    rec: Dict[str, Any] = {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
        'type': ev_type,
        'level': level,
    }
    rec.update(fields)
    try:
        with LOG_FILE.open('a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '
')
    except Exception as e:
        # last resort
        sys.stderr.write(f'[obs] write failed: {e}
')

