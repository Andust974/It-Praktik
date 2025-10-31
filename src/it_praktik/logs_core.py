from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any
@dataclass
class LogEvent:
    type: str
    file: str
    line: int | None
    reason: str
    fix: str | None = None
    severity: str | None = None
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)