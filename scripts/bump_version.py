#!/usr/bin/env python3
import sys, re, pathlib
v = sys.argv[1]
r = pathlib.Path(__file__).resolve().parents[1]
pairs = [
    (r/'src/it_praktik/__init__.py', r'__version__\\s*=\\s*\\".*\\"', f'__version__ = \\"${v}\\"'),
    (r/'pyproject.toml', r"^version\\s*=\\s*\".*\\"', f'\"version\" = \\"${v}\\"'),
    (r/'module.yaml', r"^version:\\s*.*$', f"version: {v}")
]
for p, pat, rep in pairs:
    s = p.read_text(encoding="utf-8")
    s = re.sub(pat, rep, s, flags=re.M)
    p.write_text(s, encoding="utf-8")
print("OK")