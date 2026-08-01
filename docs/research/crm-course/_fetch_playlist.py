# -*- coding: utf-8 -*-
"""Fetch YouTube playlist metadata + transcripts (ru preferred)."""
import json
import re
import time
import urllib.request
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

ROOT = Path(r"C:\Workspace\projects\flowwow-crm\docs\research\crm-course")
TRANS = ROOT / "transcripts"
ROOT.mkdir(parents=True, exist_ok=True)
TRANS.mkdir(parents=True, exist_ok=True)

PLAYLIST = "https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj"
MAX_VIDEOS = 31


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def parse_playlist(html: str):
    m = re.search(r"ytInitialData\s*=\s*(\{.+?\});</script>", html)
    if not m:
        m = re.search(r"var ytInitialData = (\{.*?\});", html)
    if not m:
        raise RuntimeError("ytInitialData not found")
    data = json.loads(m.group(1))
    videos = []

    def walk(o):
        if isinstance(o, dict):
            if "playlistVideoRenderer" in o:
                r = o["playlistVideoRenderer"]
                vid = r.get("videoId")
                t = r.get("title") or {}
                title = ""
                if t.get("runs"):
                    title = t["runs"][0].get("text", "")
                elif "simpleText" in t:
                    title = t["simpleText"]
                idx = None
                ix = r.get("index") or {}
                if "simpleText" in ix:
                    idx = ix["simpleText"]
                elif ix.get("runs"):
                    idx = ix["runs"][0].get("text")
                videos.append({"index": idx, "video_id": vid, "title": title})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for i in o:
                walk(i)

    walk(data)
    seen = set()
    out = []
    for v in videos:
        if v["video_id"] and v["video_id"] not in seen:
            seen.add(v["video_id"])
            out.append(v)
    return out


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s\-а-яА-ЯёЁ]+", "", s, flags=re.U)
    s = re.sub(r"\s+", "-", s.strip())[:60]
    return s or "video"


def get_transcript(video_id: str):
    api = YouTubeTranscriptApi()
    # v1.2.x style
    try:
        # list + find preferred
        tl = api.list(video_id)
        for langs in (["ru"], ["en"], None):
            try:
                if langs is None:
                    # first available
                    for t in tl:
                        fetched = t.fetch()
                        return fetched, getattr(t, "language_code", "?")
                else:
                    t = tl.find_transcript(langs)
                    fetched = t.fetch()
                    return fetched, getattr(t, "language_code", langs[0])
            except Exception:
                continue
    except Exception as e1:
        # fallback older API
        try:
            from youtube_transcript_api import YouTubeTranscriptApi as Y
            data = Y.get_transcript(video_id, languages=["ru", "en"])
            return data, "legacy"
        except Exception as e2:
            raise RuntimeError(f"{e1} | {e2}")
    raise RuntimeError("no transcript")


def segments_to_text(segments) -> str:
    lines = []
    # FetchedTranscript may be iterable of snippets
    for s in segments:
        if hasattr(s, "text"):
            start = getattr(s, "start", 0) or 0
            text = s.text
        elif isinstance(s, dict):
            start = s.get("start", 0) or 0
            text = s.get("text", "")
        else:
            continue
        m, sec = divmod(int(start), 60)
        h, m = divmod(m, 60)
        ts = f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"
        lines.append(f"[{ts}] {text.replace(chr(10), ' ').strip()}")
    return "\n".join(lines)


def main():
    print("Fetching playlist…")
    html = fetch_html(PLAYLIST)
    videos = parse_playlist(html)
    videos = videos[:MAX_VIDEOS]
    print(f"Found {len(videos)} videos")

    results = []
    for i, v in enumerate(videos, 1):
        vid = v["video_id"]
        title = v["title"] or vid
        print(f"[{i}/{len(videos)}] {vid} {title[:50]}")
        entry = {
            "index": i,
            "playlist_index": v.get("index"),
            "video_id": vid,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "status": "pending",
            "lang": None,
            "chars": 0,
            "file": None,
            "error": None,
        }
        try:
            segs, lang = get_transcript(vid)
            text = segments_to_text(segs)
            slug = slugify(title)
            fname = f"{i:02d}-{vid}-{slug}.txt"
            path = TRANS / fname
            header = f"# {title}\n# {entry['url']}\n# lang={lang}\n\n"
            path.write_text(header + text, encoding="utf-8")
            entry["status"] = "ok"
            entry["lang"] = lang
            entry["chars"] = len(text)
            entry["file"] = str(path.name)
            print(f"  OK {len(text)} chars lang={lang}")
        except Exception as e:
            entry["status"] = "failed"
            entry["error"] = str(e)[:300]
            print(f"  FAIL {e}")
        results.append(entry)
        time.sleep(0.6)

    (ROOT / "playlist.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # INDEX
    lines = ["# CRM Course Index\n", "| # | Title | ID | Status | Chars | File |", "|---|-------|-----|--------|-------|------|"]
    for e in results:
        lines.append(
            f"| {e['index']} | {e['title'][:80]} | `{e['video_id']}` | {e['status']} | {e['chars']} | {e.get('file') or e.get('error','')[:40]} |"
        )
    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ALL_TRANSCRIPTS condensed
    parts = ["# All transcripts (condensed)\n"]
    for e in results:
        parts.append(f"\n## {e['index']}. {e['title']}\n")
        parts.append(f"- url: {e['url']}\n- status: {e['status']} · lang: {e.get('lang')} · chars: {e['chars']}\n")
        if e["status"] == "ok" and e.get("file"):
            body = (TRANS / e["file"]).read_text(encoding="utf-8")
            # strip header
            body = re.sub(r"^#.*\n", "", body, count=3, flags=re.M)
            parts.append("```\n" + body[:3500] + ("\n…\n" if len(body) > 3500 else "") + "\n```\n")
        else:
            parts.append(f"_failed: {e.get('error')}_\n")
    (ROOT / "ALL_TRANSCRIPTS.md").write_text("".join(parts), encoding="utf-8")

    ok = sum(1 for e in results if e["status"] == "ok")
    print(f"DONE ok={ok}/{len(results)} total_chars={sum(e['chars'] for e in results)}")


if __name__ == "__main__":
    main()
