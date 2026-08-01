#!/usr/bin/env python3
"""Fetch playlist transcripts 1..31 for CRM course. Writes only under crm-course/."""
from __future__ import annotations

import json
import re
import time
import traceback
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

ROOT = Path(__file__).resolve().parent
TRANSCRIPTS = ROOT / "transcripts"
RAW = ROOT / "playlist_raw.json"
MAX_INDEX = 31  # inclusive 1..31
BATCH = 4
DELAY = 1.2  # seconds between videos
BATCH_PAUSE = 2.5


def slugify(title: str, max_len: int = 50) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    if not s:
        s = "video"
    return s[:max_len].rstrip("-")


def format_ts(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def pick_and_fetch(api: YouTubeTranscriptApi, video_id: str):
    """Prefer ru, then en, else first available. Returns (lang, segments, language_name)."""
    # Try preferred languages first via fetch
    for langs in (["ru"], ["en"]):
        try:
            result = api.fetch(video_id, languages=langs)
            segs = [
                {"text": seg.text, "start": seg.start, "duration": seg.duration}
                for seg in result
            ]
            lang = getattr(result, "language_code", langs[0])
            return lang, segs, getattr(result, "language", lang)
        except Exception:
            pass

    # Any available via list
    try:
        tlist = api.list(video_id)
        # Prefer manual over generated, ru/en first
        transcripts = list(tlist)
        def score(t):
            code = (t.language_code or "").lower()
            gen = 1 if getattr(t, "is_generated", False) else 0
            prio = 0 if code.startswith("ru") else (1 if code.startswith("en") else 2)
            return (prio, gen)

        transcripts.sort(key=score)
        if not transcripts:
            raise NoTranscriptFound(video_id, [], None)
        t = transcripts[0]
        fetched = t.fetch()
        segs = [
            {"text": seg.text, "start": seg.start, "duration": seg.duration}
            for seg in fetched
        ]
        return t.language_code, segs, t.language
    except Exception as e:
        raise e


def segments_to_text(segs) -> str:
    lines = []
    for seg in segs:
        text = (seg["text"] or "").replace("\n", " ").strip()
        if not text:
            continue
        lines.append(f"{format_ts(seg['start'])} {text}")
    return "\n".join(lines)


def plain_text(segs) -> str:
    return " ".join((s["text"] or "").replace("\n", " ").strip() for s in segs if s.get("text"))


def extract_takeaways(title: str, text: str, max_bullets: int = 6) -> list[str]:
    """Heuristic takeaways from transcript text (Russian-friendly)."""
    if not text or len(text.strip()) < 80:
        return ["нет субтитров"]

    # Split into sentences-ish
    chunks = re.split(r"(?<=[.!?…])\s+|\n+", text)
    chunks = [c.strip() for c in chunks if c and len(c.strip()) > 40]

    # Prefer chunks with informative keywords
    keywords = [
        "crm", "тз", "техническ", "компонент", "дизайн", "figma", "бэм", "bem",
        "vue", "прототип", "интерфейс", "dashboard", "страниц", "верстк",
        "стиль", "переменн", "api", "реактив", "state", "form", "button",
        "textbox", "layout", "разработ", "пользовател", "заказ", "клиент",
        "схем", "диаграмм", "архитектур", "систем", "проект", "задач",
        "//", "важно", "нужно", "созда", "добав", "настро", "рассмотр",
    ]
    scored = []
    for c in chunks:
        cl = c.lower()
        score = sum(1 for k in keywords if k in cl)
        # penalize very long or very short
        if len(c) > 400:
            score -= 1
        scored.append((score, c))

    scored.sort(key=lambda x: (-x[0], -min(len(x[1]), 200)))
    picked = []
    seen = set()
    for score, c in scored:
        # normalize for dedup
        key = re.sub(r"\s+", " ", c.lower())[:80]
        if key in seen:
            continue
        seen.add(key)
        # clean for bullet
        bullet = re.sub(r"\s+", " ", c).strip()
        if len(bullet) > 220:
            bullet = bullet[:217].rstrip() + "…"
        picked.append(bullet)
        if len(picked) >= max_bullets:
            break

    if len(picked) < 3:
        # fallback: first substantive paragraphs
        words = text.split()
        step = max(40, len(words) // 6)
        for i in range(0, min(len(words), step * 6), step):
            chunk = " ".join(words[i : i + 35])
            if len(chunk) > 30:
                picked.append(chunk + ("…" if i + 35 < len(words) else ""))
            if len(picked) >= max_bullets:
                break

    # ensure 3-8
    if not picked:
        return ["нет субтитров"]
    return picked[:8]


def main():
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)

    raw = json.loads(RAW.read_text(encoding="utf-8-sig"))
    entries = raw.get("entries") or []
    videos = []
    for i, e in enumerate(entries[:MAX_INDEX], start=1):
        videos.append(
            {
                "index": i,
                "video_id": e.get("id") or e.get("url", "").split("v=")[-1][:11],
                "title": e.get("title") or f"Video {i}",
                "url": f"https://www.youtube.com/watch?v={e.get('id')}",
                "duration": e.get("duration"),
            }
        )

    print(f"Playlist: {raw.get('title')} — processing {len(videos)} videos")
    results = []

    for batch_start in range(0, len(videos), BATCH):
        batch = videos[batch_start : batch_start + BATCH]
        for v in batch:
            idx = v["index"]
            vid = v["video_id"]
            title = v["title"]
            slug = slugify(title)
            fname = f"{idx:02d}-{vid}-{slug}.txt"
            fpath = TRANSCRIPTS / fname

            print(f"[{idx:02d}/{MAX_INDEX}] {vid} {title[:60]}...", flush=True)
            item = {
                **v,
                "filename": fname,
                "status": "pending",
                "language": None,
                "chars": 0,
                "reason": None,
            }
            try:
                # fresh API instance (not thread-safe)
                api = YouTubeTranscriptApi()
                lang, segs, lang_name = pick_and_fetch(api, vid)
                ts_text = segments_to_text(segs)
                plain = plain_text(segs)
                header = (
                    f"# {idx:02d}. {title}\n"
                    f"# video_id: {vid}\n"
                    f"# language: {lang} ({lang_name})\n"
                    f"# url: {v['url']}\n"
                    f"# segments: {len(segs)}\n\n"
                )
                fpath.write_text(header + ts_text + "\n", encoding="utf-8")
                item["status"] = "ok"
                item["language"] = lang
                item["language_name"] = lang_name
                item["chars"] = len(ts_text)
                item["plain_chars"] = len(plain)
                item["segment_count"] = len(segs)
                item["plain_text"] = plain  # temporary for ALL/CONTENT_MAP
                print(f"    OK lang={lang} chars={item['chars']}", flush=True)
            except TranscriptsDisabled as e:
                item["status"] = "FAILED"
                item["reason"] = "TranscriptsDisabled"
                print(f"    FAILED: TranscriptsDisabled", flush=True)
            except NoTranscriptFound as e:
                item["status"] = "FAILED"
                item["reason"] = f"NoTranscriptFound: {e}"
                print(f"    FAILED: NoTranscriptFound", flush=True)
            except VideoUnavailable as e:
                item["status"] = "FAILED"
                item["reason"] = "VideoUnavailable"
                print(f"    FAILED: VideoUnavailable", flush=True)
            except Exception as e:
                item["status"] = "FAILED"
                item["reason"] = f"{type(e).__name__}: {e}"
                print(f"    FAILED: {type(e).__name__}: {e}", flush=True)
                traceback.print_exc()

            results.append(item)
            time.sleep(DELAY)

        if batch_start + BATCH < len(videos):
            time.sleep(BATCH_PAUSE)

    # Save playlist.json (without full plain_text to keep lean)
    playlist_out = {
        "playlist_id": "PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj",
        "playlist_title": raw.get("title"),
        "playlist_url": "https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj",
        "fetched_count": len(results),
        "range": "1..31",
        "videos": [
            {
                k: v
                for k, v in r.items()
                if k not in ("plain_text",)
            }
            for r in results
        ],
    }
    (ROOT / "playlist.json").write_text(
        json.dumps(playlist_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ALL_TRANSCRIPTS.md
    all_parts = [
        f"# {raw.get('title') or 'CRM course'} — all transcripts\n",
        f"Playlist: https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj\n",
        f"Videos: 1..{MAX_INDEX}\n\n",
    ]
    for r in results:
        all_parts.append(f"## {r['index']:02d}. {r['title']}\n\n")
        all_parts.append(f"- video_id: `{r['video_id']}`\n")
        all_parts.append(f"- url: {r['url']}\n")
        all_parts.append(f"- status: **{r['status']}**\n")
        if r["status"] == "ok":
            all_parts.append(f"- language: {r.get('language')}\n")
            all_parts.append(f"- chars: {r.get('chars')}\n\n")
            plain = r.get("plain_text") or ""
            excerpt = plain if len(plain) <= 2000 else plain[:2000] + "…"
            all_parts.append(excerpt + "\n\n")
            all_parts.append(f"_Full timestamped: `transcripts/{r['filename']}`_\n\n")
        else:
            all_parts.append(f"- reason: {r.get('reason')}\n\n")
        all_parts.append("---\n\n")
    (ROOT / "ALL_TRANSCRIPTS.md").write_text("".join(all_parts), encoding="utf-8")

    # INDEX.md
    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] != "ok")
    total_chars = sum(r.get("chars") or 0 for r in results)
    idx_lines = [
        f"# CRM course transcripts — INDEX\n\n",
        f"Playlist: **{raw.get('title')}**  \n",
        f"URL: https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj  \n",
        f"Range: 1..{MAX_INDEX}  \n",
        f"OK: **{ok}** | FAILED: **{failed}** | Total chars: **{total_chars:,}**\n\n",
        "| # | title | video_id | status | chars |\n",
        "|---|-------|----------|--------|-------|\n",
    ]
    for r in results:
        title_esc = (r["title"] or "").replace("|", "\\|")
        st = r["status"] if r["status"] == "ok" else f"FAILED"
        idx_lines.append(
            f"| {r['index']} | {title_esc} | `{r['video_id']}` | {st} | {r.get('chars') or 0} |\n"
        )
    if failed:
        idx_lines.append("\n## Failures\n\n")
        for r in results:
            if r["status"] != "ok":
                idx_lines.append(
                    f"- #{r['index']} `{r['video_id']}`: {r.get('reason')}\n"
                )
    (ROOT / "INDEX.md").write_text("".join(idx_lines), encoding="utf-8")

    # CONTENT_MAP.md
    cm = [
        "# CONTENT_MAP — CRM с нуля\n\n",
        "Краткие takeaways по каждому видео (эвристика по тексту субтитров).\n\n",
    ]
    for r in results:
        cm.append(f"## {r['index']:02d}. {r['title']}\n\n")
        cm.append(f"- video_id: `{r['video_id']}`\n")
        cm.append(f"- status: {r['status']}\n")
        if r["status"] == "ok":
            bullets = extract_takeaways(r["title"], r.get("plain_text") or "")
            cm.append("\n")
            for b in bullets:
                cm.append(f"- {b}\n")
        else:
            cm.append("\n- нет субтитров\n")
        cm.append("\n")
    (ROOT / "CONTENT_MAP.md").write_text("".join(cm), encoding="utf-8")

    # Drop heavy plain_text from memory dump already saved
    print("\n=== DONE ===")
    print(f"OK={ok} FAILED={failed} total_chars={total_chars}")
    print(f"Output: {ROOT}")


if __name__ == "__main__":
    main()
