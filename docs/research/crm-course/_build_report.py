# -*- coding: utf-8 -*-
"""Build beautiful HTML report: architecture + course map + montage plan."""
import json
import re
from pathlib import Path

ROOT = Path(r"C:\Workspace\projects\flowwow-crm\docs\research\crm-course")
rows = json.loads((ROOT / "playlist.json").read_text(encoding="utf-8"))
total_sec = sum((r.get("duration_sec") or 0) for r in rows)
hours = total_sec // 3600
mins = (total_sec % 3600) // 60

def esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

# transcripts present?
have = set()
for f in (ROOT / "transcripts").glob("*.txt"):
    m = re.match(r"\d{2}-([A-Za-z0-9_-]{11})", f.name)
    if m:
        have.add(m.group(1))

ep_rows = []
for r in rows:
    d = r.get("duration_sec") or 0
    dm = f"{d // 60}:{d % 60:02d}" if d else "—"
    ok = r["video_id"] in have
    pill = '<span class="pill ok">transcript</span>' if ok else '<span class="pill warn">pending</span>'
    ep_rows.append(
        f"""<tr>
      <td class="num">{r['index']:02d}</td>
      <td class="ttl"><a href="{esc(r['url'])}" target="_blank" rel="noopener">{esc(r['title'])}</a></td>
      <td class="mono">{esc(r['video_id'])}</td>
      <td class="dur">{dm}</td>
      <td>{pill}</td>
    </tr>"""
    )

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bloom CRM Full — Architecture & Course Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #FBF7F4; --bg-2: #fff; --bg-3: #F3EEEA;
    --border: #EDE4DD; --border-2: #E0D5CC;
    --ink: #1C1917; --ink-dim: #44403C; --ink-mute: #78716C; --ink-faint: #A8A29E;
    --terra: #E06B4A; --terra-2: #C85A3C; --terra-soft: #FCEBE5;
    --sage: #6F8F72; --sage-soft: #EAF2EB;
    --amber: #D9A441; --amber-soft: #F8F0DC;
    --plum: #7A5A74; --plum-soft: #F3EBF1;
    --radius: 16px; --ease: cubic-bezier(0.16,1,0.3,1);
    --shadow: 0 10px 30px rgba(28,25,23,.06);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: Inter, system-ui, sans-serif;
    background:
      radial-gradient(900px 480px at 8% -8%, rgba(224,107,74,.12), transparent 55%),
      radial-gradient(700px 420px at 100% 0%, rgba(111,143,114,.08), transparent 50%),
      var(--bg);
    color: var(--ink); line-height: 1.55; font-size: 15px;
  }}
  a {{ color: var(--terra); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 22px 80px; }}
  .top {{
    display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between;
    margin-bottom: 28px;
  }}
  .brand {{ font-weight: 800; letter-spacing: -.02em; display: flex; align-items: center; gap: 10px; }}
  .brand .pro {{
    font-size: .68rem; font-weight: 700; color: #fff; background: var(--terra);
    padding: 4px 10px; border-radius: 999px;
  }}
  .nav-chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
  .nav-chips a {{
    font-size: .78rem; font-weight: 600; color: var(--ink-dim);
    background: var(--bg-2); border: 1px solid var(--border);
    padding: 8px 12px; border-radius: 999px; box-shadow: 0 2px 8px rgba(28,25,23,.04);
    text-decoration: none;
  }}
  .nav-chips a:hover {{ border-color: var(--terra); color: var(--terra); }}
  .hero {{
    background: rgba(255,255,255,.72); border: 1px solid rgba(255,255,255,.85);
    backdrop-filter: blur(14px); border-radius: 22px; padding: 32px 28px;
    box-shadow: var(--shadow); margin-bottom: 22px;
  }}
  .hero .kicker {{
    display: inline-flex; gap: 8px; align-items: center;
    font-size: .78rem; font-weight: 700; color: var(--terra);
    background: var(--terra-soft); padding: 6px 12px; border-radius: 999px; margin-bottom: 14px;
  }}
  .hero h1 {{
    font-size: clamp(1.7rem, 3.4vw, 2.4rem); font-weight: 900;
    letter-spacing: -.035em; line-height: 1.1; margin-bottom: 12px;
  }}
  .hero h1 em {{ font-style: normal; color: var(--terra); }}
  .hero .lede {{ color: var(--ink-mute); max-width: 58ch; font-size: 1.02rem; }}
  .stats {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 22px;
  }}
  .stat {{
    background: var(--bg-2); border: 1px solid var(--border); border-radius: 14px;
    padding: 14px 16px; box-shadow: 0 2px 10px rgba(28,25,23,.04);
  }}
  .stat .l {{ font-size: .78rem; font-weight: 600; color: var(--ink-mute); margin-bottom: 6px; }}
  .stat .v {{ font-size: 1.35rem; font-weight: 800; letter-spacing: -.03em; }}
  .stat .s {{ font-size: .76rem; color: var(--sage); font-weight: 600; margin-top: 4px; }}
  section.card {{
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 24px 24px 20px; margin-bottom: 16px; box-shadow: var(--shadow);
  }}
  section.card h2 {{
    font-size: 1.2rem; font-weight: 800; letter-spacing: -.02em; margin-bottom: 6px;
    display: flex; align-items: baseline; gap: 10px;
  }}
  section.card h2 .n {{
    font-size: .72rem; font-weight: 700; color: var(--terra);
    background: var(--terra-soft); padding: 3px 9px; border-radius: 999px;
  }}
  section.card .sub {{ color: var(--ink-mute); font-size: .92rem; margin-bottom: 16px; }}
  h3 {{ font-size: .95rem; font-weight: 750; margin: 16px 0 8px; letter-spacing: -.01em; }}
  p, li {{ color: var(--ink-dim); }}
  ul {{ padding-left: 1.15rem; margin: 6px 0 10px; }}
  li {{ margin: 4px 0; }}
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  .tile {{
    background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 14px;
  }}
  .tile b {{ display: block; margin-bottom: 4px; color: var(--ink); }}
  .tile .m {{ font-size: .84rem; color: var(--ink-mute); }}
  .pill {{
    display: inline-flex; align-items: center; font-size: .68rem; font-weight: 700;
    padding: 3px 8px; border-radius: 999px;
  }}
  .pill.must {{ background: var(--terra-soft); color: var(--terra); }}
  .pill.should {{ background: var(--sage-soft); color: var(--sage); }}
  .pill.could {{ background: var(--plum-soft); color: var(--plum); }}
  .pill.warn {{ background: var(--amber-soft); color: #A07A20; }}
  .pill.ok {{ background: var(--sage-soft); color: var(--sage); }}
  table {{ width: 100%; border-collapse: collapse; font-size: .86rem; }}
  th, td {{ text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  th {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: var(--ink-faint); font-weight: 700; }}
  td.num {{ font-family: 'JetBrains Mono', monospace; font-size: .78rem; color: var(--terra); font-weight: 700; width: 40px; }}
  td.mono {{ font-family: 'JetBrains Mono', monospace; font-size: .72rem; color: var(--ink-faint); }}
  td.dur {{ font-variant-numeric: tabular-nums; color: var(--ink-mute); white-space: nowrap; }}
  td.ttl a {{ color: var(--ink); font-weight: 600; text-decoration: none; }}
  td.ttl a:hover {{ color: var(--terra); }}
  .flow {{
    display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 10px 0;
  }}
  .flow span {{
    background: var(--bg); border: 1px solid var(--border); border-radius: 999px;
    padding: 6px 12px; font-size: .8rem; font-weight: 600;
  }}
  .flow .arr {{ color: var(--ink-faint); border: none; background: none; padding: 0; }}
  .callout {{
    background: var(--terra-soft); border: 1px solid rgba(224,107,74,.25);
    border-radius: 12px; padding: 14px 16px; margin: 12px 0; font-size: .92rem;
  }}
  .callout.warn {{ background: var(--amber-soft); border-color: rgba(217,164,65,.35); }}
  .callout.ok {{ background: var(--sage-soft); border-color: rgba(111,143,114,.3); }}
  .steps {{ counter-reset: s; display: grid; gap: 10px; }}
  .step {{
    display: grid; grid-template-columns: 36px 1fr; gap: 12px; align-items: start;
    padding: 12px; border-radius: 12px; background: var(--bg); border: 1px solid var(--border);
  }}
  .step::before {{
    counter-increment: s; content: counter(s);
    width: 36px; height: 36px; border-radius: 10px;
    background: var(--terra); color: #fff; font-weight: 800;
    display: flex; align-items: center; justify-content: center; font-size: .9rem;
  }}
  .step b {{ display: block; color: var(--ink); margin-bottom: 2px; }}
  .step span {{ font-size: .86rem; color: var(--ink-mute); }}
  footer {{
    margin-top: 28px; padding-top: 16px; border-top: 1px solid var(--border);
    font-size: .84rem; color: var(--ink-mute);
    display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between;
  }}
  @media (max-width: 860px) {{
    .stats, .grid-2, .grid-3 {{ grid-template-columns: 1fr 1fr; }}
  }}
  @media (max-width: 560px) {{
    .stats, .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="brand">Bloom CRM <span class="pro">FULL PLAN</span></div>
    <div class="nav-chips">
      <a href="#vision">Видение</a>
      <a href="#modules">Модули</a>
      <a href="#lifecycle">Жизненный цикл</a>
      <a href="#arch">Архитектура</a>
      <a href="#course">Курс</a>
      <a href="#apply">Применить</a>
      <a href="#montage">Монтаж</a>
    </div>
  </div>

  <header class="hero">
    <div class="kicker">✦ Product · Architecture · Lectoria course</div>
    <h1>Максимально полная версия <em>Bloom CRM</em></h1>
    <p class="lede">
      Операционный кабинет флористики: Flowwow + прямые продажи + WhatsApp/Telegram/MAX + витрина и доставка.
      Отчёт объединяет архитектурный план и разбор курса «CRM с нуля» (эпизоды 1–31) — что взять в монтаж HTML.
    </p>
    <div class="stats">
      <div class="stat"><div class="l">Модулей must</div><div class="v">9</div><div class="s">закрыть смену</div></div>
      <div class="stat"><div class="l">Экранов full UI</div><div class="v">12+</div><div class="s">sitemap кабинета</div></div>
      <div class="stat"><div class="l">Курс 1–31</div><div class="v">{len(rows)}</div><div class="s">~{hours}ч {mins}м видео</div></div>
      <div class="stat"><div class="l">Транскрипты</div><div class="v">24/31</div><div class="s">~529k chars · ru auto</div></div>
    </div>
  </header>

  <section class="card" id="vision">
    <h2><span class="n">01</span> Product vision</h2>
    <p class="sub">Bloom = source of truth · Flowwow = marketplace-канал</p>
    <div class="callout ok">
      <b>Одна фраза:</b> менеджер, флорист и курьер закрывают день в одном окне —
      Flowwow + мессенджеры + свои заказы, витрина и цифры — без Excel и «где этот букет?».
    </div>
    <div class="grid-2" style="margin-top:12px">
      <div class="tile"><b>Владелец</b><div class="m">Выручка FW vs прямые, точки, пики 8 Марта, health интеграций</div></div>
      <div class="tile"><b>Менеджер</b><div class="m">Accept за секунды, inbox, прямой заказ, SLA 3 мин</div></div>
      <div class="tile"><b>Флорист</b><div class="m">Очередь сборки, фото «как на витрине», открытка/слот</div></div>
      <div class="tile"><b>Курьер</b><div class="m">Взял → фото → еду → вручил, ETA к слоту</div></div>
    </div>
    <h3>Принципы</h3>
    <ul>
      <li><b>Визуал = продукт</b> — фото до/после, photo-gate перед доставкой</li>
      <li><b>Слот и адрес раньше «красивостей»</b></li>
      <li><b>Два контура</b> — flowwow (sync out) и direct/* (только Bloom)</li>
      <li><b>Единый inbox</b> — клиент пишет «как всегда»</li>
      <li><b>Пиковый режим</b> — 8 Марта / НГ, только P0-кнопки</li>
      <li><b>Надёжность как фича</b> — health + reconcile</li>
    </ul>
  </section>

  <section class="card" id="modules">
    <h2><span class="n">02</span> Карта модулей</h2>
    <p class="sub">Must закрывает смену · Should — сеть · Could/Later — расширения</p>
    <table>
      <thead><tr><th>Модуль</th><th>Зачем</th><th>Prio</th></tr></thead>
      <tbody>
        <tr><td>Auth & Org</td><td>Вход, сеть, магазины</td><td><span class="pill must">must</span></td></tr>
        <tr><td>Orders hub + card</td><td>Канбан, FW+direct, фото, timeline</td><td><span class="pill must">must</span></td></tr>
        <tr><td>Flowwow sync</td><td>Ingest, dual status, photo, reconcile</td><td><span class="pill must">must</span></td></tr>
        <tr><td>Direct sales</td><td>Ручные заказы без push в FW</td><td><span class="pill must">must</span></td></tr>
        <tr><td>Unified Inbox</td><td>WA + TG + MAX</td><td><span class="pill must">must</span></td></tr>
        <tr><td>Notifications + Health</td><td>SLA 3 мин, отвал ключей</td><td><span class="pill must">must</span></td></tr>
        <tr><td>Customers</td><td>Карточка, LTV, merge</td><td><span class="pill must">must</span></td></tr>
        <tr><td>Vitrina / Catalog</td><td>Цены, остатки, hide multi-shop</td><td><span class="pill should">should</span></td></tr>
        <tr><td>Delivery / Couriers</td><td>Назначение, ETA, photo-before-leave</td><td><span class="pill should">should</span></td></tr>
        <tr><td>Analytics + Finance</td><td>Цифры, оплаты, export</td><td><span class="pill should">should</span></td></tr>
        <tr><td>Loyalty / Bank / OFD</td><td>Отдельные ТЗ</td><td><span class="pill could">could</span></td></tr>
      </tbody>
    </table>
  </section>

  <section class="card" id="lifecycle">
    <h2><span class="n">03</span> Жизненный цикл заказа</h2>
    <p class="sub">Расширение 5 шагов демо до full ops set</p>
    <div class="flow">
      <span>Новый</span><span class="arr">→</span>
      <span>Принят</span><span class="arr">→</span>
      <span>В сборке</span><span class="arr">→</span>
      <span>Собран</span><span class="arr">→</span>
      <span>Фото</span><span class="arr">→</span>
      <span>Курьер / Самовывоз</span><span class="arr">→</span>
      <span>В доставке</span><span class="arr">→</span>
      <span>Вручён</span><span class="arr">→</span>
      <span>Выполнен</span>
    </div>
    <div class="callout">
      <b>Gates:</b> assembled → доставка требует before-photo · прямой заказ никогда не уходит во Flowwow ·
      sort: SLA overdue → ASAP/slot 2ч → today.
    </div>
  </section>

  <section class="card" id="arch">
    <h2><span class="n">04</span> Архитектурный blueprint</h2>
    <p class="sub">Default stack — не догма, разумный старт</p>
    <div class="grid-3">
      <div class="tile"><b>Frontend</b><div class="m">Responsive SPA shell · WS/SSE · mobile-first ops</div></div>
      <div class="tile"><b>API</b><div class="m">Modular monolith · outbox · workers Redis</div></div>
      <div class="tile"><b>Data</b><div class="m">PostgreSQL · S3 РФ · audit log</div></div>
      <div class="tile"><b>Integrations</b><div class="m">Flowwow · WA/TG/MAX · notify TG/VK</div></div>
      <div class="tile"><b>Auth</b><div class="m">Login/password · RBAC · shop scope option</div></div>
      <div class="tile"><b>Hosting</b><div class="m">Yandex/Timeweb РФ · 152-ФЗ · backups</div></div>
    </div>
    <h3>Sitemap full cabinet</h3>
    <ul>
      <li>Сегодня · Заказы (+ drawer) · Чаты · Клиенты · Витрина · Склад</li>
      <li>Доставка · Финансы · Цифры · Команда · Настройки · Лояльность</li>
      <li>Satellite: Courier PWA (Сейчас / Смена / Маршрут / Профиль)</li>
    </ul>
    <p style="margin-top:10px;font-size:.88rem;color:var(--ink-mute)">
      Полный текст: <a href="ARCHITECTURE_PLAN.md">ARCHITECTURE_PLAN.md</a>
    </p>
  </section>

  <section class="card" id="course">
    <h2><span class="n">05</span> Курс Lectoria «CRM с нуля»</h2>
    <p class="sub">
      Плейлист
      <a href="https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj" target="_blank" rel="noopener">PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj</a>
      · эпизоды 1–31 · ~{hours}ч {mins}м
    </p>
    <div class="callout ok">
      <b>Транскрипты:</b> <b>24/31</b> сохранены (~529k символов, ru auto-subs).
      Эпизоды 25–31 (DialogChoose → Vue) — rate-limit YouTube; докачаем отдельно.
      Полные тексты: <code>transcripts/</code> · сводка: <a href="ALL_TRANSCRIPTS.md">ALL_TRANSCRIPTS.md</a>.
    </div>
    <h3>Фазы курса → Bloom</h3>
    <div class="grid-2">
      <div class="tile"><b>A. ТЗ 001–006</b><div class="m">Scope freeze, обсуждение стейкхолдера → tz.md + questions</div></div>
      <div class="tile"><b>B. IA 007–013</b><div class="m">Диаграмма интерфейсов, Figma, Dashboard, таблицы</div></div>
      <div class="tile"><b>C. DS 011–022</b><div class="m">Button, fields, filters, dialogs, notifications</div></div>
      <div class="tile"><b>D. Layout 015–028</b><div class="m">BEM, auth, dashboard, profile → static CRM complete</div></div>
      <div class="tile"><b>E. Vue 029–031</b><div class="m">Stateful inputs, drop-upload, Composition API — later SPA</div></div>
      <div class="tile"><b>Не в курсе</b><div class="m">Flowwow dual, inbox×3, photo-gate, peak, 152-ФЗ — наш домен</div></div>
    </div>
    <h3 style="margin-top:18px">Эпизоды 1–31</h3>
    <div style="overflow-x:auto;margin-top:8px">
      <table>
        <thead><tr><th>#</th><th>Название</th><th>ID</th><th>Длит.</th><th>Текст</th></tr></thead>
        <tbody>
{"".join(ep_rows)}
        </tbody>
      </table>
    </div>
  </section>

  <section class="card" id="apply">
    <h2><span class="n">06</span> Что применить к Bloom</h2>
    <p class="sub">Сшивка курса + ТЗ + architecture plan</p>
    <table>
      <thead><tr><th>#</th><th>Практика</th><th>Действие</th></tr></thead>
      <tbody>
        <tr><td>1</td><td>ТЗ → freeze → design</td><td>Не монтировать full без P0-ответов (API, messengers, courier)</td></tr>
        <tr><td>2</td><td>Диаграмма интерфейсов</td><td>Full nav в shell (12 разделов)</td></tr>
        <tr><td>3</td><td>DS first</td><td>Tokens + button/field/dialog/toast/table sheet</td></tr>
        <tr><td>4</td><td>Dashboard = день</td><td>«Сегодня» = KPI + feed + hot + chips</td></tr>
        <tr><td>5</td><td>Tables + filters</td><td>Orders/Clients dense UI</td></tr>
        <tr><td>6</td><td>DialogChoose</td><td>Reject reason, shop pick, courier assign</td></tr>
        <tr><td>7</td><td>Layout complete first</td><td>Static HTML full CRM до Vue/React</td></tr>
        <tr><td>8</td><td>Drop-upload</td><td>Photo before delivery на order card</td></tr>
        <tr><td>9</td><td>Auth simple</td><td>Login/password, без SMS (как в ТЗ)</td></tr>
        <tr><td>10</td><td>Domain overlay</td><td>Наложить florist entities поверх generic CRM-паттернов курса</td></tr>
      </tbody>
    </table>
  </section>

  <section class="card" id="montage">
    <h2><span class="n">07</span> Последовательность монтажа HTML</h2>
    <p class="sub">После этого отчёта — можно начинать full-crm shell</p>
    <div class="steps">
      <div class="step"><div><b>App shell full nav</b><span>Сегодня · Заказы · Чаты · Клиенты · Витрина · Доставка · Цифры · Команда · Настройки</span></div></div>
      <div class="step"><div><b>Order detail drawer</b><span>payer≠recipient, открытка, слот, фото, timeline, reject</span></div></div>
      <div class="step"><div><b>Status gates</b><span>кнопки по этапу + «нужно фото» перед доставкой</span></div></div>
      <div class="step"><div><b>Inbox → Create order</b><span>prefill direct + badge на канбане</span></div></div>
      <div class="step"><div><b>Today ops</b><span>KPI + feed + SLA 3 мин + connection chips</span></div></div>
      <div class="step"><div><b>Filters / Vitrina / Client / Delivery / Analytics</b><span>волна 2 экранов</span></div></div>
      <div class="step"><div><b>Settings health + Roles + Peak</b><span>интеграции, доступы, 8 Марта</span></div></div>
      <div class="step"><div><b>Courier mini-PWA</b><span>4 вкладки, verb-кнопки</span></div></div>
    </div>
    <div class="callout ok" style="margin-top:16px">
      <b>DoD wave-1:</b> весь sitemap кликабелен · happy path FW new→done · chat→direct order ·
      3 точки · reject · health warn · mobile nav.
    </div>
  </section>

  <section class="card">
    <h2><span class="n">08</span> Артефакты на диске</h2>
    <ul>
      <li><a href="ARCHITECTURE_PLAN.md">ARCHITECTURE_PLAN.md</a> — полный product & architecture</li>
      <li><a href="CONTENT_MAP.md">CONTENT_MAP.md</a> — takeaways курса → Bloom</li>
      <li><a href="INDEX.md">INDEX.md</a> — таблица 31 видео</li>
      <li><a href="playlist.json">playlist.json</a> — machine-readable metadata</li>
      <li><a href="../../tz.md">../../tz.md</a> · <a href="../../demo.html">demo.html</a> · <a href="../../questions.html">questions.html</a></li>
    </ul>
  </section>

  <footer>
    <span>Bloom CRM · full plan report · 2026-08-01</span>
    <span>Курс: Lectoria · транскрипты 24/31 · эпизоды 25–31 pending</span>
  </footer>
</div>
</body>
</html>
"""

out = ROOT / "report.html"
out.write_text(html, encoding="utf-8")
# also copy to docs root for easy open
docs = Path(r"C:\Workspace\projects\flowwow-crm\docs\crm-full-report.html")
docs.write_text(html, encoding="utf-8")
print("wrote", out)
print("wrote", docs)
