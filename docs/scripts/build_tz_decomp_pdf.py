# -*- coding: utf-8 -*-
"""Build TZ decomposition markdown into PDF."""
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "tz-decomposition.md"
OUT_PATH = ROOT / "Bloom-CRM-TZ-decomposition.pdf"

pdfmetrics.registerFont(TTFont("A", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("AB", r"C:\Windows\Fonts\arialbd.ttf"))

terra = HexColor("#c45c3e")
ink = HexColor("#1a1f1c")
mute = HexColor("#5a6560")
line = HexColor("#d8e0db")
card = HexColor("#f6f8f6")
mvp_bg = HexColor("#e8f5ec")
later_bg = HexColor("#f5f0e6")

s_title = ParagraphStyle("T", fontName="AB", fontSize=16, leading=20, textColor=ink, spaceAfter=4)
s_sub = ParagraphStyle("S", fontName="A", fontSize=9, leading=12, textColor=mute, spaceAfter=8)
s_h2 = ParagraphStyle(
    "H2", fontName="AB", fontSize=11, leading=14, textColor=terra, spaceBefore=10, spaceAfter=4
)
s_body = ParagraphStyle("B", fontName="A", fontSize=9, leading=12, textColor=ink, spaceAfter=3)
s_meta = ParagraphStyle("M", fontName="A", fontSize=8, leading=11, textColor=mute)
s_cell = ParagraphStyle("C", fontName="A", fontSize=8, leading=10, textColor=ink)
s_cell_b = ParagraphStyle("CB", fontName="AB", fontSize=8, leading=10, textColor=ink)
s_footer = ParagraphStyle(
    "F", fontName="A", fontSize=8, leading=10, textColor=mute, alignment=TA_CENTER
)


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(t: str) -> str:
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = t.replace("`", "")
    return t


def p_cell(t: str, bold: bool = False) -> Paragraph:
    return Paragraph(inline(t), s_cell_b if bold else s_cell)


def make_table(rows: list[list[str]], col_widths: list[float]) -> Table:
    data = []
    for i, row in enumerate(rows):
        data.append([p_cell(c, bold=(i == 0)) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), card),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("GRID", (0, 0), (-1, -1), 0.35, line),
    ]
    # highlight MVP column if present
    if rows and len(rows[0]) >= 3 and "MVP" in rows[0][-1]:
        for r in range(1, len(rows)):
            val = rows[r][-1].lower()
            if val.startswith("да"):
                style.append(("BACKGROUND", (-1, r), (-1, r), mvp_bg))
            elif "позже" in val or "v1.1" in val or val.startswith("нет"):
                style.append(("BACKGROUND", (-1, r), (-1, r), later_bg))
    t.setStyle(TableStyle(style))
    return t


def parse_md_tables(md: str) -> list:
    """Yield flowables from markdown-ish structure."""
    story = []
    lines = md.splitlines()
    i = 0
    # skip first H1
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines):
        i += 1

    table_rows: list[str] = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        parsed = []
        for row in table_rows:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                continue
            parsed.append(cells)
        table_rows = []
        if not parsed:
            return
        n = len(parsed[0])
        usable = 170 * mm
        if n == 2:
            widths = [38 * mm, 132 * mm]
        elif n == 3:
            widths = [18 * mm, 122 * mm, 30 * mm]
        elif n == 4:
            widths = [28 * mm, 72 * mm, 40 * mm, 30 * mm]
        else:
            widths = [usable / n] * n
        story.append(Spacer(1, 2))
        story.append(make_table(parsed, widths))
        story.append(Spacer(1, 4))

    while i < len(lines):
        raw = lines[i].rstrip()
        i += 1
        if not raw.strip():
            flush_table()
            continue
        if raw.strip() == "---":
            flush_table()
            story.append(
                HRFlowable(width="100%", thickness=0.4, color=line, spaceBefore=4, spaceAfter=6)
            )
            continue
        if raw.startswith("|"):
            table_rows.append(raw)
            continue
        flush_table()
        if raw.startswith("## "):
            story.append(Paragraph(inline(raw[3:]), s_h2))
            continue
        if raw.startswith("### "):
            story.append(Paragraph(f"<b>{inline(raw[4:])}</b>", s_body))
            continue
        if raw.startswith("- "):
            story.append(Paragraph("• " + inline(raw[2:]), s_body))
            continue
        if raw.startswith("*") and raw.endswith("*") and not raw.startswith("**"):
            story.append(Paragraph(f"<i>{inline(raw.strip('* ').strip())}</i>", s_meta))
            continue
        story.append(Paragraph(inline(raw), s_body))

    flush_table()
    return story


def main() -> None:
    md = MD_PATH.read_text(encoding="utf-8")
    story = []
    story.append(Paragraph("Bloom CRM", s_title))
    story.append(
        Paragraph(
            "Декомпозиция ТЗ на подзадачи · crmbloom.ru · 2026-08-01",
            s_sub,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=terra, spaceAfter=8))
    story.extend(parse_md_tables(md))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.4, color=line, spaceAfter=4))
    story.append(
        Paragraph(
            "Bloom CRM · декомпозиция для планирования · без привязки к имени заказчика",
            s_footer,
        )
    )

    doc = SimpleDocTemplate(
        str(OUT_PATH),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Декомпозиция ТЗ — Bloom CRM",
        author="Bloom CRM",
    )
    doc.build(story)
    print(OUT_PATH, OUT_PATH.stat().st_size)


if __name__ == "__main__":
    main()
