# -*- coding: utf-8 -*-
from pathlib import Path
import re, subprocess, tempfile

t = Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html").read_text(encoding="utf-8")
scripts = re.findall(r"<script(?![^>]*src)[^>]*>([\s\S]*?)</script>", t)
s = scripts[-1]
p = Path(tempfile.gettempdir()) / "bloom_demo_check.js"
p.write_text(s, encoding="utf-8")
r = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True)
print("exit", r.returncode)
print(r.stderr or "OK")
for key in ["data-section=\"bookings\"", "id=\"noteModal\"", "function renderBookings", "function openNoteModal", "function saveBookingModal"]:
    print(key, key in t or key in s)
