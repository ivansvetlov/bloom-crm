# -*- coding: utf-8 -*-
"""Build cost-oriented TZ decomposition into PDF (coarse packages)."""
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
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

s_title = ParagraphStyle("T", fontName="AB", fontSize=16, leading=20, textColor=ink, spaceAfter=4)
s_sub = ParagraphStyle("S", fontName="A", fontSize=9.5, leading=13, textColor=mute, spaceAfter=8)
s_h2 = ParagraphStyle(
    "H2", fontName="AB", fontSize=11.5, leading=15, textColor=terra, spaceBefore=11, spaceAfter=5
)
s_body = ParagraphStyle("B", fontName="A", fontSize=9.5, leading=13, textColor=ink, spaceAfter=4)
s_meta = ParagraphStyle("M", fontName="A", fontSize=8.5, leading=11, textColor=mute, spaceAfter=3)
s_cell = ParagraphStyle("C", fontName="A", fontSize=8.5, leading=11, textColor=ink)
s_cell_b = ParagraphStyle("CB", fontName="AB", fontSize=8.5, leading=11, textColor=ink)
s_footer = ParagraphStyle(
    "F", fontName="A", fontSize=8, leading=10, textColor=mute, alignment=TA_CENTER
)


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(t: str) -> str:
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    t = t.replace("`", "")
    return t


def p_cell(t: str, bold: bool = False) -> Paragraph:
    return Paragraph(inline(t), s_cell_b if bold else s_cell)


def make_table(rows: list[list[str]]) -> Table:
    data = [[p_cell(c, bold=(i == 0)) for c in row] for i, row in enumerate(rows)]
    n = len(rows[0])
    usable = 172 * mm
    if n == 2:
        widths = [42 * mm, 130 * mm]
    elif n == 3:
        widths = [32 * mm, 78 * mm, 62 * mm]
    else:
        widths = [usable / n] * n
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), card),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.35, line),
            ]
        )
    )
    return t


def build_story(md: str) -> list:
    story = []
    lines = md.splitlines()
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines):
        i += 1

    table_rows: list[str] = []

    def flush_table() -> None:
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
        if parsed:
            story.append(Spacer(1, 3))
            story.append(make_table(parsed))
            story.append(Spacer(1, 5))

    while i < len(lines):
        raw = lines[i].rstrip()
        i += 1
        if not raw.strip():
            flush_table()
            continue
        if raw.strip() == "---":
            flush_table()
            story.append(
                HRFlowable(width="100%", thickness=0.4, color=line, spaceBefore=3, spaceAfter=6)
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
        if raw.startswith("- ") or raw.startswith("→ "):
            story.append(Paragraph(inline(raw), s_meta if raw.startswith("→") else s_body))
            continue
        if re.match(r"^\d+\.", raw):
            story.append(Paragraph(inline(raw), s_body))
            continue
        if raw.startswith("*") and raw.endswith("*") and not raw.startswith("**"):
            story.append(Paragraph(f"<i>{inline(raw.strip('* ').strip())}</i>", s_meta))
            continue
        story.append(Paragraph(inline(raw), s_body))

    flush_table()
    return story


def main() -> None:
    md = MD_PATH.read_text(encoding="utf-8")
    story = [
        Paragraph("Bloom CRM", s_title),
        Paragraph(
            "Декомпозиция ТЗ для оценки стоимости · крупные пакеты работ",
            s_sub,
        ),
        HRFlowable(width="100%", thickness=1, color=terra, spaceAfter=8),
    ]
    story.extend(build_story(md))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.4, color=line, spaceAfter=4))
    story.append(
        Paragraph(
            "Bloom CRM · оценка · без детализации до кнопок · имена площадок не фиксируются",
            s_footer,
        )
    )

    SimpleDocTemplate(
        str(OUT_PATH),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="Декомпозиция ТЗ для оценки — Bloom CRM",
        author="Bloom CRM",
    ).build(story)
    print(OUT_PATH, OUT_PATH.stat().st_size)


if __name__ == "__main__":
    main()
