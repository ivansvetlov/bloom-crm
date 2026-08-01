# -*- coding: utf-8 -*-
"""Hang Chatwoot + Twenty + Dolibarr + mega modules onto docs/kp/demo/demo.html (canonical base)."""
from __future__ import annotations

from pathlib import Path

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]

text = BASE.read_text(encoding="utf-8")

# ── title / badge ──
text = text.replace(
    "<title>Bloom CRM — демо кабинета</title>",
    "<title>Bloom CRM — прототип кабинета</title>",
)
text = text.replace(
    'Bloom CRM <span class="pro">ДЕМО</span>',
    'Bloom CRM <span class="pro">ПРОТОТИП</span>',
)

# ── extra CSS before </style> ──
EXTRA_CSS = r"""
  /* ═══ Prototype layers: Chatwoot · Twenty · Dolibarr · Mega ═══ */
  .content.chat-mode { max-width: none; padding: 12px 16px 16px; }
  .content.chat-mode .demo-note,
  .content.chat-mode .footer { display: none; }

  .tg-app { grid-template-columns: 280px 1fr 260px; }
  .tg-contact {
    border-left: 1px solid var(--border); background: #fff;
    display: flex; flex-direction: column; min-width: 0; overflow: hidden;
  }
  .tg-contact .cc-head {
    padding: 14px 14px 10px; border-bottom: 1px solid var(--border);
    font-weight: 800; font-size: 0.88rem;
  }
  .tg-contact .cc-body { padding: 12px 14px; overflow-y: auto; flex: 1; font-size: 0.84rem; color: var(--ink-dim); }
  .tg-contact .cc-row { margin-bottom: 10px; }
  .tg-contact .cc-row b { display: block; font-size: 0.72rem; color: var(--ink-faint); margin-bottom: 2px; }
  .tg-contact .cc-actions { padding: 12px; border-top: 1px solid var(--border); display: flex; flex-direction: column; gap: 8px; }
  .tg-contact .btn { width: 100%; justify-content: center; }

  .bubble.note {
    align-self: center; max-width: 88%;
    background: var(--amber-soft); color: #6b5410; border: 1px dashed #d9a441;
    border-radius: 12px; font-size: 0.84rem;
  }
  .chat-input .note-on { background: var(--amber-soft) !important; color: #6b5410; }

  .kc-badges { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px; }
  .kc-tag.pay-paid { background: var(--sage-soft); color: var(--sage); }
  .kc-tag.pay-pending { background: var(--amber-soft); color: #A07A20; }
  .kc-tag.pay-cod { background: var(--plum-soft); color: var(--plum); }
  .kcard { cursor: pointer; }
  .kcard .grab { cursor: grab; }

  .drawer-scrim {
    position: fixed; inset: 0; z-index: 80; background: rgba(28,25,23,0.35);
    opacity: 0; pointer-events: none; transition: opacity 0.25s;
  }
  .drawer-scrim.show { opacity: 1; pointer-events: auto; }
  .order-drawer {
    position: fixed; top: 0; right: 0; bottom: 0; z-index: 85;
    width: min(420px, 100vw); background: var(--bg-2);
    border-left: 1px solid var(--border);
    box-shadow: -12px 0 40px rgba(28,25,23,0.12);
    transform: translateX(100%); transition: transform 0.3s var(--ease);
    display: flex; flex-direction: column;
  }
  .order-drawer.show { transform: none; }
  .od-head {
    padding: 16px 18px; border-bottom: 1px solid var(--border);
    display: flex; align-items: flex-start; justify-content: space-between; gap: 12px;
  }
  .od-head h3 { font-size: 1.05rem; font-weight: 800; letter-spacing: -0.02em; }
  .od-head .sub { font-size: 0.78rem; color: var(--ink-mute); margin-top: 4px; }
  .od-body { flex: 1; overflow-y: auto; padding: 16px 18px; }
  .od-foot {
    padding: 14px 18px; border-top: 1px solid var(--border);
    display: flex; gap: 8px; flex-wrap: wrap;
  }
  .doc-chain {
    display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 0 16px;
  }
  .doc-chain span {
    font-size: 0.68rem; font-weight: 700; padding: 6px 10px; border-radius: 999px;
    background: var(--bg-3); color: var(--ink-mute); border: 1px solid var(--border);
  }
  .doc-chain span.on { background: var(--terra-soft); color: var(--terra); border-color: transparent; }
  .doc-chain span.done { background: var(--sage-soft); color: var(--sage); border-color: transparent; }
  .stream { display: flex; flex-direction: column; gap: 8px; margin-top: 12px; }
  .stream .ev {
    font-size: 0.8rem; color: var(--ink-dim); padding: 8px 10px;
    background: var(--bg); border-radius: 10px; border: 1px solid var(--border);
  }
  .stream .ev time { display: block; font-size: 0.68rem; color: var(--ink-faint); margin-top: 2px; }

  .cmdk {
    position: fixed; inset: 0; z-index: 120; display: none;
    align-items: flex-start; justify-content: center; padding-top: 12vh;
    background: rgba(28,25,23,0.4);
  }
  .cmdk.show { display: flex; }
  .cmdk-box {
    width: min(520px, calc(100vw - 32px)); background: var(--bg-2);
    border-radius: 16px; border: 1px solid var(--border);
    box-shadow: 0 24px 60px rgba(28,25,23,0.2); overflow: hidden;
  }
  .cmdk-box input {
    width: 100%; border: 0; outline: 0; padding: 16px 18px;
    font-size: 1rem; font-family: var(--font); border-bottom: 1px solid var(--border);
    background: transparent; color: var(--ink);
  }
  .cmdk-list { max-height: 320px; overflow-y: auto; padding: 8px; }
  .cmdk-item {
    display: flex; align-items: center; gap: 10px; width: 100%;
    text-align: left; border: 0; background: transparent; cursor: pointer;
    padding: 10px 12px; border-radius: 10px; font-family: var(--font); color: var(--ink);
  }
  .cmdk-item:hover, .cmdk-item.on { background: var(--terra-soft); }
  .cmdk-item .k { margin-left: auto; font-size: 0.72rem; color: var(--ink-faint); font-weight: 700; }

  .vit-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
  .vit-card {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 14px; box-shadow: var(--shadow-sm);
  }
  .vit-card.hidden-sku { opacity: 0.55; }
  .vit-card .nm { font-weight: 800; font-size: 0.92rem; margin-bottom: 4px; }
  .vit-card .pr { color: var(--terra); font-weight: 800; font-size: 1.05rem; }
  .vit-card .st { font-size: 0.78rem; color: var(--ink-mute); margin: 8px 0; }
  .vit-card .st.low { color: var(--terra); font-weight: 700; }
  .vit-actions { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
  .vit-actions button {
    border: 1px solid var(--border-2); background: var(--bg); border-radius: 8px;
    padding: 6px 10px; cursor: pointer; font-family: var(--font); font-size: 0.78rem; font-weight: 700;
  }
  .vit-actions button:hover { border-color: var(--terra); color: var(--terra); }

  .set-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .set-card {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 16px; box-shadow: var(--shadow-sm);
  }
  .set-card h3 { font-size: 0.92rem; font-weight: 800; margin-bottom: 10px; }
  .set-card ul { list-style: none; display: flex; flex-direction: column; gap: 8px; }
  .set-card li {
    display: flex; justify-content: space-between; gap: 8px;
    font-size: 0.86rem; padding: 8px 10px; background: var(--bg); border-radius: 10px;
  }
  .set-card li span { color: var(--ink-mute); font-size: 0.78rem; font-weight: 600; }

  .proto-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
  .proto-chips .chip { box-shadow: none; }

  @media (max-width: 1100px) {
    .tg-app { grid-template-columns: 240px 1fr; }
    .tg-contact { display: none; }
  }
  @media (max-width: 860px) {
    .set-grid { grid-template-columns: 1fr; }
  }
"""

if "/* ═══ Prototype layers:" not in text:
    text = text.replace("</style>", EXTRA_CSS + "\n</style>")

# ── nav ──
old_nav = """  <div class="sb-label">Меню</div>
  <nav class="sb-nav">
    <button class="sb-link active" data-view="overview"><span class="idx">01</span>Сегодня</button>
    <button class="sb-link" data-view="orders"><span class="idx">02</span>Заказы <span class="badge" id="navNew">0</span></button>
    <button class="sb-link" data-view="chats"><span class="idx">03</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="analytics"><span class="idx">04</span>Отчёты</button>
  </nav>"""

new_nav = """  <div class="sb-label">Меню</div>
  <nav class="sb-nav">
    <button class="sb-link active" data-view="overview"><span class="idx">01</span>Сегодня</button>
    <button class="sb-link" data-view="orders"><span class="idx">02</span>Заказы <span class="badge" id="navNew">0</span></button>
    <button class="sb-link" data-view="chats"><span class="idx">03</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">04</span>Витрина</button>
    <button class="sb-link" data-view="analytics"><span class="idx">05</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">06</span>Настройки</button>
  </nav>"""

if old_nav not in text:
    raise SystemExit("nav block not found")
text = text.replace(old_nav, new_nav)

# topbar crumb + cmdk chip
text = text.replace(
    """  <header class="topbar">
    <div class="crumb"><b>Кабинет</b><span class="sep">·</span><span>Демо</span></div>
    <div class="tb-chips">
      <span class="chip sage"><span class="dot online"></span>Маркетплейс · подключено</span>
      <span class="chip hide-m">₽ · Россия</span>
      <button class="chip terra" data-action="newOrder">+ Новый заказ</button>
    </div>
  </header>""",
    """  <header class="topbar">
    <div class="crumb"><b>Кабинет</b><span class="sep">·</span><span id="crumbView">Сегодня</span></div>
    <div class="tb-chips">
      <span class="chip hide-m" title="Twenty">⌘K поиск</span>
      <span class="chip sage"><span class="dot online"></span>Маркетплейс · подключено</span>
      <span class="chip hide-m">₽ · Россия</span>
      <button class="chip terra" data-action="newOrder">+ Новый заказ</button>
    </div>
  </header>""",
)

# demo note
text = text.replace(
    """    <div class="demo-note">
      <span>Это <b>демо-кабинет</b>. Полный прототип (чаты Chatwoot · UX Twenty · dual status Dolibarr · mega-модули): <a href="cabinet.html" style="color:var(--terra);font-weight:700">cabinet.html</a></span>
      <span class="dn-right">
        <button class="btn" data-action="reset">Начать сначала</button>
        <a class="btn terra" href="cabinet.html">Прототип кабинета</a>
        <a class="btn" href="index.html">К предложению</a>
      </span>
    </div>""",
    """    <div class="demo-note">
      <span>Прототип на базе демо · слои: <b>Chatwoot</b> (чаты) · <b>Twenty</b> (⌘K) · <b>Dolibarr</b> (dual status / витрина) · <b>mega</b> (модули)</span>
      <span class="dn-right">
        <button class="btn" data-action="reset">Начать сначала</button>
        <a class="btn" href="index.html">К предложению</a>
      </span>
    </div>
    <div class="proto-chips">
      <span class="chip">Chatwoot · inbox + note + заказ из чата</span>
      <span class="chip">Twenty · ⌘K</span>
      <span class="chip">Dolibarr · оплата ∥ статус · витрина</span>
      <span class="chip sage">Mega · витрина / настройки / drawer</span>
    </div>""",
)

# chats: add contact panel + note + create order buttons
old_chat_main = """        <div class="tg-main">
          <div class="chat-head">
            <div class="who" id="chHead"></div>
            <div style="display:flex;align-items:center;gap:8px">
              <span class="meta" id="chMeta">в сети</span>
              <div class="actions">
                <button type="button" class="ico-btn" title="Поиск" aria-label="Поиск">⌕</button>
                <button type="button" class="ico-btn" title="Ещё" aria-label="Ещё">⋯</button>
              </div>
            </div>
          </div>
          <div class="chat-body" id="chBody"></div>
          <div class="chat-input">
            <button type="button" class="ico-btn" title="Вложение" aria-label="Вложение">📎</button>
            <input id="chInput" type="text" placeholder="Сообщение" autocomplete="off">
            <button type="button" class="send" id="chSend" title="Отправить" aria-label="Отправить">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/></svg>
            </button>
          </div>
        </div>
      </div>
    </section>"""

new_chat_main = """        <div class="tg-main">
          <div class="chat-head">
            <div class="who" id="chHead"></div>
            <div style="display:flex;align-items:center;gap:8px">
              <span class="meta" id="chMeta">в сети</span>
              <div class="actions">
                <button type="button" class="ico-btn" id="btnNoteMode" title="Приватная заметка (Chatwoot)">📝</button>
                <button type="button" class="ico-btn" id="btnAssignMe" title="Назначить мне">👤</button>
              </div>
            </div>
          </div>
          <div class="chat-body" id="chBody"></div>
          <div class="chat-input">
            <button type="button" class="ico-btn" title="Вложение" aria-label="Вложение">📎</button>
            <input id="chInput" type="text" placeholder="Сообщение" autocomplete="off">
            <button type="button" class="send" id="chSend" title="Отправить" aria-label="Отправить">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/></svg>
            </button>
          </div>
        </div>
        <aside class="tg-contact" id="tgContact">
          <div class="cc-head">Контакт</div>
          <div class="cc-body" id="tgContactBody"></div>
          <div class="cc-actions">
            <button type="button" class="btn terra" id="btnOrderFromChat">+ Заказ из чата</button>
            <button type="button" class="btn" id="btnResolveChat">Решить диалог</button>
          </div>
        </aside>
      </div>
    </section>"""

if old_chat_main not in text:
    raise SystemExit("chat main block not found")
text = text.replace(old_chat_main, new_chat_main)

# inject vitrina + settings before footer
FOOTER_MARK = '    <div class="footer">'
VITRINA_SETTINGS = """    <!-- ═════════════ 05 · VITRINA (Dolibarr stock) ═════════════ -->
    <section data-section="vitrina" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Dolibarr · остатки / цены / hide</span>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap">
        <button type="button" class="btn" id="vitFilterAll">Все</button>
        <button type="button" class="btn" id="vitFilterLow">Мало на складе</button>
        <button type="button" class="btn" id="vitFilterHidden">Скрытые</button>
      </div>
      <div class="vit-grid" id="vitGrid"></div>
    </section>

    <!-- ═════════════ 06 · SETTINGS (mega) ═════════════ -->
    <section data-section="settings" style="display:none">
      <div class="set-grid">
        <div class="set-card">
          <h3>Точки сети</h3>
          <ul id="setShops"></ul>
        </div>
        <div class="set-card">
          <h3>Пользователи · роли</h3>
          <ul id="setUsers"></ul>
        </div>
        <div class="set-card">
          <h3>Каналы</h3>
          <ul>
            <li>Маркетплейс <span>подключён</span></li>
            <li>WhatsApp <span>активен</span></li>
            <li>Telegram <span>активен</span></li>
            <li>MAX <span>активен</span></li>
          </ul>
        </div>
        <div class="set-card">
          <h3>Источники паттернов</h3>
          <ul>
            <li>Chatwoot <span>inbox</span></li>
            <li>Twenty <span>⌘K / UX</span></li>
            <li>Dolibarr <span>dual status · витрина</span></li>
            <li>Mega CRM <span>модули</span></li>
          </ul>
        </div>
      </div>
    </section>

"""

if 'data-section="vitrina"' not in text:
    text = text.replace(FOOTER_MARK, VITRINA_SETTINGS + FOOTER_MARK)

# drawers + cmdk before toast
if 'id="orderDrawer"' not in text:
    text = text.replace(
        '<div class="toast" id="toast"></div>',
        """<div class="drawer-scrim" id="drawerScrim"></div>
<div class="order-drawer" id="orderDrawer">
  <div class="od-head">
    <div>
      <h3 id="odTitle">Заказ</h3>
      <div class="sub" id="odSub"></div>
    </div>
    <button type="button" class="btn ghost" id="odClose">✕</button>
  </div>
  <div class="od-body" id="odBody"></div>
  <div class="od-foot" id="odFoot"></div>
</div>

<div class="cmdk" id="cmdk">
  <div class="cmdk-box">
    <input id="cmdkInput" type="search" placeholder="Перейти · заказ · чат · SKU…" autocomplete="off" />
    <div class="cmdk-list" id="cmdkList"></div>
  </div>
</div>

<div class="toast" id="toast"></div>""",
    )

# ── JS: seed pay + history, products ──
text = text.replace(
    """  var seed = [
    { id: 'FW-1042', name: 'Букет пионов, 15 шт.', price: 3200, channel: 'fw', status: 'new', shop: 'Мира 14' },
    { id: 'FW-1041', name: 'Сборный букет, роза + эустома', price: 2450, channel: 'fw', status: 'new', shop: 'Ленина 92' },
    { id: 'WA-881', name: 'Торт «Красный бархат»', price: 1890, channel: 'wa', status: 'new', shop: 'Рижская 8' },
    { id: 'FW-1040', name: 'Композиция «Нежность»', price: 4100, channel: 'fw', status: 'accepted', shop: 'Мира 14' },
    { id: 'TG-556', name: 'Букет тюльпанов, 21 шт.', price: 1990, channel: 'tg', status: 'accepted', shop: 'Ленина 92' },
    { id: 'FW-1039', name: 'Орхидея в кашпо', price: 5300, channel: 'fw', status: 'assembled', shop: 'Мира 14' },
    { id: 'MAX-31', name: 'Корзина «Счастье»', price: 7600, channel: 'max', status: 'assembled', shop: 'Рижская 8' },
    { id: 'FW-1038', name: 'Букет гербер, 25 шт.', price: 2800, channel: 'fw', status: 'delivering', shop: 'Ленина 92' },
    { id: 'WA-880', name: 'Медвежонок 40 см', price: 1500, channel: 'wa', status: 'done', shop: 'Мира 14' },
    { id: 'FW-1037', name: 'Пионовидная роза, 7 шт.', price: 2700, channel: 'fw', status: 'done', shop: 'Рижская 8' }
  ];""",
    """  var PAY_NAMES = { paid: 'Оплачен', pending: 'Ожидает', cod: 'При получении' };
  var seed = [
    { id: 'FW-1042', name: 'Букет пионов, 15 шт.', price: 3200, channel: 'fw', status: 'new', shop: 'Мира 14', pay: 'paid', history: [] },
    { id: 'FW-1041', name: 'Сборный букет, роза + эустома', price: 2450, channel: 'fw', status: 'new', shop: 'Ленина 92', pay: 'paid', history: [] },
    { id: 'WA-881', name: 'Торт «Красный бархат»', price: 1890, channel: 'wa', status: 'new', shop: 'Рижская 8', pay: 'pending', history: [] },
    { id: 'FW-1040', name: 'Композиция «Нежность»', price: 4100, channel: 'fw', status: 'accepted', shop: 'Мира 14', pay: 'paid', history: [] },
    { id: 'TG-556', name: 'Букет тюльпанов, 21 шт.', price: 1990, channel: 'tg', status: 'accepted', shop: 'Ленина 92', pay: 'cod', history: [] },
    { id: 'FW-1039', name: 'Орхидея в кашпо', price: 5300, channel: 'fw', status: 'assembled', shop: 'Мира 14', pay: 'paid', history: [] },
    { id: 'MAX-31', name: 'Корзина «Счастье»', price: 7600, channel: 'max', status: 'assembled', shop: 'Рижская 8', pay: 'pending', history: [] },
    { id: 'FW-1038', name: 'Букет гербер, 25 шт.', price: 2800, channel: 'fw', status: 'delivering', shop: 'Ленина 92', pay: 'paid', history: [] },
    { id: 'WA-880', name: 'Медвежонок 40 см', price: 1500, channel: 'wa', status: 'done', shop: 'Мира 14', pay: 'paid', history: [] },
    { id: 'FW-1037', name: 'Пионовидная роза, 7 шт.', price: 2700, channel: 'fw', status: 'done', shop: 'Рижская 8', pay: 'paid', history: [] }
  ];

  var products = [
    { id: 'sku-1', name: 'Букет пионов, 15 шт.', price: 3200, stock: 12, hidden: false },
    { id: 'sku-2', name: 'Сборный · роза + эустома', price: 2450, stock: 4, hidden: false },
    { id: 'sku-3', name: 'Композиция «Нежность»', price: 4100, stock: 2, hidden: false },
    { id: 'sku-4', name: 'Корзина «Счастье»', price: 7600, stock: 1, hidden: false },
    { id: 'sku-5', name: 'Тюльпаны, 21 шт.', price: 1990, stock: 28, hidden: false },
    { id: 'sku-6', name: 'Орхидея в кашпо', price: 5300, stock: 0, hidden: true }
  ];
  var vitFilter = 'all';""",
)

text = text.replace(
    """  var state = {
    orders: JSON.parse(JSON.stringify(seed)),
    nextOrder: 1043,
    chatIdx: 0,
    typing: false,
    view: 'overview',
    simTimer: null,
    animIds: {},
    simPaused: false
  };""",
    """  var state = {
    orders: JSON.parse(JSON.stringify(seed)),
    nextOrder: 1043,
    chatIdx: 0,
    typing: false,
    view: 'overview',
    simTimer: null,
    animIds: {},
    simPaused: false,
    noteMode: false,
    openOrderId: null,
    assignee: 'Анна К.'
  };""",
)

# cardHtml dual badges + click
old_card = """  function cardHtml(o) {
    var shopBadge = SHOP_N[o.shop] ? ' · точка ' + SHOP_N[o.shop] : '';
    var anim = state.animIds[o.id] || '';
    var cls = 'kcard' + (anim ? ' ' + anim : '');
    return '<div class="' + cls + '" draggable="true" data-id="' + o.id + '">' +
      '<div class="kc-top"><span class="kc-id">' + o.id + '</span><span class="kc-price">' + fmtPrice(o.price) + '</span></div>' +
      '<div class="kc-name">' + esc(o.name) + '</div>' +
      '<div class="kc-meta">' + esc(o.shop) + shopBadge + '</div>' +
      '<span class="kc-tag ' + o.channel + '">' + CH_NAMES[o.channel] + '</span>' +
      '</div>';
  }"""

new_card = """  function cardHtml(o) {
    var shopBadge = SHOP_N[o.shop] ? ' · точка ' + SHOP_N[o.shop] : '';
    var anim = state.animIds[o.id] || '';
    var cls = 'kcard' + (anim ? ' ' + anim : '');
    var pay = o.pay || (o.channel === 'fw' ? 'paid' : 'pending');
    return '<div class="' + cls + '" draggable="true" data-id="' + o.id + '">' +
      '<div class="kc-top"><span class="kc-id">' + o.id + '</span><span class="kc-price">' + fmtPrice(o.price) + '</span></div>' +
      '<div class="kc-name">' + esc(o.name) + '</div>' +
      '<div class="kc-meta">' + esc(o.shop) + shopBadge + '</div>' +
      '<div class="kc-badges">' +
        '<span class="kc-tag ' + o.channel + '">' + CH_NAMES[o.channel] + '</span>' +
        '<span class="kc-tag pay-' + pay + '">' + (PAY_NAMES[pay] || pay) + '</span>' +
      '</div></div>';
  }"""

if old_card not in text:
    raise SystemExit("cardHtml not found")
text = text.replace(old_card, new_card)

# simNewOrder with pay
text = text.replace(
    "    state.orders.unshift({ id: id, name: name, price: price, channel: channel, status: 'new', shop: shop });",
    "    var pay = channel === 'fw' ? 'paid' : (Math.random() > 0.5 ? 'pending' : 'cod');\n"
    "    state.orders.unshift({ id: id, name: name, price: price, channel: channel, status: 'new', shop: shop, pay: pay, history: [{ t: Date.now(), text: 'Создан (симуляция)' }] });",
)

# moveOrder history
text = text.replace(
    """    var from = order.status;
    order.status = status;
    flashCard(id, status === 'done' ? 'is-done-flash' : 'is-moved', 650);""",
    """    var from = order.status;
    order.status = status;
    order.history = order.history || [];
    order.history.push({ t: Date.now(), text: NAMES[from] + ' → ' + NAMES[status] });
    flashCard(id, status === 'done' ? 'is-done-flash' : 'is-moved', 650);
    if (state.openOrderId === id) openOrderDrawer(id);""",
)

# saveOrder pay
text = text.replace(
    "    state.orders.unshift({ id: id, name: item, price: price, channel: channel, status: 'new', shop: shop });",
    "    state.orders.unshift({ id: id, name: item, price: price, channel: channel, status: 'new', shop: shop, pay: channel === 'fw' ? 'paid' : 'pending', history: [{ t: Date.now(), text: 'Создан вручную' }] });",
)

# switchView VIEW_NAMES + crumb + render modules
text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', chats: 'Чаты', analytics: 'Отчёты' };",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', chats: 'Чаты', vitrina: 'Витрина', analytics: 'Отчёты', settings: 'Настройки' };",
)

text = text.replace(
    """    if (view === 'analytics') renderReports();
    if (view === 'orders') {
      liveSay('Имитация запущена');
      // burst when opening board
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 400);
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 1100);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }""",
    """    if (view === 'analytics') renderReports();
    if (view === 'vitrina') renderVitrina();
    if (view === 'settings') renderSettings();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    var crumb = $('#crumbView');
    if (crumb) crumb.textContent = VIEW_NAMES[view] || view;
    if (view === 'orders') {
      liveSay('Имитация запущена');
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 400);
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 1100);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }""",
)

# enhance renderChat for notes + contact
old_render_chat = """  function renderChat() {
    var c = chats[state.chatIdx];
    var av = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : 'max';
    $('#chHead').innerHTML =
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<div><div class="nm">' + esc(c.name) + '</div><div class="ch">' + CH_NAMES[c.channel] + ' · ' + esc(c.shop) + '</div></div>';
    $('#chMeta').textContent = 'в сети';
    var body = $('#chBody');
    body.innerHTML = c.msgs.map(function (m) {
      var now = new Date();
      var time = now.getHours() + ':' + String(now.getMinutes()).padStart(2, '0');
      return '<div class="bubble' + (m.me ? ' me' : '') + '">' + esc(m.text) + '<span class="time">' + time + '</span></div>';
    }).join('');
    body.scrollTop = body.scrollHeight;
  }"""

new_render_chat = """  function renderChat() {
    var c = chats[state.chatIdx];
    if (!c) return;
    var av = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : 'max';
    $('#chHead').innerHTML =
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<div><div class="nm">' + esc(c.name) + '</div><div class="ch">' + CH_NAMES[c.channel] + ' · ' + esc(c.shop) + (c.assignee ? ' · ' + esc(c.assignee) : '') + '</div></div>';
    $('#chMeta').textContent = c.resolved ? 'решён' : 'в сети';
    var body = $('#chBody');
    body.innerHTML = c.msgs.map(function (m) {
      var now = new Date();
      var time = now.getHours() + ':' + String(now.getMinutes()).padStart(2, '0');
      if (m.note) return '<div class="bubble note">📝 ' + esc(m.text) + '<span class="time">' + time + '</span></div>';
      return '<div class="bubble' + (m.me ? ' me' : '') + '">' + esc(m.text) + '<span class="time">' + time + '</span></div>';
    }).join('');
    body.scrollTop = body.scrollHeight;
    renderContact();
  }

  function renderContact() {
    var el = $('#tgContactBody');
    if (!el) return;
    var c = chats[state.chatIdx];
    if (!c) { el.innerHTML = ''; return; }
    var linked = state.orders.filter(function (o) {
      return (c.orderIds || []).indexOf(o.id) >= 0 || (o.channel !== 'fw' && o.shop === c.shop);
    }).slice(0, 3);
    el.innerHTML =
      '<div class="cc-row"><b>Имя</b>' + esc(c.name) + '</div>' +
      '<div class="cc-row"><b>Канал</b>' + CH_NAMES[c.channel] + '</div>' +
      '<div class="cc-row"><b>Точка</b>' + esc(c.shop) + '</div>' +
      '<div class="cc-row"><b>Ответственный</b>' + esc(c.assignee || '—') + '</div>' +
      '<div class="cc-row"><b>Заказы</b>' + (linked.length ? linked.map(function (o) {
        return '<div style="margin-top:4px"><a href="#" data-open-order="' + o.id + '" style="color:var(--terra);font-weight:700">' + o.id + '</a> · ' + esc(o.name) + '</div>';
      }).join('') : 'нет связанных') + '</div>';
  }"""

if old_render_chat not in text:
    raise SystemExit("renderChat not found")
text = text.replace(old_render_chat, new_render_chat)

# sendMessage note mode
text = text.replace(
    """    c.msgs.push({ me: true, text: text });
    c.unread = 0;
    input.value = '';
    renderChats();
    renderChat();
    log('Сообщение <b>' + esc(c.name) + '</b>: «' + esc(text.slice(0, 42)) + (text.length > 42 ? '…' : '') + '»');

    state.typing = true;
    setTimeout(function () {
      state.typing = false;
      var reply = autoReplies[Math.floor(Math.random() * autoReplies.length)];
      c.msgs.push({ me: false, text: reply });
      renderChat();
      toast(c.name + ' ответила');
    }, 1400);
  }""",
    """    if (state.noteMode) {
      c.msgs.push({ me: false, note: true, text: text });
      input.value = '';
      renderChat();
      toast('Приватная заметка');
      return;
    }
    c.msgs.push({ me: true, text: text });
    c.unread = 0;
    input.value = '';
    renderChats();
    renderChat();
    log('Сообщение <b>' + esc(c.name) + '</b>: «' + esc(text.slice(0, 42)) + (text.length > 42 ? '…' : '') + '»');

    state.typing = true;
    setTimeout(function () {
      state.typing = false;
      var reply = autoReplies[Math.floor(Math.random() * autoReplies.length)];
      c.msgs.push({ me: false, text: reply });
      renderChat();
      toast(c.name + ' ответила');
    }, 1400);
  }""",
)

# append big JS block before INIT
EXTRA_JS = r"""
  /* ────────────────────────── ORDER DRAWER (Dolibarr chain + stream) ────────────────────────── */
  function openOrderDrawer(id) {
    var o = null;
    state.orders.forEach(function (x) { if (x.id === id) o = x; });
    if (!o) return;
    state.openOrderId = id;
    var pay = o.pay || 'pending';
    $('#odTitle').textContent = o.id + ' · ' + o.name;
    $('#odSub').textContent = o.shop + ' · ' + CH_NAMES[o.channel] + ' · ' + (PAY_NAMES[pay] || pay);
    var chain = [
      { k: 'Заказ', on: true, done: true },
      { k: 'Оплата', on: pay === 'paid', done: pay === 'paid' },
      { k: 'Сборка', on: ['assembled','delivering','done'].indexOf(o.status) >= 0, done: ['delivering','done'].indexOf(o.status) >= 0 },
      { k: 'Доставка', on: ['delivering','done'].indexOf(o.status) >= 0, done: o.status === 'done' }
    ];
    var hist = (o.history || []).slice().reverse();
    $('#odBody').innerHTML =
      '<div class="doc-chain">' + chain.map(function (c) {
        return '<span class="' + (c.done ? 'done' : (c.on ? 'on' : '')) + '">' + c.k + '</span>';
      }).join('') + '</div>' +
      '<div style="font-size:0.86rem;color:var(--ink-dim);margin-bottom:8px"><b>Сумма:</b> ' + fmtPrice(o.price) + '</div>' +
      '<div style="font-size:0.86rem;color:var(--ink-dim);margin-bottom:8px"><b>Статус:</b> ' + NAMES[o.status] + '</div>' +
      '<div style="font-size:0.86rem;color:var(--ink-dim);margin-bottom:12px"><b>Оплата:</b> ' + (PAY_NAMES[pay] || pay) + '</div>' +
      '<div style="font-weight:800;font-size:0.84rem;margin-bottom:6px">Лента (Espo-style stream)</div>' +
      '<div class="stream">' + (hist.length ? hist.map(function (h) {
        return '<div class="ev">' + esc(h.text) + '<time>' + new Date(h.t || Date.now()).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }) + '</time></div>';
      }).join('') : '<div class="ev">Пока нет событий</div>') + '</div>';
    var idx = STATUS.indexOf(o.status);
    var next = idx >= 0 && idx < STATUS.length - 1 ? STATUS[idx + 1] : null;
    $('#odFoot').innerHTML =
      (next ? '<button type="button" class="btn terra" id="odAdvance">→ ' + NAMES[next] + '</button>' : '') +
      '<button type="button" class="btn" id="odTogglePay">Сменить оплату</button>';
    $('#drawerScrim').classList.add('show');
    $('#orderDrawer').classList.add('show');
    var adv = $('#odAdvance');
    if (adv) adv.onclick = function () { moveOrder(id, next, { quietToast: false }); };
    $('#odTogglePay').onclick = function () {
      var cycle = ['pending', 'paid', 'cod'];
      var i = cycle.indexOf(o.pay || 'pending');
      o.pay = cycle[(i + 1) % cycle.length];
      o.history = o.history || [];
      o.history.push({ t: Date.now(), text: 'Оплата: ' + PAY_NAMES[o.pay] });
      renderAllKanban();
      openOrderDrawer(id);
      toast('Оплата: ' + PAY_NAMES[o.pay]);
    };
  }

  function closeOrderDrawer() {
    state.openOrderId = null;
    $('#drawerScrim').classList.remove('show');
    $('#orderDrawer').classList.remove('show');
  }

  /* ────────────────────────── VITRINA ────────────────────────── */
  function renderVitrina() {
    var grid = $('#vitGrid');
    if (!grid) return;
    var list = products.filter(function (p) {
      if (vitFilter === 'low') return p.stock > 0 && p.stock <= 3;
      if (vitFilter === 'hidden') return p.hidden;
      return true;
    });
    grid.innerHTML = list.map(function (p) {
      return '<div class="vit-card' + (p.hidden ? ' hidden-sku' : '') + '" data-sku="' + p.id + '">' +
        '<div class="nm">' + esc(p.name) + '</div>' +
        '<div class="pr">' + fmtPrice(p.price) + '</div>' +
        '<div class="st' + (p.stock <= 3 ? ' low' : '') + '">Остаток: <b>' + p.stock + '</b>' + (p.hidden ? ' · скрыт' : '') + '</div>' +
        '<div class="vit-actions">' +
          '<button type="button" data-vit="minus" data-id="' + p.id + '">−</button>' +
          '<button type="button" data-vit="plus" data-id="' + p.id + '">+</button>' +
          '<button type="button" data-vit="price" data-id="' + p.id + '">цена</button>' +
          '<button type="button" data-vit="hide" data-id="' + p.id + '">' + (p.hidden ? 'показать' : 'скрыть') + '</button>' +
        '</div></div>';
    }).join('') || '<div style="color:var(--ink-faint)">Нет позиций</div>';
  }

  function renderSettings() {
    var shops = $('#setShops');
    var users = $('#setUsers');
    if (shops) {
      shops.innerHTML = SIM_SHOPS.map(function (s, i) {
        return '<li>' + esc(s) + '<span>точка ' + (i + 1) + '</span></li>';
      }).join('');
    }
    if (users) {
      users.innerHTML =
        '<li>Анна К. <span>менеджер сети</span></li>' +
        '<li>Игорь М. <span>точка · Мира 14</span></li>' +
        '<li>Света П. <span>флорист</span></li>';
    }
  }

  /* ────────────────────────── CMD+K (Twenty) ────────────────────────── */
  function openCmdk() {
    $('#cmdk').classList.add('show');
    var inp = $('#cmdkInput');
    inp.value = '';
    renderCmdk('');
    setTimeout(function () { inp.focus(); }, 50);
  }
  function closeCmdk() { $('#cmdk').classList.remove('show'); }
  function renderCmdk(q) {
    q = (q || '').toLowerCase();
    var items = [];
    Object.keys(VIEW_NAMES).forEach(function (v) {
      items.push({ t: 'Раздел · ' + VIEW_NAMES[v], k: 'nav', v: v });
    });
    state.orders.slice(0, 12).forEach(function (o) {
      items.push({ t: o.id + ' · ' + o.name, k: 'order', v: o.id });
    });
    chats.forEach(function (c) {
      items.push({ t: 'Чат · ' + c.name, k: 'chat', v: c.id });
    });
    products.forEach(function (p) {
      items.push({ t: 'SKU · ' + p.name, k: 'sku', v: p.id });
    });
    if (q) items = items.filter(function (it) { return it.t.toLowerCase().indexOf(q) >= 0; });
    $('#cmdkList').innerHTML = items.slice(0, 14).map(function (it, i) {
      return '<button type="button" class="cmdk-item' + (i === 0 ? ' on' : '') + '" data-k="' + it.k + '" data-v="' + esc(it.v) + '">' +
        esc(it.t) + '<span class="k">' + it.k + '</span></button>';
    }).join('') || '<div style="padding:16px;color:var(--ink-faint);font-size:0.86rem">Ничего не найдено</div>';
  }
  function runCmdkItem(k, v) {
    closeCmdk();
    if (k === 'nav') switchView(v);
    else if (k === 'order') { switchView('orders'); openOrderDrawer(v); }
    else if (k === 'chat') {
      switchView('chats');
      selectChat(v);
    } else if (k === 'sku') switchView('vitrina');
  }

"""

if "ORDER DRAWER (Dolibarr" not in text:
    text = text.replace("  /* ────────────────────────── INIT ────────────────────────── */", EXTRA_JS + "\n  /* ────────────────────────── INIT ────────────────────────── */")

# bind extensions
old_bind_end = """    if (kanban1) bindDrag(kanban1);
    if (kanban2) bindDrag(kanban2);

    // pause sim while dragging
    document.addEventListener('dragstart', function () { state.simPaused = true; });
    document.addEventListener('dragend', function () { state.simPaused = false; });
    document.addEventListener('visibilitychange', function () {
      state.simPaused = document.hidden;
    });
  }"""

new_bind_end = """    if (kanban1) bindDrag(kanban1);
    if (kanban2) bindDrag(kanban2);

    document.addEventListener('dragstart', function () { state.simPaused = true; });
    document.addEventListener('dragend', function () { state.simPaused = false; });
    document.addEventListener('visibilitychange', function () {
      state.simPaused = document.hidden;
    });

    // open order drawer on card click (not drag)
    document.addEventListener('click', function (e) {
      var card = e.target.closest('.kcard');
      if (card && !e.target.closest('.dragging')) openOrderDrawer(card.getAttribute('data-id'));
      var oo = e.target.closest('[data-open-order]');
      if (oo) { e.preventDefault(); openOrderDrawer(oo.getAttribute('data-open-order')); }
      var vit = e.target.closest('[data-vit]');
      if (vit) {
        var id = vit.getAttribute('data-id');
        var act = vit.getAttribute('data-vit');
        var p = products.filter(function (x) { return x.id === id; })[0];
        if (!p) return;
        if (act === 'plus') p.stock++;
        if (act === 'minus') p.stock = Math.max(0, p.stock - 1);
        if (act === 'price') p.price = Math.max(100, p.price + 100);
        if (act === 'hide') p.hidden = !p.hidden;
        renderVitrina();
        toast(p.name + ' обновлён');
      }
    });

    var odClose = $('#odClose');
    if (odClose) odClose.addEventListener('click', closeOrderDrawer);
    var scr = $('#drawerScrim');
    if (scr) scr.addEventListener('click', closeOrderDrawer);

    var bn = $('#btnNoteMode');
    if (bn) bn.addEventListener('click', function () {
      state.noteMode = !state.noteMode;
      bn.classList.toggle('note-on', state.noteMode);
      $('#chInput').placeholder = state.noteMode ? 'Приватная заметка…' : 'Сообщение';
      toast(state.noteMode ? 'Режим заметки (Chatwoot)' : 'Режим ответа');
    });
    var ba = $('#btnAssignMe');
    if (ba) ba.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.assignee = state.assignee;
      renderChat();
      toast('Назначено: ' + state.assignee);
    });
    var br = $('#btnResolveChat');
    if (br) br.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.resolved = !c.resolved;
      c.msgs.push({ me: false, note: true, text: c.resolved ? 'Диалог решён' : 'Диалог открыт снова' });
      renderChat();
      toast(c.resolved ? 'Диалог решён' : 'Снова открыт');
    });
    var bo = $('#btnOrderFromChat');
    if (bo) bo.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      var channel = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : 'max';
      var prefix = { wa: 'WA', tg: 'TG', max: 'MX' }[channel];
      var id = prefix + '-' + state.nextOrder++;
      var order = {
        id: id, name: 'Букет из чата · ' + c.name, price: 3200, channel: channel,
        status: 'new', shop: c.shop, pay: 'pending',
        history: [{ t: Date.now(), text: 'Создан из чата (Chatwoot pattern)' }]
      };
      state.orders.unshift(order);
      c.orderIds = c.orderIds || [];
      c.orderIds.push(id);
      c.msgs.push({ me: false, note: true, text: 'Создан заказ ' + id });
      flashCard(id, 'is-new', 900);
      renderAllKanban();
      renderChat();
      toast('Заказ ' + id + ' из чата');
      log('Заказ из чата: <b>' + id + '</b> · ' + esc(c.name), 'ok');
    });

    ['vitFilterAll', 'vitFilterLow', 'vitFilterHidden'].forEach(function (id) {
      var el = $('#' + id);
      if (!el) return;
      el.addEventListener('click', function () {
        vitFilter = id === 'vitFilterLow' ? 'low' : id === 'vitFilterHidden' ? 'hidden' : 'all';
        renderVitrina();
      });
    });

    // Twenty ⌘K
    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openCmdk();
      }
      if (e.key === 'Escape') { closeCmdk(); closeOrderDrawer(); }
    });
    var cmdk = $('#cmdk');
    if (cmdk) {
      cmdk.addEventListener('click', function (e) { if (e.target === cmdk) closeCmdk(); });
      $('#cmdkInput').addEventListener('input', function () { renderCmdk(this.value); });
      $('#cmdkList').addEventListener('click', function (e) {
        var it = e.target.closest('.cmdk-item');
        if (it) runCmdkItem(it.getAttribute('data-k'), it.getAttribute('data-v'));
      });
    }
  }"""

if old_bind_end not in text:
    raise SystemExit("bind end not found")
text = text.replace(old_bind_end, new_bind_end)

# init extras
text = text.replace(
    """  renderAllKanban();
  renderChats();
  renderChat();
  renderChart();
  renderReports();
  bind();
  startSim();
})();""",
    """  renderAllKanban();
  renderChats();
  renderChat();
  renderChart();
  renderReports();
  renderVitrina();
  renderSettings();
  bind();
  startSim();
})();""",
)

BASE.write_text(text, encoding="utf-8")
for c in COPIES:
    c.write_text(text, encoding="utf-8")
    print("copied", c)
print("OK", BASE, BASE.stat().st_size)
