#!/usr/bin/env python3
import sys, yaml, pathlib
p = pathlib.Path(__file__).resolve().parents[1]/"module.yaml"
d = yaml.safe_load(p.read_text(encoding="utf-8")
ko = all(k in d for k in ["name","version","contracts","compatibility","endpoints"])
print("OK" if ko else "INVALID")
sys.exit(0 if ko else 1)