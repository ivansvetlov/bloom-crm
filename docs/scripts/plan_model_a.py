# -*- coding: utf-8 -*-
"""
Plan model A: phases = map, weeks = expansion.
- Canonical 8 phases on offer/landing (+ mirrors)
- index.html: phase map + each week tagged; reorder weeks to follow phases
"""
from pathlib import Path
import re

ROOT = Path(r"C:\Workspace\projects\flowwow-crm")
WT = Path(r"C:\Users\MiBookPro\.grok\worktrees\projects-flowwow-crm\flowwow-crm-dev")

# ── Canonical timeline block (offer/landing style) ─────────────────
TIMELINE_INNER = """      <div class="panel timeline">
        <div class="tl-row"><div class="tl-key">Фаза 0</div><div class="tl-val">Решения и визуальный язык<span class="tl-sub">Разведка, доступы, объём · палитра и тон UI · <b>нед. 1</b></span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 1</div><div class="tl-val">Основа системы<span class="tl-sub">Сервер, база, домен, бэкапы · <b>нед. 2</b></span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 2</div><div class="tl-val">Каркас кабинета<span class="tl-sub">Вход, роли, точки, журнал · <b>нед. 2</b></span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 3</div><div class="tl-val">Заказы<span class="tl-sub">Площадка + прямые, статусы, доставка · <b>нед. 3</b></span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 4</div><div class="tl-val">Чаты и уведомления<span class="tl-sub">WhatsApp, Telegram, MAX · алерты · <b>нед. 4–5</b></span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 5</div><div class="tl-val">Витрина, данные и цифры<span class="tl-sub">Каталог, перенос базы, отчёты · <b>нед. 6–8</b></span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 6</div><div class="tl-val">Тестирование и переход<span class="tl-sub">Сценарии с командой, параллельный режим, приёмка · <b>нед. 9</b></span></div></div>
        <div class="tl-row"><div class="tl-key">Фаза 7</div><div class="tl-val">Защита, запуск и поддержка<span class="tl-sub">Оплата, SLA, go-live, сопровождение · <b>нед. 10–12</b></span></div></div>
      </div>"""

TIMELINE_LEDE_OFFER = (
    "От согласования — к работающей системе. "
    "<strong>Фазы</strong> — карта работ; "
    "<strong>12 недель</strong> на "
    '<a href="index.html" style="color:inherit;font-weight:800;text-decoration:underline;text-underline-offset:3px">главной</a> '
    "— как фазы раскрываются по времени."
)

TIMELINE_LEDE_LANDING = (
    "От согласования — к работающей системе. "
    "<strong>Фазы</strong> — карта работ; "
    "<strong>12 недель</strong> "
    "раскрывают каждую фазу по шагам (см. подробный план на главной странице)."
)

# ── Week meta after reorder (old index → new) ─────────────────────
# Old weeks by extraction order (0-based):
# 0 connect/visual, 1 catalog, 2 chats, 3 roles, 4 payment, 5 delivery,
# 6 notif, 7 data, 8 test, 9 analytics, 10 security, 11 launch
#
# New order follows phases:
NEW_ORDER = [0, 3, 5, 2, 6, 1, 7, 9, 8, 4, 10, 11]
# 01 visual(0), 02 roles(3), 03 delivery~orders(5), 04 chats(2), 05 notif(6),
# 06 catalog(1), 07 data(7), 08 analytics(9), 09 test(8), 10 payment(4),
# 11 security(10), 12 launch(11)

WEEK_META = [
    # (no, title, sub, phase_label)
    ("01", "Решения и визуальный язык", "неделя 1 · фаза 0 · решения · визуал", "0"),
    ("02", "Основа и каркас: роли и точки", "неделя 2 · фазы 1–2 · основа · каркас", "1–2"),
    ("03", "Заказы и доставка", "неделя 3 · фаза 3 · заказы · логистика", "3"),
    ("04", "Все чаты в одном окне", "неделя 4 · фаза 4 · чаты", "4"),
    ("05", "Уведомления", "неделя 5 · фаза 4 · оповещения", "4"),
    ("06", "Витрина и товары", "неделя 6 · фаза 5 · каталог", "5"),
    ("07", "Данные и перенос", "неделя 7 · фаза 5 · перенос", "5"),
    ("08", "Аналитика", "неделя 8 · фаза 5 · отчёты", "5"),
    ("09", "Тестирование и параллельный запуск", "неделя 9 · фаза 6 · тестирование · переход", "6"),
    ("10", "Оплата и чеки", "неделя 10 · фаза 7 · финансы", "7"),
    ("11", "Безопасность", "неделя 11 · фаза 7 · защита", "7"),
    ("12", "Запуск и поддержка", "неделя 12 · фаза 7 · go-live", "7"),
]


def patch_timeline_file(path: Path, lede: str) -> None:
    if not path.exists():
        print("MISS", path)
        return
    text = path.read_text(encoding="utf-8")
    # lede
    text2, n1 = re.subn(
        r'(id="timeline">\s*<div class="sec-head">.*?</div>\s*<h2 class="sec-h">.*?</h2>\s*)'
        r'<p class="sec-lede">.*?</p>',
        r"\1" + f'<p class="sec-lede">{lede}</p>',
        text,
        count=1,
        flags=re.S,
    )
    # panel
    text3, n2 = re.subn(
        r'      <div class="panel timeline">.*?</div>\n    </section>',
        TIMELINE_INNER + "\n    </section>",
        text2,
        count=1,
        flags=re.S,
    )
    if n2 == 0:
        print("NO timeline panel", path)
        return
    path.write_text(text3, encoding="utf-8")
    print(f"OK timeline {path.name} lede={n1} panel={n2}")


def extract_weeks(html: str):
    """Return (prefix, weeks_list, suffix) for week-stack content."""
    m = re.search(r'(<div class="week-stack">\s*)', html)
    if not m:
        raise RuntimeError("week-stack not found")
    start = m.end()
    end_m = re.search(r"\n  </div>\n</section>", html[start:])
    if not end_m:
        raise RuntimeError("week-stack end not found")
    end = start + end_m.start()
    body = html[start:end]
    # split into week cards: each starts with optional comment then <div class="week
    parts = re.split(r"(?=\n    <!-- |\n    <div class=\"week)", body)
    weeks = []
    for p in parts:
        p = p.strip("\n")
        if not p.strip():
            continue
        if '<div class="week' in p or "class=\"week" in p:
            weeks.append(p if p.startswith("    ") else "    " + p.lstrip())
        elif p.strip().startswith("<!--"):
            # comment-only fragment — attach later; store as preamble of next
            weeks.append(p if p.startswith("    ") else "    " + p.lstrip())
    # merge comment-only with following week
    merged = []
    i = 0
    while i < len(weeks):
        w = weeks[i]
        if '<div class="week' not in w and i + 1 < len(weeks):
            merged.append(w.rstrip() + "\n" + weeks[i + 1])
            i += 2
        else:
            merged.append(w)
            i += 1
    if len(merged) != 12:
        # fallback: split only by week div
        merged = re.findall(
            r"(?:    <!--[\s\S]*?\n)?    <div class=\"week[\s\S]*?(?=\n    <!-- |\n    <div class=\"week|\Z)",
            body,
        )
        merged = [x.rstrip() for x in merged if x.strip()]
    if len(merged) != 12:
        raise RuntimeError(f"expected 12 weeks, got {len(merged)}")
    prefix = html[:start]
    suffix = html[end:]
    return prefix, merged, suffix


def retag_week(block: str, no: str, title: str, sub: str, open_first: bool) -> str:
    # open class only on first
    if open_first:
        block = re.sub(
            r'<div class="week(?: open)?">',
            '<div class="week open">',
            block,
            count=1,
        )
    else:
        block = re.sub(
            r'<div class="week(?: open)?">',
            '<div class="week">',
            block,
            count=1,
        )
    block = re.sub(
        r'<div class="week-no">\d+</div>',
        f'<div class="week-no">{no}</div>',
        block,
        count=1,
    )
    block = re.sub(
        r'<div class="week-title">.*?</div>',
        f'<div class="week-title">{title}</div>',
        block,
        count=1,
    )
    block = re.sub(
        r'<div class="week-sub">.*?</div>',
        f'<div class="week-sub">{sub}</div>',
        block,
        count=1,
    )
    # refresh leading comment
    block = re.sub(
        r"^    <!--.*?-->\n",
        f"    <!-- {no} · фаза · {title} -->\n",
        block,
        count=1,
        flags=re.S,
    )
    if not block.lstrip().startswith("<!--"):
        block = f"    <!-- {no} · фаза · {title} -->\n" + block.lstrip()
        if not block.startswith("    "):
            pass
    return block


INDEX_HEAD = """  <div class="sec-head reveal">
    <div style="display:flex;align-items:baseline;gap:14px"><span class="sec-num">01</span><span class="sec-tag">план запуска</span></div>
    <h2 class="sec-h">12 недель до полного запуска</h2>
    <p class="sec-lede" style="margin-top:12px;max-width:58ch;color:var(--ink-dim);font-size:1rem;line-height:1.5">
      <b>Фазы</b> — карта работ (как в коммерческом предложении).
      <b>Недели ниже</b> — как каждая фаза раскрывается по времени: не дублируют фазы, а детализируют их.
    </p>
    <div class="phase-map" aria-label="Карта фаз">
      <div class="pm-row"><span class="pm-k">Фаза 0</span><span class="pm-v">Решения и визуальный язык</span><span class="pm-w">нед. 1</span></div>
      <div class="pm-row"><span class="pm-k">Фаза 1–2</span><span class="pm-v">Основа и каркас кабинета</span><span class="pm-w">нед. 1–2</span></div>
      <div class="pm-row"><span class="pm-k">Фаза 3</span><span class="pm-v">Заказы (площадка + прямые + доставка)</span><span class="pm-w">нед. 3</span></div>
      <div class="pm-row"><span class="pm-k">Фаза 4</span><span class="pm-v">Чаты и уведомления</span><span class="pm-w">нед. 4–5</span></div>
      <div class="pm-row"><span class="pm-k">Фаза 5</span><span class="pm-v">Витрина, данные и цифры</span><span class="pm-w">нед. 6–8</span></div>
      <div class="pm-row"><span class="pm-k">Фаза 6</span><span class="pm-v">Тестирование и переход</span><span class="pm-w">нед. 9</span></div>
      <div class="pm-row"><span class="pm-k">Фаза 7</span><span class="pm-v">Защита, оплата, запуск</span><span class="pm-w">нед. 10–12</span></div>
    </div>
  </div>"""

PHASE_MAP_CSS = """
  .phase-map {
    margin-top: 22px;
    max-width: 720px;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: #fff;
    overflow: hidden;
  }
  .phase-map .pm-row {
    display: grid;
    grid-template-columns: 88px 1fr 72px;
    gap: 10px;
    align-items: baseline;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    font-size: 0.86rem;
  }
  .phase-map .pm-row:last-child { border-bottom: none; }
  .phase-map .pm-k {
    font-family: var(--mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: var(--terra);
  }
  .phase-map .pm-v { font-weight: 650; color: var(--ink-dim); }
  .phase-map .pm-w {
    font-family: var(--mono);
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--ink-mute);
    text-align: right;
  }
  @media (max-width: 640px) {
    .phase-map .pm-row { grid-template-columns: 72px 1fr; }
    .phase-map .pm-w { grid-column: 2; text-align: left; margin-top: -4px; }
  }
"""


def patch_index(path: Path) -> None:
    html = path.read_text(encoding="utf-8")

    # CSS for phase-map
    if ".phase-map" not in html:
        html = html.replace(
            "  .sec-lede { color: var(--ink-mute); max-width: 600px; }",
            "  .sec-lede { color: var(--ink-mute); max-width: 600px; }\n" + PHASE_MAP_CSS,
            1,
        )

    # section head
    html, n = re.subn(
        r'  <div class="sec-head reveal">\s*'
        r'<div style="display:flex;align-items:baseline;gap:14px"><span class="sec-num">01</span><span class="sec-tag">план запуска</span></div>\s*'
        r'<h2 class="sec-h">12 недель до полного запуска</h2>.*?'
        r"  </div>\s*\n\s*<div class=\"week-stack\">",
        INDEX_HEAD + "\n\n  <div class=\"week-stack\">",
        html,
        count=1,
        flags=re.S,
    )
    if n == 0:
        print("WARN index head not replaced", path)

    prefix, weeks, suffix = extract_weeks(html)
    reordered = []
    for i, old_i in enumerate(NEW_ORDER):
        no, title, sub, _ph = WEEK_META[i]
        block = weeks[old_i]
        block = retag_week(block, no, title, sub, open_first=(i == 0))
        reordered.append(block)

    new_body = "\n\n".join(reordered) + "\n"
    html = prefix + new_body + suffix
    path.write_text(html, encoding="utf-8")
    print(f"OK index weeks reordered {path}")


def main():
    # timelines
    pairs = [
        (ROOT / "docs" / "offer.html", TIMELINE_LEDE_OFFER),
        (ROOT / "docs" / "landing.html", TIMELINE_LEDE_LANDING),
        (ROOT / "docs" / "kp" / "demo" / "index.html", TIMELINE_LEDE_OFFER),
        (ROOT / "docs" / "kp" / "demo" / "landing.html", TIMELINE_LEDE_LANDING),
        (ROOT / "docs" / "kp" / "_template" / "index.html", TIMELINE_LEDE_OFFER),
        (ROOT / "docs" / "kp" / "_template" / "landing.html", TIMELINE_LEDE_LANDING),
        (WT / "docs" / "landing.html", TIMELINE_LEDE_LANDING),
        (WT / "docs" / "index.html", TIMELINE_LEDE_OFFER),  # may be offer-style
    ]
    for p, lede in pairs:
        if p.exists() and "panel timeline" in p.read_text(encoding="utf-8"):
            patch_timeline_file(p, lede)
        elif p.exists():
            print("skip timeline (no panel)", p)

    # main index with weeks
    idx = ROOT / "docs" / "index.html"
    if "week-stack" in idx.read_text(encoding="utf-8"):
        patch_index(idx)
    else:
        print("main index has no week-stack")


if __name__ == "__main__":
    main()
