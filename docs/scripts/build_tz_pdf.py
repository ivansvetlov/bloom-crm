# -*- coding: utf-8 -*-
"""Build polished TZ markdown into PDF (Cyrillic via Arial)."""
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
MD_PATH = ROOT / "tz.md"
OUT_PATH = ROOT / "Bloom-CRM-TZ.pdf"

pdfmetrics.registerFont(TTFont("A", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("AB", r"C:\Windows\Fonts\arialbd.ttf"))

terra = HexColor("#c45c3e")
ink = HexColor("#1a1f1c")
mute = HexColor("#5a6560")
line = HexColor("#d8e0db")
card = HexColor("#f6f8f6")

s_title = ParagraphStyle("T", fontName="AB", fontSize=18, leading=22, textColor=ink, spaceAfter=6)
s_sub = ParagraphStyle("S", fontName="A", fontSize=10, leading=14, textColor=mute, spaceAfter=10)
s_h2 = ParagraphStyle(
    "H2", fontName="AB", fontSize=12, leading=16, textColor=terra, spaceBefore=12, spaceAfter=4
)
s_body = ParagraphStyle("B", fontName="A", fontSize=10, leading=14, textColor=ink, spaceAfter=3)
s_bullet = ParagraphStyle(
    "Bu", fontName="A", fontSize=10, leading=14, textColor=ink, leftIndent=12, spaceAfter=2
)
s_meta = ParagraphStyle("M", fontName="A", fontSize=9, leading=12, textColor=mute)
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


def main() -> None:
    md = MD_PATH.read_text(encoding="utf-8")
    lines = md.splitlines()
    story = []
    story.append(Paragraph("Техническое задание", s_sub))
    story.append(Paragraph("Bloom CRM", s_title))
    story.append(
        Paragraph(
            "crmbloom.ru · исходные формулировки · 2026-08-01",
            s_sub,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=terra, spaceAfter=10))

    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines) and lines[i].startswith("# "):
        i += 1

    in_table = False
    table_rows: list[str] = []

    def flush_table() -> None:
        nonlocal table_rows, in_table
        if not table_rows:
            in_table = False
            return
        data = []
        for row in table_rows:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            # skip markdown separator
            if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                continue
            data.append([Paragraph(inline(c), s_meta) for c in cells])
        if data:
            n = len(data[0])
            if n == 2:
                widths = [40 * mm, 130 * mm]
            else:
                widths = [170 * mm / n] * n
            t = Table(data, colWidths=widths)
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), card),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        ("GRID", (0, 0), (-1, -1), 0.4, line),
                    ]
                )
            )
            story.append(Spacer(1, 4))
            story.append(t)
            story.append(Spacer(1, 6))
        table_rows = []
        in_table = False

    while i < len(lines):
        raw = lines[i].rstrip()
        i += 1
        if not raw.strip():
            if in_table:
                flush_table()
            continue
        if raw.strip() == "---":
            if in_table:
                flush_table()
            story.append(
                HRFlowable(width="100%", thickness=0.5, color=line, spaceBefore=4, spaceAfter=6)
            )
            continue
        if raw.startswith("|"):
            in_table = True
            table_rows.append(raw)
            continue
        if in_table:
            flush_table()
        if raw.startswith("## "):
            story.append(Paragraph(inline(raw[3:]), s_h2))
            continue
        if raw.startswith("### "):
            story.append(Paragraph(f"<b>{inline(raw[4:])}</b>", s_body))
            continue
        if raw.startswith("- "):
            story.append(Paragraph("• " + inline(raw[2:]), s_bullet))
            continue
        if raw.startswith("*") and raw.endswith("*") and not raw.startswith("**"):
            story.append(Paragraph(f"<i>{inline(raw.strip('* ').strip())}</i>", s_meta))
            continue
        story.append(Paragraph(inline(raw), s_body))

    if in_table:
        flush_table()

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=line, spaceAfter=6))
    story.append(
        Paragraph("Bloom CRM · crmbloom.ru · для согласования с заказчиком", s_footer)
    )

    doc = SimpleDocTemplate(
        str(OUT_PATH),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="ТЗ — Bloom CRM",
        author="Bloom CRM",
    )
    doc.build(story)
    print(OUT_PATH, OUT_PATH.stat().st_size)


if __name__ == "__main__":
    main()
