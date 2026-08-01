# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

root = Path(r"C:\Workspace\projects\flowwow-crm\docs\research\crm-course")
files = list((root / "transcripts").glob("*.txt"))
print("transcript files", len(files))
text = (root / "ALL_TRANSCRIPTS.md").read_text(encoding="utf-8")
print("ok markers", len(re.findall(r"status: \*\*ok\*\*", text)))
print("fail markers", len(re.findall(r"status: \*\*fail", text, re.I)))
have = set()
for f in files:
    m = re.search(r"([A-Za-z0-9_-]{11})", f.name)
    # better: after NN-
    m2 = re.match(r"\d{2}-([A-Za-z0-9_-]{11})", f.name)
    if m2:
        have.add(m2.group(1))
    elif m:
        have.add(m.group(1))
pl = json.loads((root / "playlist.json").read_text(encoding="utf-8"))
for r in pl:
    st = "OK" if r["video_id"] in have else "MISS"
    print(f"{r['index']:02d} {st} {r['video_id']} {r['title'][:55]}")
print("have", len(have), "of", len(pl))
# total chars
tc = 0
for f in files:
    body = f.read_text(encoding="utf-8", errors="replace")
    tc += len(body)
print("total chars", tc)
