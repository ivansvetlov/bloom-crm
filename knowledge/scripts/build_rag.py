# -*- coding: utf-8 -*-
"""
Build RAG index for Bloom CRM knowledge base.

Outputs:
  knowledge/chunks/chunks.jsonl
  knowledge/chunks/manifest.json
  knowledge/rag.sqlite  (FTS5 full-text)

Usage:
  python knowledge/scripts/build_rag.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # knowledge/
PROJECT = ROOT.parent
DOCS = PROJECT / "docs"
CHUNKS_DIR = ROOT / "chunks"
DB_PATH = ROOT / "rag.sqlite"

# Sources: (path, source_id, title, kind)
SOURCES: list[tuple[Path, str, str, str]] = [
    (DOCS / "tz.md", "tz", "ТЗ заказчика", "spec"),
    (DOCS / "questions.md", "questions", "Вопросы заказчику", "spec"),
    (DOCS / "research/crm-course/ARCHITECTURE_PLAN.md", "arch", "Architecture plan", "architecture"),
    (DOCS / "research/crm-course/CONTENT_MAP.md", "course-map", "Course content map", "research"),
    (DOCS / "research/courier-ux-everest-hybrid.md", "courier", "Courier UX research", "research"),
    (ROOT / "SCHEMA.md", "schema", "Wiki schema", "wiki"),
    (ROOT / "index.md", "wiki-index", "Wiki index", "wiki"),
]

# All wiki markdown under entities/concepts/comparisons
for sub in ("entities", "concepts", "comparisons"):
    d = ROOT / sub
    if d.is_dir():
        for p in sorted(d.glob("*.md")):
            SOURCES.append((p, f"wiki-{p.stem}", p.stem, "wiki"))


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    return text


def read_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".html":
        return strip_html(raw)
    # drop yaml frontmatter for chunking body (keep for meta separately)
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return raw


def chunk_text(text: str, source_id: str, title: str, kind: str, max_chars: int = 900, overlap: int = 120) -> list[dict]:
    # Prefer markdown headings / double newlines
    blocks = re.split(r"\n(?=#{1,3}\s)|\n{2,}", text)
    pieces: list[str] = []
    buf = ""
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if len(buf) + len(b) + 2 <= max_chars:
            buf = f"{buf}\n\n{b}".strip()
        else:
            if buf:
                pieces.append(buf)
            if len(b) <= max_chars:
                buf = b
            else:
                # hard split long block
                for i in range(0, len(b), max_chars - overlap):
                    pieces.append(b[i : i + max_chars])
                buf = ""
    if buf:
        pieces.append(buf)

    # merge tiny tails
    merged: list[str] = []
    for p in pieces:
        if merged and len(p) < 200 and len(merged[-1]) + len(p) < max_chars:
            merged[-1] = merged[-1] + "\n\n" + p
        else:
            merged.append(p)

    out = []
    for i, body in enumerate(merged):
        body = re.sub(r"[ \t]+", " ", body)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        if len(body) < 40:
            continue
        cid = f"{source_id}#{i:04d}"
        out.append(
            {
                "id": cid,
                "source_id": source_id,
                "title": title,
                "kind": kind,
                "chunk_index": i,
                "text": body,
                "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()[:16],
                "chars": len(body),
            }
        )
    return out


def build() -> None:
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    all_chunks: list[dict] = []
    source_meta = []

    for path, sid, title, kind in SOURCES:
        if not path.exists():
            print("SKIP missing", path)
            continue
        text = read_text(path)
        chunks = chunk_text(text, sid, title, kind)
        all_chunks.extend(chunks)
        source_meta.append(
            {
                "source_id": sid,
                "title": title,
                "kind": kind,
                "path": str(path.relative_to(PROJECT)).replace("\\", "/"),
                "chunks": len(chunks),
                "chars": len(text),
            }
        )
        print(f"  {sid}: {len(chunks)} chunks from {path.name}")

    # write jsonl
    jsonl_path = CHUNKS_DIR / "chunks.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    manifest = {
        "version": "1.0.0",
        "built": date.today().isoformat(),
        "project": "flowwow-crm",
        "product": "Bloom CRM",
        "chunk_count": len(all_chunks),
        "sources": source_meta,
        "files": {
            "chunks_jsonl": "knowledge/chunks/chunks.jsonl",
            "sqlite": "knowledge/rag.sqlite",
            "wiki_index": "knowledge/index.md",
        },
        "query": "python knowledge/scripts/query_rag.py \"ваш запрос\"",
    }
    (CHUNKS_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # SQLite FTS5
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE VIRTUAL TABLE chunks USING fts5(
            id UNINDEXED,
            source_id UNINDEXED,
            title,
            kind UNINDEXED,
            text,
            tokenize = 'unicode61'
        );
        """
    )
    cur.executemany(
        "INSERT INTO chunks (id, source_id, title, kind, text) VALUES (?, ?, ?, ?, ?)",
        [(c["id"], c["source_id"], c["title"], c["kind"], c["text"]) for c in all_chunks],
    )
    conn.commit()
    conn.close()

    print(f"\nOK: {len(all_chunks)} chunks -> {jsonl_path}")
    print(f"OK: FTS5 -> {DB_PATH}")
    print(f"OK: manifest -> {CHUNKS_DIR / 'manifest.json'}")


if __name__ == "__main__":
    build()
