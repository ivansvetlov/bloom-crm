# -*- coding: utf-8 -*-
"""Krayin-style Mail + questionnaire-driven Settings on kp/demo/demo.html."""
from pathlib import Path

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
text = BASE.read_text(encoding="utf-8")

if "/* ═══ Krayin: Mail + Settings ═══ */" in text:
    print("Already applied (CSS marker). Exit.")
    raise SystemExit(0)

# ── CSS ──────────────────────────────────────────────────────────────
CSS = r"""
  /* ═══ Krayin: Mail + Settings ═══ */
  .mail-toolbar {
    display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px;
  }
  .mail-toolbar input {
    flex: 1; min-width: 160px; border: 1px solid var(--border-2); border-radius: 10px;
    padding: 9px 12px; font-family: var(--font); font-size: 0.86rem; background: var(--bg-2); outline: none;
  }
  .mail-toolbar input:focus { border-color: var(--terra); }
  .mail-layout {
    display: grid; grid-template-columns: 168px minmax(240px, 300px) 1fr;
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    overflow: hidden; min-height: 520px; box-shadow: var(--shadow-sm);
  }
  .mail-folders {
    background: var(--bg); border-right: 1px solid var(--border); padding: 12px 8px;
  }
  .mail-folder {
    display: flex; align-items: center; gap: 8px; width: 100%;
    padding: 9px 10px; border-radius: 10px; border: 0; background: transparent;
    font-family: var(--font); font-size: 0.84rem; font-weight: 650; color: var(--ink-dim);
    text-align: left; cursor: pointer;
  }
  .mail-folder:hover { background: var(--bg-3); }
  .mail-folder.on { background: var(--terra-soft); color: var(--terra); }
  .mail-folder .n { margin-left: auto; font-size: 0.7rem; font-weight: 800; color: var(--ink-faint); font-family: var(--mono); }
  .mail-folder.on .n { color: var(--terra); }
  .mail-list { border-right: 1px solid var(--border); max-height: 560px; overflow-y: auto; background: var(--bg-2); }
  .mail-row {
    display: grid; grid-template-columns: 1fr auto; gap: 2px 10px;
    padding: 12px 14px; border-bottom: 1px solid var(--border);
    cursor: pointer; text-align: left; width: 100%; border: 0; background: transparent;
    font-family: var(--font); color: var(--ink);
  }
  .mail-row:hover, .mail-row.on { background: var(--bg-3); }
  .mail-row.unread .mail-from { font-weight: 800; }
  .mail-from { font-size: 0.86rem; }
  .mail-subj { font-size: 0.8rem; color: var(--ink-mute); grid-column: 1 / -1; line-height: 1.35; }
  .mail-date { font-size: 0.7rem; color: var(--ink-faint); font-family: var(--mono); }
  .mail-preview { padding: 18px 20px; font-size: 0.9rem; color: var(--ink-dim); line-height: 1.55; min-height: 200px; }
  .mail-preview h3 { font-size: 1.05rem; font-weight: 800; color: var(--ink); margin-bottom: 6px; letter-spacing: -0.02em; }
  .mail-preview .meta { font-size: 0.78rem; color: var(--ink-mute); margin-bottom: 14px; }
  .mail-preview .body {
    white-space: pre-wrap; background: var(--bg); border: 1px solid var(--border);
    border-radius: 12px; padding: 14px; margin-bottom: 14px;
  }
  .mail-preview .links { display: flex; flex-wrap: wrap; gap: 8px; }
  .mail-empty { color: var(--ink-faint); font-size: 0.86rem; padding: 24px 16px; }

  /* Settings: nav + detail */
  .set-shell {
    display: grid; grid-template-columns: 220px 1fr; gap: 14px; align-items: start;
  }
  .set-nav {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 10px 8px; box-shadow: var(--shadow-sm); position: sticky; top: 72px;
  }
  .set-nav-item {
    display: flex; align-items: flex-start; gap: 8px; width: 100%;
    padding: 10px 10px; border: 0; border-radius: 10px; background: transparent;
    font-family: var(--font); text-align: left; cursor: pointer; color: var(--ink-dim);
  }
  .set-nav-item:hover { background: var(--bg-3); }
  .set-nav-item.on { background: var(--terra-soft); color: var(--terra); }
  .set-nav-item .ix {
    font-family: var(--mono); font-size: 0.65rem; font-weight: 800; color: var(--ink-faint);
    min-width: 1.4rem; padding-top: 2px;
  }
  .set-nav-item.on .ix { color: var(--terra); }
  .set-nav-item .tt { font-size: 0.82rem; font-weight: 750; line-height: 1.25; }
  .set-nav-item .sub { font-size: 0.68rem; color: var(--ink-faint); font-weight: 600; margin-top: 2px; }
  .set-nav-item.on .sub { color: var(--terra); opacity: 0.85; }
  .set-panel {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 18px 20px; box-shadow: var(--shadow-sm); min-height: 420px;
  }
  .set-panel h2 {
    font-size: 1.1rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 4px;
  }
  .set-panel .set-lead {
    font-size: 0.82rem; color: var(--ink-mute); margin-bottom: 14px; line-height: 1.45;
  }
  .set-qref {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: var(--mono); font-size: 0.65rem; font-weight: 700;
    color: var(--plum); background: var(--plum-soft); padding: 3px 8px; border-radius: 999px;
    margin-bottom: 12px;
  }
  .set-block { margin-bottom: 16px; }
  .set-block h4 {
    font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em;
    color: var(--ink-faint); margin-bottom: 8px;
  }
  .set-row {
    display: flex; justify-content: space-between; gap: 12px; align-items: flex-start;
    padding: 10px 12px; background: var(--bg); border-radius: 10px; margin-bottom: 6px;
    border: 1px solid var(--border);
  }
  .set-row .k { font-size: 0.84rem; font-weight: 700; color: var(--ink); max-width: 42%; }
  .set-row .v { font-size: 0.82rem; color: var(--ink-dim); text-align: right; line-height: 1.4; flex: 1; }
  .set-row .v b { color: var(--ink); font-weight: 750; }
  .set-row .tag {
    display: inline-block; font-size: 0.65rem; font-weight: 800; padding: 2px 7px;
    border-radius: 999px; margin-left: 6px; vertical-align: middle;
  }
  .set-row .tag.ok { background: var(--sage-soft); color: var(--sage); }
  .set-row .tag.warn { background: var(--amber-soft); color: #A07A20; }
  .set-row .tag.risk { background: var(--red-soft); color: var(--red); }
  .set-row .tag.off { background: var(--bg-3); color: var(--ink-mute); }
  .set-matrix {
    width: 100%; border-collapse: collapse; font-size: 0.78rem; margin-top: 4px;
  }
  .set-matrix th, .set-matrix td {
    border: 1px solid var(--border); padding: 8px 10px; text-align: center;
  }
  .set-matrix th { background: var(--bg); font-size: 0.68rem; text-transform: uppercase; color: var(--ink-faint); }
  .set-matrix td:first-child, .set-matrix th:first-child { text-align: left; font-weight: 700; }
  .set-matrix .y { color: var(--sage); font-weight: 800; }
  .set-matrix .n { color: var(--ink-faint); }
  .set-max {
    margin-top: 14px; padding: 12px 14px; border-radius: 12px;
    background: linear-gradient(135deg, var(--terra-soft), var(--plum-soft));
    border: 1px solid var(--border); font-size: 0.8rem; color: var(--ink-dim); line-height: 1.45;
  }
  .set-max b { color: var(--ink); }
  .set-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
  @media (max-width: 900px) {
    .mail-layout { grid-template-columns: 1fr; }
    .mail-folders { display: flex; flex-wrap: wrap; gap: 4px; border-right: 0; border-bottom: 1px solid var(--border); }
    .mail-list { border-right: 0; max-height: 240px; }
    .set-shell { grid-template-columns: 1fr; }
    .set-nav { position: static; display: flex; flex-wrap: wrap; gap: 4px; }
    .set-nav-item { width: auto; }
  }
"""

text = text.replace("</style>", CSS + "\n</style>")

# ── NAV ──────────────────────────────────────────────────────────────
old_nav = """    <button class="sb-link" data-view="chats"><span class="idx">06</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">07</span>Номенклатура</button>
    <button class="sb-link" data-view="warehouses"><span class="idx">08</span>Склады</button>
    <button class="sb-link" data-view="invoices"><span class="idx">09</span>Счета</button>
    <button class="sb-link" data-view="analytics"><span class="idx">10</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">11</span>Настройки</button>"""

new_nav = """    <button class="sb-link" data-view="chats"><span class="idx">06</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="mail"><span class="idx">07</span>Почта <span class="badge" id="navMail">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">08</span>Номенклатура</button>
    <button class="sb-link" data-view="warehouses"><span class="idx">09</span>Склады</button>
    <button class="sb-link" data-view="invoices"><span class="idx">10</span>Счета</button>
    <button class="sb-link" data-view="analytics"><span class="idx">11</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">12</span>Настройки</button>"""

if old_nav not in text:
    raise SystemExit("nav block not found — check current indices")
text = text.replace(old_nav, new_nav)

# ── SECTIONS: mail + replace settings ────────────────────────────────
MAIL_SECTION = r"""
    <!-- ═════════════ MAIL (Krayin) ═════════════ -->
    <section data-section="mail" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Krayin · Mail folders</span>
        <span class="chip">Связь с клиентом / заказом</span>
      </div>
      <div class="mail-toolbar">
        <button type="button" class="btn terra" id="btnMailCompose">Написать</button>
        <input type="search" id="mailSearch" placeholder="Поиск по письмам…" autocomplete="off" />
        <button type="button" class="btn ghost" id="btnMailRefresh">Обновить</button>
      </div>
      <div class="mail-layout">
        <div class="mail-folders" id="mailFolders"></div>
        <div class="mail-list" id="mailList"></div>
        <div class="mail-preview" id="mailPreview">
          <div class="mail-empty">Выберите письмо</div>
        </div>
      </div>
    </section>

"""

old_settings = """    <section data-section="settings" style="display:none">
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
    </section>"""

new_settings = r"""    <section data-section="settings" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Конфиг под опросник · 25 Q / 9 блоков</span>
        <span class="chip">Максимальные ответы заказчика (демо)</span>
      </div>
      <div class="set-shell">
        <nav class="set-nav" id="setNav"></nav>
        <div class="set-panel" id="setPanel">
          <div class="mail-empty">Выберите раздел настроек</div>
        </div>
      </div>
    </section>"""

if old_settings not in text:
    raise SystemExit("old settings section not found")
text = text.replace(old_settings, MAIL_SECTION + new_settings)

# ── VIEW_NAMES ───────────────────────────────────────────────────────
text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', tasks: 'Задачи', notes: 'Заметки', chats: 'Чаты', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', tasks: 'Задачи', notes: 'Заметки', chats: 'Чаты', mail: 'Почта', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
)

# switchView hooks
text = text.replace(
    """    if (view === 'settings') renderSettings();
    if (view === 'clients') renderClients();
    if (view === 'tasks') renderTasks();
    if (view === 'notes') renderNotes();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
    """    if (view === 'settings') renderSettings();
    if (view === 'clients') renderClients();
    if (view === 'tasks') renderTasks();
    if (view === 'notes') renderNotes();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    if (view === 'mail') renderMail();
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
)

# state fields for mail + settings
if "mailFolder:" not in text:
    text = text.replace(
        """    taskId: null,
    noteId: null
  };""",
        """    taskId: null,
    noteId: null,
    mailFolder: 'inbox',
    mailId: null,
    setSection: 'channels'
  };""",
    )

# ── DATA + JS (replace renderSettings entirely) ──────────────────────
MAIL_SETTINGS_JS = r"""
  /* ────────────────────────── MAIL (Krayin) ────────────────────────── */
  var MAIL_FOLDERS = [
    { id: 'inbox', name: 'Входящие' },
    { id: 'draft', name: 'Черновики' },
    { id: 'outbox', name: 'Исходящие' },
    { id: 'sent', name: 'Отправленные' },
    { id: 'trash', name: 'Корзина' }
  ];
  var mailsSeed = {
    inbox: [
      { id: 'm1', from: 'Марина К.', email: 'marina@mail.ru', subj: 'Re: Фото букета до отправки', date: '11:42', unread: true, body: 'Анна, спасибо! Можем ли добавить открытку с текстом «С 8 марта»?\n\nЖду подтверждения.', clientId: 'c1', orderId: 'FW-1042', shop: 'Мира 14' },
      { id: 'm2', from: 'procurement@office.ru', email: 'procurement@office.ru', subj: 'Корпоративный договор · 12 офисов', date: 'Вчера', unread: true, body: 'Добрый день. Нужен договор на еженедельную поставку в 12 офисов. Просьба выслать КП и условия SLA.', clientId: 'c5', orderId: null, shop: 'Ленина 92' },
      { id: 'm3', from: 'noreply@webform', email: 'form@bloom.local', subj: 'Заявка с сайта · доставка в офис', date: 'Вчера', unread: false, body: 'Новая заявка: букет до 3000 ₽, адрес Строителей 15, к 15:00.\nТел: +7 900 222-33-44', clientId: 'c2', orderId: null, shop: 'Ленина 92' },
      { id: 'm4', from: 'Ирина · маркетплейс', email: 'irina@guest.local', subj: 'Уточнение по замене цветов', date: 'Пн', unread: false, body: 'Менеджер маркетплейса: клиент согласен на замену пионов на ранункулюсы.', clientId: 'c4', orderId: 'FW-1038', shop: 'Мира 14' }
    ],
    draft: [
      { id: 'm5', from: 'я', email: 'shop@bloom.local', subj: 'Черновик: follow-up B2B', date: 'Сегодня', unread: false, body: 'Дмитрий, направляю коммерческое…', clientId: 'c5', orderId: null, shop: 'Ленина 92' }
    ],
    outbox: [],
    sent: [
      { id: 'm6', from: 'я', email: 'shop@bloom.local', subj: 'Счёт и фото · заказ FW-1042', date: 'Вчера', unread: false, body: 'Марина, во вложении счёт и фото букета перед отправкой.', clientId: 'c1', orderId: 'FW-1042', shop: 'Мира 14' },
      { id: 'm7', from: 'я', email: 'shop@bloom.local', subj: 'Подтверждение доставки', date: 'Пн', unread: false, body: 'Заказ доставлен. Будем рады отзыву.', clientId: 'c3', orderId: null, shop: 'Рижская 8' }
    ],
    trash: []
  };
  var mails = JSON.parse(JSON.stringify(mailsSeed));
  var mailSearchQ = '';

  function mailFolderCount(fid) {
    return (mails[fid] || []).length;
  }
  function mailUnreadTotal() {
    return (mails.inbox || []).filter(function (m) { return m.unread; }).length;
  }
  function updateMailBadge() {
    var b = $('#navMail');
    if (b) {
      var n = mailUnreadTotal();
      b.textContent = n ? String(n) : '';
      b.style.display = n ? '' : 'none';
    }
  }
  function filteredMails() {
    var list = mails[state.mailFolder] || [];
    var q = (mailSearchQ || '').toLowerCase();
    if (!q) return list;
    return list.filter(function (m) {
      return (m.from + ' ' + m.subj + ' ' + m.body + ' ' + (m.email || '')).toLowerCase().indexOf(q) >= 0;
    });
  }
  function renderMailFolders() {
    var el = $('#mailFolders');
    if (!el) return;
    el.innerHTML = MAIL_FOLDERS.map(function (f) {
      var n = mailFolderCount(f.id);
      var on = state.mailFolder === f.id ? ' on' : '';
      return '<button type="button" class="mail-folder' + on + '" data-mail-folder="' + f.id + '">' +
        esc(f.name) + (n ? '<span class="n">' + n + '</span>' : '') + '</button>';
    }).join('');
  }
  function renderMail() {
    renderMailFolders();
    updateMailBadge();
    var list = filteredMails();
    var listEl = $('#mailList');
    var prev = $('#mailPreview');
    if (!listEl || !prev) return;
    if (!list.length) {
      listEl.innerHTML = '<div class="mail-empty">Папка пуста</div>';
      prev.innerHTML = '<div class="mail-empty">Нет писем</div>';
      return;
    }
    if (!state.mailId || !list.filter(function (m) { return m.id === state.mailId; })[0]) {
      state.mailId = list[0].id;
    }
    listEl.innerHTML = list.map(function (m) {
      var on = m.id === state.mailId ? ' on' : '';
      var ur = m.unread ? ' unread' : '';
      return '<button type="button" class="mail-row' + on + ur + '" data-mail="' + m.id + '">' +
        '<span class="mail-from">' + esc(m.from) + '</span>' +
        '<span class="mail-date">' + esc(m.date) + '</span>' +
        '<span class="mail-subj">' + esc(m.subj) + '</span></button>';
    }).join('');
    var m = list.filter(function (x) { return x.id === state.mailId; })[0];
    if (!m) {
      prev.innerHTML = '<div class="mail-empty">Выберите письмо</div>';
      return;
    }
    if (m.unread) { m.unread = false; updateMailBadge(); renderMailFolders(); }
    var client = clients.filter(function (c) { return c.id === m.clientId; })[0];
    var links = '';
    if (m.clientId) {
      links += '<button type="button" class="btn terra" data-mail-open-client="' + esc(m.clientId) + '">Клиент' +
        (client ? ' · ' + esc(client.name) : '') + '</button>';
    }
    if (m.orderId) {
      links += '<button type="button" class="btn" data-mail-open-order="' + esc(m.orderId) + '">Заказ ' + esc(m.orderId) + '</button>';
    }
    links += '<button type="button" class="btn ghost" id="btnMailReply">Ответить</button>';
    links += '<button type="button" class="btn ghost" id="btnMailTrash">В корзину</button>';
    prev.innerHTML =
      '<h3>' + esc(m.subj) + '</h3>' +
      '<div class="meta">От: <b>' + esc(m.from) + '</b> &lt;' + esc(m.email || '—') + '&gt; · ' + esc(m.date) +
        (m.shop ? ' · ' + esc(m.shop) : '') + '</div>' +
      '<div class="body">' + esc(m.body) + '</div>' +
      '<div class="links">' + links + '</div>';
    var br = $('#btnMailReply');
    if (br) br.onclick = function () {
      toast('Ответ · черновик (stub Krayin compose)');
      state.mailFolder = 'draft';
      renderMail();
    };
    var bt = $('#btnMailTrash');
    if (bt) bt.onclick = function () {
      var folder = state.mailFolder;
      mails[folder] = (mails[folder] || []).filter(function (x) { return x.id !== m.id; });
      if (!mails.trash) mails.trash = [];
      m.unread = false;
      mails.trash.unshift(m);
      state.mailId = null;
      toast('В корзине');
      renderMail();
    };
  }

  /* ────────────────────────── SETTINGS (опросник 25Q) ────────────────────────── */
  /* Демо: «максимальные» ответы заказчика — верхняя граница потребностей из questions.html */
  var SET_SECTIONS = [
    { id: 'channels', ix: '01', title: 'Каналы и мессенджеры', sub: 'Q1–5 · чаты', q: '1–5' },
    { id: 'marketplace', ix: '02', title: 'Маркетплейс', sub: 'Q6–8 · API и заказы', q: '6–8' },
    { id: 'data', ix: '03', title: 'Данные и склад', sub: 'Q9–11 · клиенты / WMS', q: '9–11' },
    { id: 'staff', ix: '04', title: 'Сотрудники и права', sub: 'Q12–13 · ACL', q: '12–13' },
    { id: 'pay', ix: '05', title: 'Бонусы и оплата', sub: 'Q14–16 · банк / ОФД', q: '14–16' },
    { id: 'sla', ix: '06', title: 'Надёжность и SLA', sub: 'Q17–18 · поддержка', q: '17–18' },
    { id: 'pdn', ix: '07', title: '152‑ФЗ', sub: 'Q19 · ПДн', q: '19' },
    { id: 'scale', ix: '08', title: 'Масштаб сети', sub: 'Q20–23 · точки / пик', q: '20–23' },
    { id: 'delivery', ix: '09', title: 'Доставка', sub: 'Q24–25 · курьеры / трек', q: '24–25' },
    { id: 'mailcfg', ix: '10', title: 'Почта IMAP/SMTP', sub: 'Krayin Email settings', q: '—' },
    { id: 'shops', ix: '11', title: 'Точки и партнёры', sub: 'Контекст сети', q: '20,23' },
    { id: 'integrations', ix: '12', title: 'Интеграции', sub: 'Webhooks · алерты', q: 'ТЗ' }
  ];

  function setRow(k, v, tagHtml) {
    return '<div class="set-row"><div class="k">' + k + '</div><div class="v">' + v + (tagHtml || '') + '</div></div>';
  }
  function setTag(cls, t) {
    return '<span class="tag ' + cls + '">' + t + '</span>';
  }

  function renderSetNav() {
    var nav = $('#setNav');
    if (!nav) return;
    nav.innerHTML = SET_SECTIONS.map(function (s) {
      var on = state.setSection === s.id ? ' on' : '';
      return '<button type="button" class="set-nav-item' + on + '" data-set="' + s.id + '">' +
        '<span class="ix">' + s.ix + '</span>' +
        '<span><div class="tt">' + esc(s.title) + '</div><div class="sub">' + esc(s.sub) + '</div></span></button>';
    }).join('');
  }

  function renderSettings() {
    renderSetNav();
    var panel = $('#setPanel');
    if (!panel) return;
    var sec = SET_SECTIONS.filter(function (s) { return s.id === state.setSection; })[0] || SET_SECTIONS[0];
    var html = '<span class="set-qref">Опросник · вопросы ' + esc(sec.q) + '</span>';
    html += '<h2>' + esc(sec.title) + '</h2>';
    html += '<div class="set-lead">' + esc(sec.sub) + ' · значения ниже = демо «максимум требований» из формы вопросов</div>';

    if (sec.id === 'channels') {
      html += '<div class="set-block"><h4>WhatsApp · Q1–2</h4>';
      html += setRow('Модель подключения', '<b>Личные номера менеджеров</b> через дешёвую платформу', setTag('risk', 'риск бана'));
      html += setRow('Риск блокировки', 'Заказчик <b>принимает</b>; план Б: 3 запасных SIM + резервные аккаунты', setTag('warn', 'план Б'));
      html += setRow('История WA', 'Только диалоги <b>после</b> подключения; выгрузка со старых телефонов — вручную Excel', setTag('ok', 'ок'));
      html += '</div><div class="set-block"><h4>Telegram · Q3</h4>';
      html += setRow('Режим', '<b>Бот</b> с именем/аватаром менеджера (для клиента — как личный чат)', setTag('ok', 'официально'));
      html += setRow('Личные аккаунты TG', 'Не используем (риск бана) — зафиксировано', setTag('off', 'выкл'));
      html += '</div><div class="set-block"><h4>MAX · Q4</h4>';
      html += setRow('Подключение', 'Официальный business API / бот', setTag('ok', 'без бана'));
      html += setRow('Объём', '<b>~800–1500</b> сообщений/мес в пик (8 Марта ×2)', setTag('warn', 'пик'));
      html += '</div><div class="set-block"><h4>Платформа чатов · Q5</h4>';
      html += setRow('Платформа', '<b>Указать после ответа заказчика</b> (цитата ТЗ: «платформу прислали»)', setTag('warn', 'ждём'));
      html += setRow('Каналы платформы', 'WA + TG + MAX (+ опц. VK Community Messages)', setTag('ok', 'мульти'));
      html += setRow('Алерты менеджерам', 'Telegram <b>и</b> VK (по ТЗ «или») — оба канала', setTag('ok', 'TG+VK'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум из формы:</b> личные WA с риском + бот TG «как менеджер» + MAX business + внешняя unlimited-платформа, встраиваемая в inbox; алерты TG и VK; история только post-connect.</div>';
    } else if (sec.id === 'marketplace') {
      html += '<div class="set-block"><h4>API маркетплейса · Q6</h4>';
      html += setRow('Чтение заказов', '<b>Да</b> — список + карточка', setTag('ok', 'read'));
      html += setRow('Смена статусов / отмена', '<b>Да</b>', setTag('ok', 'write'));
      html += setRow('Фото букета', '<b>Загрузка</b> в карточку заказа', setTag('ok', 'photo'));
      html += setRow('Цены и остатки', '<b>Двусторонняя синхронизация</b> каталога', setTag('ok', 'stock'));
      html += '</div><div class="set-block"><h4>Аккаунты · Q7</h4>';
      html += setRow('Сайт', 'Общий маркетплейс', setTag('ok', '1 сайт'));
      html += setRow('Аккаунты', '<b>Отдельный аккаунт на каждую точку</b>', setTag('ok', 'N keys'));
      html += setRow('Bloom', 'Один кабинет на всю сеть; ключи API per-shop', setTag('ok', 'multi-tenant'));
      html += setRow('Каталоги', 'Разные витрины / цены по точкам', setTag('warn', 'сложнее'));
      html += '</div><div class="set-block"><h4>Прямые заказы · Q8</h4>';
      html += setRow('Ручное создание', '<b>Обязательно</b> (телефон, чат, постоянные)', setTag('ok', 'manual'));
      html += setRow('Поля', 'Источник · оплата · магазин-исполнитель · канал', setTag('ok', 'full'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> full API (read+status+photo+price+stock), N shop keys, один Bloom, разные каталоги, ручные заказы со всеми атрибутами.</div>';
    } else if (sec.id === 'data') {
      html += '<div class="set-block"><h4>Клиентская база · Q9–10</h4>';
      html += setRow('Источники', 'Маркетплейс API + Excel менеджеров + legacy CRM CSV', setTag('ok', '3+'));
      html += setRow('Объём', '<b>~25–40 тыс</b> контактов по сети (оценка max)', setTag('warn', 'объём'));
      html += setRow('Чистота', 'Дубли, битые телефоны — <b>чистим при импорте</b> (dedupe)', setTag('ok', 'clean'));
      html += setRow('Правила dedupe', 'Телефон primary · email secondary · merge tags', setTag('ok', 'rules'));
      html += '</div><div class="set-block"><h4>Склад · Q11</h4>';
      html += setRow('Режим v1', '<b>Учёт в Bloom</b> (остатки по точкам + хаб)', setTag('ok', 'native'));
      html += setRow('Внешний WMS', 'Опция 2-й очереди: интеграция при наличии системы', setTag('off', 'later'));
      html += setRow('Синхронизация', 'Bloom → витрина маркетплейса (остатки/цены)', setTag('ok', 'push'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> импорт из 3+ источников, десятки тысяч клиентов, авто-очистка, встроенный склад + задел под внешний WMS.</div>';
    } else if (sec.id === 'staff') {
      html += '<div class="set-block"><h4>Роли · Q12</h4>';
      html += '<table class="set-matrix"><thead><tr><th>Действие</th><th>Флорист</th><th>Менеджер</th><th>Старший</th><th>Директор</th></tr></thead><tbody>';
      html += '<tr><td>Принять / собрать заказ</td><td class="y">✓</td><td class="y">✓</td><td class="y">✓</td><td class="y">✓</td></tr>';
      html += '<tr><td>Отменить заказ</td><td class="n">—</td><td class="y">✓</td><td class="y">✓</td><td class="y">✓</td></tr>';
      html += '<tr><td>Цены / остатки</td><td class="n">—</td><td class="n">—</td><td class="y">✓</td><td class="y">✓</td></tr>';
      html += '<tr><td>Все точки сети</td><td class="n">—</td><td class="n">—</td><td class="n">—</td><td class="y">✓</td></tr>';
      html += '<tr><td>Настройки / API-ключи</td><td class="n">—</td><td class="n">—</td><td class="n">—</td><td class="y">✓</td></tr>';
      html += '</tbody></table></div>';
      html += '<div class="set-block"><h4>Вход · Q13</h4>';
      html += setRow('Аутентификация', 'Логин + пароль (без SMS в v1)', setTag('ok', 'simple'));
      html += setRow('Восстановление', '<b>Админ сети сбрасывает</b> + опц. секретный вопрос', setTag('ok', 'admin reset'));
      html += setRow('Сейчас в демо', 'Анна К. · менеджер · ' + esc(state.shop === '*' ? 'сеть' : state.shop), setTag('ok', 'scope'));
      html += setRow('Пользователи', 'Игорь М. (Мира 14) · Света П. (флорист) · директор (все)', '');
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> 4-уровневый ACL, изоляция по магазину, сброс пароля админом, без SMS-2FA в v1.</div>';
    } else if (sec.id === 'pay') {
      html += '<div class="set-block"><h4>Лояльность · Q14</h4>';
      html += setRow('ТЗ по бонусам', '<b>Отдельный документ</b> — ждём от заказчика (критично для схемы БД)', setTag('warn', 'блокер'));
      html += setRow('Задел в схеме', 'Поля баллов / уровней — reserved', setTag('ok', 'schema'));
      html += '</div><div class="set-block"><h4>Банк · Q15</h4>';
      html += setRow('v1', 'Только отметка <b>«оплачено»</b> вручную', setTag('ok', 'manual pay'));
      html += setRow('Эквайринг', 'Отдельный этап: банк + схема + договор', setTag('off', 'v2+'));
      html += '</div><div class="set-block"><h4>ОФД · Q16</h4>';
      html += setRow('Онлайн-чеки', '<b>Не в v1</b>', setTag('off', 'v2'));
      html += setRow('Если критично сразу', 'Заложить 2-ю очередь: касса + ОФД + интеграция', setTag('warn', 'queue'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> полное ТЗ лояльности ASAP; банк и ОФД как отдельные этапы (не раздувать v1).</div>';
    } else if (sec.id === 'sla') {
      html += '<div class="set-block"><h4>Надёжность · Q17</h4>';
      html += setRow('SLA в договоре', 'Реакция <b>≤ 4 ч</b> · восстановление <b>≤ 8 ч</b> (рабочее время)', setTag('ok', 'SLA'));
      html += setRow('Код и доступы', 'Полная передача заказчику при сдаче', setTag('ok', 'escrow-free'));
      html += setRow('Бэкапы', 'Ежедневные + мониторинг uptime в базе', setTag('ok', 'backup'));
      html += setRow('Особые требования', 'Пик 8 Марта: capacity plan + hot standby (если запросят)', setTag('warn', 'пик'));
      html += '</div><div class="set-block"><h4>Сопровождение · Q18</h4>';
      html += setRow('Модель', '<b>Поддержка инфраструктуры</b> (сервер, обновления, реакция) — рекомендуем', setTag('ok', 'managed'));
      html += setRow('Альтернатива', 'Полная передача: код + доступы + сервер — клиент сам', setTag('off', 'hand-off'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> жёсткий SLA + managed support + capacity на пик; код всё равно у клиента.</div>';
    } else if (sec.id === 'pdn') {
      html += '<div class="set-block"><h4>Персональные данные · Q19</h4>';
      html += setRow('Сервера', 'РФ (соответствие 152‑ФЗ)', setTag('ok', 'RU'));
      html += setRow('Документы', '<b>В рамках проекта</b>: политика, согласия, журнал действий', setTag('ok', 'в проекте'));
      html += setRow('У заказчика уже есть', 'Частично — сводим и дополняем', setTag('warn', 'merge'));
      html += setRow('Хранение', 'Имена, телефоны, переписка — срок и основания в политике', setTag('ok', 'policy'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> полный пакет ПДн в проекте + сервера РФ + audit log действий сотрудников.</div>';
    } else if (sec.id === 'scale') {
      html += '<div class="set-block"><h4>Объём · Q20–22</h4>';
      html += setRow('Точки сейчас', '<b>3</b> (Мира 14 · Ленина 92 · Рижская 8)', setTag('ok', 'demo'));
      html += setRow('Через год', 'До <b>12–15</b> (рост ×4–5)', setTag('warn', 'scale'));
      html += setRow('Менеджеры одновременно', '<b>8–12</b> в пик (не «2 или 20» — точное число ждём)', setTag('ok', 'concurrent'));
      html += setRow('Заказов в пик / день', '<b>400–800</b> сеть (8 Марта / НГ) — для sizing серверов', setTag('warn', 'peak'));
      html += '</div><div class="set-block"><h4>Партнёры · Q23</h4>';
      html += setRow('Партнёрские точки', 'Точки маркетплейса + франчайзи с ограниченным доступом', setTag('ok', 'partners'));
      html += setRow('Права партнёра', 'Только свои заказы / свой склад · без сети', setTag('ok', 'isolate'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> рост до 15 точек, десятки менеджеров, сотни заказов/день в пик, партнёры с изоляцией.</div>';
    } else if (sec.id === 'delivery') {
      html += '<div class="set-block"><h4>Кто доставляет · Q24</h4>';
      html += setRow('Модель', '<b>Смешанная:</b> курьеры маркетплейса + свои + сторонняя служба', setTag('ok', 'hybrid'));
      html += setRow('Статус «В доставке»', 'Единый статус; источник курьера — поле на заказе', setTag('ok', 'field'));
      html += '</div><div class="set-block"><h4>Трек · Q25</h4>';
      html += setRow('Карта / GPS', 'Желательно для своих курьеров (2-я очередь)', setTag('warn', 'v2 map'));
      html += setRow('v1', 'Статус + сообщение клиенту «заказ в пути» + трек-номер если есть', setTag('ok', 'status'));
      html += setRow('Маркетплейс-курьер', 'Трек из API маркетплейса (если отдаёт)', setTag('ok', 'API track'));
      html += '</div>';
      html += '<div class="set-max"><b>Максимум:</b> hybrid delivery + GPS later; v1 — статусы + push клиенту + трек-номер.</div>';
    } else if (sec.id === 'mailcfg') {
      html += '<div class="set-block"><h4>Krayin Email settings</h4>';
      html += setRow('Ящик сети', 'orders@bloom.local (IMAP)', setTag('ok', 'inbox'));
      html += setRow('SMTP', 'smtp.bloom.local:587 · TLS', setTag('ok', 'send'));
      html += setRow('Подпись', '«Bloom · [точка] · +7…» подставляется по магазину', setTag('ok', 'sign'));
      html += setRow('Шаблоны', 'Счёт · фото · follow-up B2B · отказ', setTag('ok', 'tpl'));
      html += setRow('Связь', 'Письмо ↔ клиент / заказ (как Lead link в Krayin)', setTag('ok', 'link'));
      html += '</div>';
      html += '<div class="set-actions"><button type="button" class="btn terra" id="btnGoMail">Открыть Почту</button></div>';
      html += '<div class="set-max"><b>Паттерн Krayin:</b> folders + compose + entity-linked thread. Не замена мессенджеров — email-канал рядом с inbox.</div>';
    } else if (sec.id === 'shops') {
      var shops = ['Мира 14', 'Ленина 92', 'Рижская 8'];
      html += '<div class="set-block"><h4>Точки</h4>';
      shops.forEach(function (s, i) {
        var active = state.shop === s ? setTag('ok', 'контекст') : '';
        html += setRow('Точка ' + (i + 1), '<b>' + esc(s) + '</b> · ключ API · склад · каталог', active);
      });
      html += setRow('Вся сеть', state.shop === '*' ? '<b>активный контекст</b>' : 'переключить в сайдбаре', state.shop === '*' ? setTag('ok', 'now') : '');
      html += '</div><div class="set-block"><h4>Партнёры (см. Q23)</h4>';
      html += setRow('Партнёр «Флора Юг»', 'Только свои заказы · read-only цены сети', setTag('warn', 'partner'));
      html += setRow('Франчайзи «Букет 24»', 'Свой склад · без доступа к чужим клиентам', setTag('ok', 'franchise'));
      html += '</div>';
    } else if (sec.id === 'integrations') {
      html += '<div class="set-block"><h4>Каналы и внешние системы</h4>';
      html += setRow('Маркетплейс', 'Подключён · multi-account', setTag('ok', 'live'));
      html += setRow('WhatsApp / TG / MAX', 'Через платформу чатов (Q5)', setTag('ok', 'inbox'));
      html += setRow('VK alerts', 'Community Messages / Callback · 0–2 тыс ₽/мес', setTag('ok', 'alerts'));
      html += setRow('Webhooks', 'order.created · status.changed · stock.low', setTag('ok', 'hooks'));
      html += setRow('Паттерны UI', 'Chatwoot · Twenty · Dolibarr · Krayin mail', setTag('ok', 'OSS'));
      html += '</div>';
      html += '<div class="set-max"><b>Итог:</b> настройки = живая карта ответов на 25 вопросов формы. Меняются вместе со сметой.</div>';
    }

    html += '<div class="set-actions">';
    html += '<button type="button" class="btn ghost" id="btnSetSave">Сохранить (демо)</button>';
    html += '<button type="button" class="btn ghost" id="btnSetQs">Форма вопросов →</button>';
    html += '</div>';

    panel.innerHTML = html;

    var bg = $('#btnGoMail');
    if (bg) bg.onclick = function () { switchView('mail'); };
    var bs = $('#btnSetSave');
    if (bs) bs.onclick = function () { toast('Настройки сохранены (демо, local only)'); };
    var bq = $('#btnSetQs');
    if (bq) bq.onclick = function () {
      window.open('../../questions.html', '_blank');
    };
  }

"""

# Replace old renderSettings function
import re
old_rs = re.search(
    r"  function renderSettings\(\) \{\n    var shops = \$\('#setShops'\);.*?  \}\n\n  /\* ────────────────────────── CMD\+K",
    text,
    re.S,
)
if not old_rs:
    raise SystemExit("renderSettings block not found")
text = text[: old_rs.start()] + MAIL_SETTINGS_JS + "\n  /* ────────────────────────── CMD+K" + text[old_rs.end() - len("  /* ────────────────────────── CMD+K") :]

# Bind mail events — inject before INIT or into bind if exists
# Look for function bind
if "function bind()" in text and "data-mail-folder" not in text:
    # inject into document click / after bind start
    BIND_MAIL = r"""
    /* Mail + Settings nav */
    document.addEventListener('click', function (e) {
      var mf = e.target.closest('[data-mail-folder]');
      if (mf) {
        state.mailFolder = mf.getAttribute('data-mail-folder');
        state.mailId = null;
        renderMail();
        return;
      }
      var mr = e.target.closest('[data-mail]');
      if (mr && mr.getAttribute('data-mail')) {
        state.mailId = mr.getAttribute('data-mail');
        renderMail();
        return;
      }
      var mc = e.target.closest('[data-mail-open-client]');
      if (mc) {
        state.clientId = mc.getAttribute('data-mail-open-client');
        switchView('clients');
        if (typeof renderClients === 'function') renderClients();
        return;
      }
      var mo = e.target.closest('[data-mail-open-order]');
      if (mo) {
        switchView('orders');
        if (typeof openOrderDrawer === 'function') openOrderDrawer(mo.getAttribute('data-mail-open-order'));
        return;
      }
      var ss = e.target.closest('[data-set]');
      if (ss) {
        state.setSection = ss.getAttribute('data-set');
        renderSettings();
        return;
      }
    });
    var mSearch = $('#mailSearch');
    if (mSearch) mSearch.addEventListener('input', function () { mailSearchQ = this.value; renderMail(); });
    var mCompose = $('#btnMailCompose');
    if (mCompose) mCompose.addEventListener('click', function () {
      var id = 'm' + Date.now();
      if (!mails.draft) mails.draft = [];
      mails.draft.unshift({
        id: id, from: 'я', email: 'shop@bloom.local', subj: 'Новое письмо', date: 'Сейчас',
        unread: false, body: '…', clientId: null, orderId: null, shop: state.shop === '*' ? 'Мира 14' : state.shop
      });
      state.mailFolder = 'draft';
      state.mailId = id;
      renderMail();
      toast('Черновик создан');
    });
    var mRef = $('#btnMailRefresh');
    if (mRef) mRef.addEventListener('click', function () { renderMail(); toast('Почта обновлена'); });
"""
    # Find bind function body - append at start of bind after '{'
    m = re.search(r"function bind\(\)\s*\{", text)
    if m:
        insert_at = m.end()
        text = text[:insert_at] + "\n" + BIND_MAIL + text[insert_at:]
    else:
        # fallback: before INIT
        text = text.replace(
            "  /* ────────────────────────── INIT ────────────────────────── */",
            "  function bindMailSettings() {" + BIND_MAIL + "\n  }\n\n  /* ────────────────────────── INIT ────────────────────────── */",
        )
        text = text.replace(
            "  bind();\n",
            "  bind();\n  if (typeof bindMailSettings === 'function') bindMailSettings();\n",
        )

# Init calls
if "renderMail();" not in text.split("INIT")[-1] if "INIT" in text else True:
    text = text.replace(
        "  renderSettings();\n  updateShopBanner();",
        "  renderSettings();\n  renderMail();\n  updateMailBadge();\n  updateShopBanner();",
    )

# cmdk should include mail
if "Раздел · " in text and "mail" not in text[text.find("function renderCmdk"):text.find("function renderCmdk")+800]:
    pass  # VIEW_NAMES already includes mail so cmdk will pick it up

BASE.write_text(text, encoding="utf-8")
print("Wrote", BASE, "bytes", BASE.stat().st_size)

for c in COPIES:
    try:
        c.parent.mkdir(parents=True, exist_ok=True)
        c.write_text(text, encoding="utf-8")
        print("Mirrored", c)
    except Exception as ex:
        print("Mirror fail", c, ex)

print("OK")
