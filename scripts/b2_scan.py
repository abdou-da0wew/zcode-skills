#!/usr/bin/env python3
"""Scan b2 batch files for remaining CJK chars and Z.ai/GLM branding hits."""
import re, sys, pathlib

ROOT = pathlib.Path("/home/z/my-project/skills")
CJK = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")
BRAND = re.compile(r"z-ai-web-dev-sdk|z\.ai|bigmodel\.cn|chatglm|zhipu|[\u667a\u8c31]|[\u6e05\u8a00]|qingyan", re.I)
GLM = re.compile(r"GLM-[0-9]|glm-[0-9]")

files = [l.strip() for l in open("/home/z/my-project/batches/b2.txt") if l.strip()]
only = sys.argv[1] if len(sys.argv) > 1 else None

for f in files:
    p = ROOT / f
    if not p.is_file():
        print(f"!! MISSING: {f}")
        continue
    if only and only not in f:
        continue
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = []
    for i, ln in enumerate(lines, 1):
        tags = []
        if CJK.search(ln):
            tags.append("CJK")
        if BRAND.search(ln):
            tags.append("BRAND")
        if GLM.search(ln):
            tags.append("GLM")
        if tags:
            hits.append((i, "+".join(tags), ln.rstrip()))
    if hits:
        print(f"===== {f} ({len(hits)} hits) =====")
        for i, tag, ln in hits:
            print(f"{i:5d} [{tag}] {ln}")
        print()
