# -*- coding: utf-8 -*-
from pathlib import Path
import re

offer = Path(r"C:\Workspace\projects\flowwow-crm\docs\offer.html").read_text(encoding="utf-8")
m = re.search(r'panel timeline">(.*?)</div>\s*</section>', offer, re.S)
print("=== TIMELINE (offer/landing) ===")
if m:
    for row in re.findall(
        r'tl-key">(.*?)</div><div class="tl-val">(.*?)<span class="tl-sub">(.*?)</span>',
        m.group(1),
    ):
        print(f"{row[0]} | {row[1]} | {row[2]}")

idx = Path(r"C:\Workspace\projects\flowwow-crm\docs\index.html").read_text(encoding="utf-8")
print()
print("=== WEEKS (index) ===")
for no, title, sub in re.findall(
    r'week-no">(\d+)</div>.*?week-title">(.*?)</div>\s*<div class="week-sub">(.*?)</div>',
    idx,
    re.S,
):
    print(f"{no} | {title} | {sub}")
