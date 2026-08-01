# -*- coding: utf-8 -*-
import json
import subprocess
from pathlib import Path

ROOT = Path(r"C:\Workspace\projects\flowwow-crm\docs\research\crm-course")
ROOT.mkdir(parents=True, exist_ok=True)
(ROOT / "transcripts").mkdir(exist_ok=True)

out = subprocess.check_output(
    [
        "python",
        "-m",
        "yt_dlp",
        "--flat-playlist",
        "--print",
        "%(playlist_index)s\t%(id)s\t%(title)s\t%(duration)s",
        "https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj",
    ],
    text=True,
    encoding="utf-8",
    errors="replace",
)

rows = []
for line in out.strip().splitlines():
    parts = line.split("\t")
    if len(parts) < 3:
        continue
    idx_s, vid, title = parts[0], parts[1], parts[2]
    dur = parts[3] if len(parts) > 3 else None
    try:
        idx = int(idx_s)
    except ValueError:
        continue
    if idx > 31:
        continue
    rows.append(
        {
            "index": idx,
            "video_id": vid,
            "title": title,
            "duration_sec": int(dur) if dur and str(dur).isdigit() else None,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "status": "meta_ok",
            "transcript_status": "blocked_youtube_rate_limit",
            "file": None,
            "chars": 0,
        }
    )

(ROOT / "playlist.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
)

# INDEX
lines = [
    "# CRM Course Index — Lectoria «CRM с нуля»",
    "",
    "Playlist: https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj",
    "",
    f"**Videos 1–31:** {len(rows)} · full transcripts: blocked (YouTube IP/429 from this host).",
    "",
    "| # | Title | ID | Duration | Transcript |",
    "|---|-------|-----|----------|------------|",
]
for e in rows:
    d = e["duration_sec"]
    dm = f"{d // 60}:{d % 60:02d}" if d else "—"
    lines.append(
        f"| {e['index']} | {e['title']} | `{e['video_id']}` | {dm} | {e['transcript_status']} |"
    )
(ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"saved {len(rows)} videos")
for r in rows:
    print(f"{r['index']:02d} {r['video_id']} {r['title'][:72]}")
