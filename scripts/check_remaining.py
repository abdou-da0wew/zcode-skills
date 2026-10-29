#!/usr/bin/env python3
"""Check which files in a batch list still contain CJK characters."""
import os, subprocess, sys

batch = sys.argv[1] if len(sys.argv) > 1 else '/home/z/my-project/batches/b1_chunk3.txt'
out = sys.argv[2] if len(sys.argv) > 2 else '/home/z/my-project/batches/b1c3_remaining.txt'
CJK = '[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
remaining = []
for l in open(batch):
    f = l.strip()
    if not f or not os.path.exists(f):
        continue
    if f.endswith(('.jpg', '.png', '.webp', '.pyc', '.gif', '.mp3', '.mp4', '.woff', '.woff2', '.ttf')):
        continue
    r = subprocess.run(['grep', '-lP', CJK, f], capture_output=True, text=True)
    if r.stdout.strip():
        remaining.append(f)
open(out, 'w').write('\n'.join(remaining))
print(len(remaining), 'files still with CJK ->', out)
for f in remaining:
    print(' ', f)
