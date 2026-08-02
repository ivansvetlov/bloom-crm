# -*- coding: utf-8 -*-
from pathlib import Path
import re

idx = Path(r"C:\Workspace\projects\flowwow-crm\docs\index.html").read_text(encoding="utf-8")
print("phase-map", "phase-map" in idx)
print("week open", len(re.findall(r'class="week open"', idx)))
print("week total divs", len(re.findall(r'class="week', idx)))
print("=== WEEKS ===")
for no, title, sub in re.findall(
    r'week-no">(\d+)</div>.*?week-title">(.*?)</div>\s*<div class="week-sub">(.*?)</div>',
    idx,
    re.S,
):
    print(f"{no} | {title} | {sub}")

offer = Path(r"C:\Workspace\projects\flowwow-crm\docs\offer.html").read_text(encoding="utf-8")
print("=== OFFER PHASES ===")
m = re.search(r'panel timeline">(.*?)</div>\s*</section>', offer, re.S)
if m:
    for row in re.findall(
        r'tl-key">(.*?)</div><div class="tl-val">(.*?)<span class="tl-sub">(.*?)</span>',
        m.group(1),
    ):
        print(f"{row[0]} | {row[1]} | {re.sub('<[^>]+>', '', row[2])}")
lede = re.search(r'id="timeline".*?<p class="sec-lede">(.*?)</p>', offer, re.S)
if lede:
    print("LEDE:", re.sub("<[^>]+>", "", lede.group(1))[:220])
