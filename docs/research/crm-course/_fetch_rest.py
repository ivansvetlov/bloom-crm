# -*- coding: utf-8 -*-
"""Fetch remaining 25-31 transcripts via yt-dlp auto-subs with delay."""
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(r"C:\Workspace\projects\flowwow-crm\docs\research\crm-course")
TRANS = ROOT / "transcripts"
missing = [
    (25, "tA7F0K8FtU8", "DialogChoose"),
    (26, "_nJTsTcb174", "SignIn-Dashboard"),
    (27, "96bN6ZSW8CA", "Profile"),
    (28, "Fq72fU7m4xg", "Layout-complete"),
    (29, "zXAiNTsPlOQ", "Vue3-TextBox"),
    (30, "YQHT_VIXxkU", "Vue3-Avatar"),
    (31, "SOi0APxsdgE", "Composition-vs-Options"),
]


def vtt_to_text(vtt: str) -> str:
    lines = []
    for line in vtt.splitlines():
        line = line.strip()
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if re.match(r"^\d+$", line):
            continue
        if "-->" in line:
            # keep timestamp of start
            start = line.split("-->")[0].strip().split(".")[0]
            lines.append(f"[{start}] ")
            continue
        # strip tags
        clean = re.sub(r"<[^>]+>", "", line)
        if clean:
            if lines and lines[-1].startswith("["):
                lines[-1] = lines[-1] + clean
            else:
                lines.append(clean)
    # collapse consecutive
    out = []
    prev = None
    for L in lines:
        if L != prev:
            out.append(L)
            prev = L
    return "\n".join(out)


for idx, vid, slug in missing:
    print(f"=== {idx} {vid}")
    outtmpl = str(TRANS / f"{idx:02d}-{vid}-%(id)s.%(ext)s")
    cmd = [
        "python", "-m", "yt_dlp",
        "--skip-download",
        "--write-auto-sub",
        "--sub-lang", "ru",
        "--sub-format", "vtt",
        "--sleep-requests", "2",
        "-o", outtmpl,
        f"https://www.youtube.com/watch?v={vid}",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(p.stdout[-400:] if p.stdout else "")
    print(p.stderr[-500:] if p.stderr else "")
    # find vtt
    vtts = list(TRANS.glob(f"{idx:02d}-{vid}*.vtt")) + list(TRANS.glob(f"*{vid}*.vtt"))
    if not vtts:
        print("  no vtt")
        time.sleep(3)
        continue
    vtt = vtts[0].read_text(encoding="utf-8", errors="replace")
    text = vtt_to_text(vtt)
    txt_path = TRANS / f"{idx:02d}-{vid}-{slug}.txt"
    txt_path.write_text(
        f"# {slug}\n# https://www.youtube.com/watch?v={vid}\n# lang=ru-auto\n\n{text}",
        encoding="utf-8",
    )
    print(f"  saved {txt_path.name} chars={len(text)}")
    time.sleep(2)

print("done")
