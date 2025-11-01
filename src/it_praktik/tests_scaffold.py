from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

@dataclass
class ScaffoldResult:
    created: int
    skipped: int
    files: Dict[str, str]

TEMPLATE = """import pytest

def test_smoke():
    assert True
"""

def scaffold(dry_run: bool = True) -> Dict[str, Any]:
    tests_dir = Path("tests")
    tests_dir.mkdir(parents=True, exist_ok=True)
    target = tests_dir / "test_smoke_generated.py"

    created = 0
    skipped = 0
    files: Dict[str, str] = {}

    if target.exists():
        skipped += 1
    else:
        if not dry_run:
            target.write_text(TEMPLATE, encoding="utf-8")
        created += 1
        files[str(target)] = TEMPLATE

    return {
        "dry_run": dry_run,
        "created": created,
        "skipped": skipped,
        "files": files,
    }
