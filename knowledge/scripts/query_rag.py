# -*- coding: utf-8 -*-
"""
Query Bloom CRM RAG (SQLite FTS5).

Usage:
  python knowledge/scripts/query_rag.py "Flowwow multi-account"
  python knowledge/scripts/query_rag.py "SLA поддержка" --limit 8
  python knowledge/scripts/query_rag.py "остатки склад" --json
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "rag.sqlite"


def to_fts_query(q: str) -> str:
    # Simple: AND of tokens; keep cyrillic/latin words
    tokens = re.findall(r"[\wа-яА-ЯёЁ]{2,}", q, flags=re.U)
    if not tokens:
        return q
    # FTS5 prefix for partial matches
    return " ".join(f'"{t}"' if len(t) <= 3 else f"{t}*" for t in tokens[:12])


def search(q: str, limit: int = 6) -> list[dict]:
    if not DB_PATH.exists():
        raise SystemExit(f"Missing {DB_PATH}. Run: python knowledge/scripts/build_rag.py")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    fts_q = to_fts_query(q)
    try:
        rows = conn.execute(
            """
            SELECT id, source_id, title, kind, text,
                   bm25(chunks) AS score
            FROM chunks
            WHERE chunks MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (fts_q, limit),
        ).fetchall()
    except sqlite3.OperationalError:
        # fallback: OR loose
        loose = " OR ".join(re.findall(r"[\wа-яА-ЯёЁ]{3,}", q, flags=re.U)[:8])
        rows = conn.execute(
            """
            SELECT id, source_id, title, kind, text,
                   bm25(chunks) AS score
            FROM chunks
            WHERE chunks MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (loose or q, limit),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def main() -> None:
    ap = argparse.ArgumentParser(description="Query Bloom CRM RAG")
    ap.add_argument("query", help="search query (RU/EN)")
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    hits = search(args.query, args.limit)
    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return

    if not hits:
        print("No hits.")
        sys.exit(1)

    print(f"# RAG hits for: {args.query}\n")
    for i, h in enumerate(hits, 1):
        preview = h["text"].replace("\n", " ")
        if len(preview) > 420:
            preview = preview[:420] + "…"
        print(f"## {i}. [{h['kind']}] {h['title']} · `{h['id']}`")
        print(f"score={h['score']:.3f} source={h['source_id']}")
        print(preview)
        print()


if __name__ == "__main__":
    main()
