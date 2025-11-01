from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

class DslError(Exception):
    pass

@dataclass
class Rule:
    name: str
    if_contains: List[str]
    severity: str = "info"
    reason: Optional[str] = None
    fix: Optional[str] = None
    flags: List[str] = None

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Rule":
        if "name" not in d or "if_contains" not in d:
            raise DslError("rule must have 'name' and 'if_contains'")
        flags = d.get("flags") or []
        if not isinstance(flags, list):
            raise DslError("flags must be list")
        return Rule(
            name=str(d["name"]),
            if_contains=[str(x) for x in d["if_contains"]],
            severity=str(d.get("severity", "info")),
            reason=d.get("reason"),
            fix=d.get("fix"),
            flags=flags,
        )

@dataclass
class Rules:
    rules: List[Rule]


def parse_rules_yaml(inline_yaml: str) -> Rules:
    try:
        import yaml  # lazy import to avoid hard dep at import-time
        data = yaml.safe_load(inline_yaml) or {}
    except ModuleNotFoundError as e:
        raise DslError("PyYAML is required to parse rules. Install pyyaml.") from e
    except Exception as e:
        raise DslError(f"YAML parse error: {e}")
    if not isinstance(data, dict) or "rules" not in data:
        raise DslError("YAML must contain 'rules' list")
    rules = [Rule.from_dict(x) for x in (data.get("rules") or [])]
    return Rules(rules=rules)


def build_commands(paths: List[str], rules: Rules, tool: str = "rg") -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in rules.rules:
        if not r.if_contains:
            continue
        if tool == "rg":
            pats = "|".join([f"{p}" for p in r.if_contains])
            cmd = ["rg", "-n", "-H"] + (r.flags or []) + [f"({pats})"] + paths
        else:
            pats = r.if_contains[0] if len(r.if_contains) == 1 else "\|".join(r.if_contains)
            cmd = ["grep", "-R", "-n", "-H"] + (r.flags or []) + [pats] + paths
        out.append({
            "name": r.name,
            "severity": r.severity,
            "reason": r.reason,
            "fix": r.fix,
            "cmd": cmd,
        })
    return out
