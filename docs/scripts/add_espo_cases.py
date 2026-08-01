# -*- coding: utf-8 -*-
"""EspoCRM Cases → Bloom «Обращения» (жалобы / обратная связь / претензии)."""
from pathlib import Path
import re

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
text = BASE.read_text(encoding="utf-8")

if "/* ═══ EspoCRM: Cases → Обращения ═══ */" in text:
    print("Already applied. Exit.")
    raise SystemExit(0)

# ── CSS ──────────────────────────────────────────────────────────────
CSS = r"""
  /* ═══ EspoCRM: Cases → Обращения ═══ */
  .cs-toolbar {
    display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px;
  }
  .cs-toolbar input, .cs-toolbar select {
    border: 1px solid var(--border-2); border-radius: 10px; padding: 9px 12px;
    font-family: var(--font); font-size: 0.86rem; background: var(--bg-2); outline: none;
  }
  .cs-toolbar input { flex: 1; min-width: 160px; }
  .cs-toolbar input:focus, .cs-toolbar select:focus { border-color: var(--terra); }
  .cs-view-toggle {
    display: inline-flex; border: 1px solid var(--border-2); border-radius: 10px; overflow: hidden;
  }
  .cs-view-toggle button {
    border: 0; background: var(--bg-2); padding: 8px 12px; font-family: var(--font);
    font-size: 0.78rem; font-weight: 700; color: var(--ink-mute); cursor: pointer;
  }
  .cs-view-toggle button.on { background: var(--terra-soft); color: var(--terra); }
  .cs-layout {
    display: grid; grid-template-columns: 1fr minmax(300px, 360px); gap: 14px; align-items: start;
  }
  .cs-table {
    width: 100%; border-collapse: collapse; background: var(--bg-2);
    border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
    box-shadow: var(--shadow-sm);
  }
  .cs-table th {
    text-align: left; font-size: 0.68rem; font-weight: 700; color: var(--ink-faint);
    text-transform: uppercase; letter-spacing: 0.04em;
    padding: 10px 12px; border-bottom: 1px solid var(--border); background: var(--bg);
  }
  .cs-table td {
    padding: 11px 12px; border-bottom: 1px solid var(--border);
    font-size: 0.86rem; color: var(--ink-dim); vertical-align: middle; cursor: pointer;
  }
  .cs-table tr:last-child td { border-bottom: 0; }
  .cs-table tr:hover td { background: var(--bg-3); }
  .cs-table tr.on td { background: var(--terra-soft); }
  .cs-table .title { font-weight: 800; color: var(--ink); letter-spacing: -0.01em; }
  .cs-table .sub { font-size: 0.72rem; color: var(--ink-mute); margin-top: 2px; }
  .cs-badge {
    font-size: 0.65rem; font-weight: 800; padding: 3px 8px; border-radius: 999px;
    background: var(--bg-3); color: var(--ink-mute); white-space: nowrap;
  }
  .cs-badge.new { background: #E8F1FB; color: #3A7BD5; }
  .cs-badge.assigned { background: var(--plum-soft); color: var(--plum); }
  .cs-badge.progress { background: var(--amber-soft); color: #A07A20; }
  .cs-badge.waiting { background: #F0E8F8; color: #7B4BA0; }
  .cs-badge.closed { background: var(--sage-soft); color: var(--sage); }
  .cs-badge.pri-low { background: var(--bg-3); color: var(--ink-mute); }
  .cs-badge.pri-med { background: var(--amber-soft); color: #A07A20; }
  .cs-badge.pri-high { background: var(--terra-soft); color: var(--terra); }
  .cs-badge.pri-crit { background: var(--red-soft); color: var(--red); }
  .cs-badge.type-complaint { background: var(--red-soft); color: var(--red); }
  .cs-badge.type-feedback { background: var(--sage-soft); color: var(--sage); }
  .cs-badge.type-claim { background: var(--amber-soft); color: #A07A20; }
  .cs-badge.type-question { background: #E8F1FB; color: #3A7BD5; }
  .cs-detail {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 16px; box-shadow: var(--shadow-sm); position: sticky; top: 72px; min-height: 280px;
  }
  .cs-detail h3 { font-size: 1.02rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 4px; }
  .cs-detail .meta { font-size: 0.78rem; color: var(--ink-mute); margin-bottom: 10px; line-height: 1.4; }
  .cs-detail .body {
    font-size: 0.88rem; color: var(--ink-dim); line-height: 1.5;
    white-space: pre-wrap; background: var(--bg); border-radius: 12px; padding: 12px;
    border: 1px solid var(--border); margin-bottom: 12px; min-height: 56px;
  }
  .cs-detail .row {
    display: flex; justify-content: space-between; gap: 8px; padding: 7px 0;
    border-bottom: 1px solid var(--border); font-size: 0.84rem;
  }
  .cs-detail .row span { color: var(--ink-mute); font-weight: 600; font-size: 0.74rem; }
  .cs-detail .actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
  .cs-empty { color: var(--ink-faint); font-size: 0.86rem; padding: 8px 0; }

  /* Stream (Espo) */
  .cs-stream-title {
    font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;
    color: var(--ink-faint); margin: 14px 0 8px;
  }
  .cs-stream { display: flex; flex-direction: column; gap: 0; max-height: 260px; overflow-y: auto; }
  .cs-stream-item {
    display: flex; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--border);
    font-size: 0.82rem;
  }
  .cs-stream-item:last-child { border-bottom: 0; }
  .cs-stream-ico {
    width: 28px; height: 28px; border-radius: 8px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 800; background: var(--bg-3); color: var(--ink-mute);
  }
  .cs-stream-ico.note { background: var(--amber-soft); color: #A07A20; }
  .cs-stream-ico.status { background: var(--plum-soft); color: var(--plum); }
  .cs-stream-ico.create { background: #E8F1FB; color: #3A7BD5; }
  .cs-stream-ico.email { background: var(--sage-soft); color: var(--sage); }
  .cs-stream-head { display: flex; justify-content: space-between; gap: 8px; margin-bottom: 2px; }
  .cs-stream-who { font-weight: 750; color: var(--ink); }
  .cs-stream-when { color: var(--ink-faint); font-size: 0.7rem; font-family: var(--mono); white-space: nowrap; }
  .cs-stream-text { color: var(--ink-dim); line-height: 1.4; }
  .cs-compose {
    display: flex; flex-direction: column; gap: 8px; margin-top: 10px;
  }
  .cs-compose textarea {
    width: 100%; min-height: 64px; resize: vertical; border: 1px solid var(--border-2);
    border-radius: 10px; padding: 10px 12px; font-family: var(--font); font-size: 0.84rem;
    background: var(--bg); outline: none;
  }
  .cs-compose textarea:focus { border-color: var(--terra); }

  /* Kanban */
  .cs-kanban {
    display: grid; grid-template-columns: repeat(5, minmax(160px, 1fr)); gap: 10px;
    overflow-x: auto; padding-bottom: 6px;
  }
  .cs-kcol {
    background: var(--bg); border: 1px solid var(--border); border-radius: 12px;
    min-height: 320px; display: flex; flex-direction: column;
  }
  .cs-kcol-head {
    padding: 10px 12px; font-size: 0.78rem; font-weight: 800;
    border-bottom: 1px solid var(--border); display: flex; justify-content: space-between;
    border-top: 3px solid var(--border-2); border-radius: 12px 12px 0 0;
  }
  .cs-kcol-head.st-new { border-top-color: #3A7BD5; }
  .cs-kcol-head.st-assigned { border-top-color: var(--plum); }
  .cs-kcol-head.st-progress { border-top-color: var(--amber); }
  .cs-kcol-head.st-waiting { border-top-color: #7B4BA0; }
  .cs-kcol-head.st-closed { border-top-color: var(--sage); }
  .cs-kcol-head .cnt {
    font-family: var(--mono); font-size: 0.7rem; color: var(--ink-faint); font-weight: 700;
  }
  .cs-kcards { padding: 8px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
  .cs-kcard {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: 10px;
    padding: 10px 12px; cursor: pointer; text-align: left; width: 100%;
    font-family: var(--font); box-shadow: var(--shadow-sm);
  }
  .cs-kcard:hover { border-color: var(--terra); }
  .cs-kcard.on { border-color: var(--terra); background: var(--terra-soft); }
  .cs-kcard .kt { font-size: 0.84rem; font-weight: 800; color: var(--ink); margin-bottom: 4px; line-height: 1.3; }
  .cs-kcard .km { font-size: 0.72rem; color: var(--ink-mute); display: flex; flex-wrap: wrap; gap: 4px; align-items: center; }
  .cs-kcard .adv {
    margin-top: 8px; font-size: 0.7rem; font-weight: 700; color: var(--terra);
    background: none; border: 0; cursor: pointer; padding: 0; font-family: var(--font);
  }
  .cs-kcard .adv:hover { text-decoration: underline; }
  @media (max-width: 900px) {
    .cs-layout { grid-template-columns: 1fr; }
    .cs-detail { position: static; }
    .cs-kanban { grid-template-columns: repeat(2, minmax(180px, 1fr)); }
  }
"""

text = text.replace("</style>", CSS + "\n</style>")

# ── NAV ──────────────────────────────────────────────────────────────
old_nav = """    <button class="sb-link" data-view="mail"><span class="idx">07</span>Почта <span class="badge" id="navMail">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">08</span>Номенклатура</button>
    <button class="sb-link" data-view="warehouses"><span class="idx">09</span>Склады</button>
    <button class="sb-link" data-view="invoices"><span class="idx">10</span>Счета</button>
    <button class="sb-link" data-view="analytics"><span class="idx">11</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">12</span>Настройки</button>"""

new_nav = """    <button class="sb-link" data-view="mail"><span class="idx">07</span>Почта <span class="badge" id="navMail">0</span></button>
    <button class="sb-link" data-view="cases"><span class="idx">08</span>Обращения <span class="badge" id="navCases">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">09</span>Номенклатура</button>
    <button class="sb-link" data-view="warehouses"><span class="idx">10</span>Склады</button>
    <button class="sb-link" data-view="invoices"><span class="idx">11</span>Счета</button>
    <button class="sb-link" data-view="analytics"><span class="idx">12</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">13</span>Настройки</button>"""

if old_nav not in text:
    raise SystemExit("nav block not found")
text = text.replace(old_nav, new_nav)

# ── SECTION ──────────────────────────────────────────────────────────
SECTION = r"""
    <!-- ═════════════ CASES / ОБРАЩЕНИЯ (EspoCRM) ═════════════ -->
    <section data-section="cases" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">EspoCRM · Cases</span>
        <span class="chip">Жалобы · обратная связь · претензии</span>
        <span class="chip">Отдельно от заказа (KPI)</span>
      </div>
      <div class="cs-toolbar">
        <input type="search" id="caseSearch" placeholder="Поиск обращений…" autocomplete="off" />
        <select id="caseStatusFilter">
          <option value="*">Все статусы</option>
          <option value="new">Новое</option>
          <option value="assigned">Назначено</option>
          <option value="progress">В работе</option>
          <option value="waiting">Ждёт клиента</option>
          <option value="closed">Закрыто</option>
        </select>
        <select id="caseTypeFilter">
          <option value="*">Все типы</option>
          <option value="complaint">Жалоба</option>
          <option value="feedback">Обратная связь</option>
          <option value="claim">Претензия</option>
          <option value="question">Вопрос</option>
        </select>
        <div class="cs-view-toggle">
          <button type="button" class="on" data-case-view="list">Список</button>
          <button type="button" data-case-view="kanban">Канбан</button>
        </div>
        <button type="button" class="btn terra" id="btnAddCase">+ Обращение</button>
      </div>
      <div id="casesListWrap">
        <div class="cs-layout">
          <div>
            <table class="cs-table">
              <thead>
                <tr>
                  <th>№</th><th>Тема</th><th>Тип</th><th>Статус</th><th>Приоритет</th><th>Клиент / заказ</th><th>Ответственный</th>
                </tr>
              </thead>
              <tbody id="casesBody"></tbody>
            </table>
          </div>
          <aside class="cs-detail" id="caseDetail">
            <div class="cs-empty">Выберите обращение · Case + Stream (EspoCRM)</div>
          </aside>
        </div>
      </div>
      <div id="casesKanbanWrap" style="display:none">
        <div class="cs-kanban" id="casesKanban"></div>
        <aside class="cs-detail" id="caseDetailKanban" style="margin-top:14px">
          <div class="cs-empty">Клик по карточке — детали и лента</div>
        </aside>
      </div>
    </section>

"""

if 'data-section="cases"' not in text:
    text = text.replace(
        '    <!-- ═════════════ MAIL (Krayin) ═════════════ -->',
        SECTION + '    <!-- ═════════════ MAIL (Krayin) ═════════════ -->',
    )

# ── VIEW_NAMES ───────────────────────────────────────────────────────
text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', tasks: 'Задачи', notes: 'Заметки', chats: 'Чаты', mail: 'Почта', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', tasks: 'Задачи', notes: 'Заметки', chats: 'Чаты', mail: 'Почта', cases: 'Обращения', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
)

# switchView
text = text.replace(
    """    if (view === 'mail') renderMail();
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
    """    if (view === 'mail') renderMail();
    if (view === 'cases') renderCases();
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
)

# state
if "caseId:" not in text:
    text = text.replace(
        """    mailFolder: 'inbox',
    mailId: null,
    setSection: 'channels'
  };""",
        """    mailFolder: 'inbox',
    mailId: null,
    setSection: 'channels',
    caseId: null
  };""",
    )

# ── DATA after notes ─────────────────────────────────────────────────
DATA = r"""
  var casesSeed = [
    {
      id: 'CS-104', number: 'CS-104',
      title: 'Букет пришёл увядшим',
      type: 'complaint', priority: 'high', status: 'progress',
      clientId: 'c1', clientName: 'Марина К.', orderId: 'FW-1042',
      shop: 'Мира 14', assignee: 'Анна К.',
      channel: 'wa', created: 'сегодня 09:20',
      body: 'Клиент: цветы выглядели уставшими при получении. Просит частичный возврат или повторную доставку.',
      stream: [
        { kind: 'create', who: 'Система', when: '09:20', text: 'Обращение создано из WhatsApp' },
        { kind: 'status', who: 'Анна К.', when: '09:25', text: 'Статус → В работе' },
        { kind: 'note', who: 'Анна К.', when: '09:40', text: 'Запросили фото у клиента. Сверяем с фото перед отправкой.' }
      ]
    },
    {
      id: 'CS-103', number: 'CS-103',
      title: 'Спасибо за 8 Марта — хочу постоянным',
      type: 'feedback', priority: 'low', status: 'new',
      clientId: 'c3', clientName: 'Елена С.', orderId: null,
      shop: 'Рижская 8', assignee: '—',
      channel: 'max', created: 'сегодня 10:05',
      body: 'Положительный отзыв. Просит завести в программу лояльности, когда будет готова.',
      stream: [
        { kind: 'create', who: 'Система', when: '10:05', text: 'Обращение из MAX · обратная связь' }
      ]
    },
    {
      id: 'CS-102', number: 'CS-102',
      title: 'Претензия: опоздание курьера 40 мин',
      type: 'claim', priority: 'crit', status: 'assigned',
      clientId: 'c5', clientName: 'Дмитрий П.', orderId: 'FW-1038',
      shop: 'Ленина 92', assignee: 'Игорь М.',
      channel: 'email', created: 'вчера',
      body: 'B2B-клиент. Слот 14:00, факт 14:40. Просит скидку на следующий корпоратив.',
      stream: [
        { kind: 'create', who: 'Система', when: 'вчера 15:10', text: 'Из почты · email-to-case' },
        { kind: 'email', who: 'Дмитрий П.', when: 'вчера 15:12', text: 'Ожидаю письменный ответ до конца дня.' },
        { kind: 'status', who: 'Игорь М.', when: 'вчера 16:00', text: 'Назначено · Ленина 92' }
      ]
    },
    {
      id: 'CS-101', number: 'CS-101',
      title: 'Можно ли заменить пионы на ранункулюсы?',
      type: 'question', priority: 'med', status: 'waiting',
      clientId: 'c4', clientName: 'Ирина', orderId: 'FW-1038',
      shop: 'Мира 14', assignee: 'Анна К.',
      channel: 'fw', created: 'вчера',
      body: 'Вопрос по замене состава. Ждём подтверждение клиента в чате маркетплейса.',
      stream: [
        { kind: 'create', who: 'Система', when: 'вчера 12:00', text: 'Из чата маркетплейса' },
        { kind: 'status', who: 'Анна К.', when: 'вчера 12:30', text: 'Ждёт клиента' },
        { kind: 'note', who: 'Анна К.', when: 'вчера 12:31', text: 'Отправили фото альтернативы.' }
      ]
    },
    {
      id: 'CS-100', number: 'CS-100',
      title: 'Неверный адрес на открытке',
      type: 'complaint', priority: 'med', status: 'closed',
      clientId: 'c2', clientName: 'Алексей', orderId: null,
      shop: 'Ленина 92', assignee: 'Света П.',
      channel: 'tg', created: '2 дня назад',
      body: 'Открытка с опечаткой. Переделали и отправили повторно. Клиент доволен.',
      stream: [
        { kind: 'create', who: 'Система', when: '2д', text: 'Из Telegram' },
        { kind: 'status', who: 'Света П.', when: '2д', text: 'Закрыто · повторная доставка' },
        { kind: 'note', who: 'Света П.', when: '2д', text: 'Компенсация: бесплатная открытка в след. заказ.' }
      ]
    }
  ];
  var cases = JSON.parse(JSON.stringify(casesSeed));
  var caseFilterStatus = '*';
  var caseFilterType = '*';
  var caseSearchQ = '';
  var caseViewMode = 'list';
  var CASE_ST = { new: 'Новое', assigned: 'Назначено', progress: 'В работе', waiting: 'Ждёт клиента', closed: 'Закрыто' };
  var CASE_ST_ORDER = ['new', 'assigned', 'progress', 'waiting', 'closed'];
  var CASE_TYPE = { complaint: 'Жалоба', feedback: 'Обратная связь', claim: 'Претензия', question: 'Вопрос' };
  var CASE_PRI = { low: 'Низкий', med: 'Средний', high: 'Высокий', crit: 'Критичный' };
"""

if "var casesSeed" not in text:
    # insert after notes seed block
    anchor = "  var notes = JSON.parse(JSON.stringify(notesSeed));"
    if anchor not in text:
        # try after mail
        anchor = "  var mailSearchQ = '';"
    text = text.replace(anchor, anchor + "\n" + DATA, 1)

# ── JS module ────────────────────────────────────────────────────────
CASES_JS = r"""
  /* ────────────────────────── CASES / ОБРАЩЕНИЯ (EspoCRM) ────────────────────────── */
  function updateCasesBadge() {
    var b = $('#navCases');
    if (!b) return;
    var n = cases.filter(function (c) { return c.status !== 'closed'; }).length;
    b.textContent = n ? String(n) : '';
    b.style.display = n ? '' : 'none';
  }

  function filteredCases() {
    var q = (caseSearchQ || '').toLowerCase();
    return cases.filter(function (c) {
      if (caseFilterStatus !== '*' && c.status !== caseFilterStatus) return false;
      if (caseFilterType !== '*' && c.type !== caseFilterType) return false;
      if (state.shop !== '*' && c.shop !== state.shop) return false;
      if (q) {
        var blob = (c.number + ' ' + c.title + ' ' + c.body + ' ' + (c.clientName || '') + ' ' + (c.orderId || '') + ' ' + (c.assignee || '')).toLowerCase();
        if (blob.indexOf(q) < 0) return false;
      }
      return true;
    });
  }

  function caseStreamIco(kind) {
    var map = { note: 'N', status: 'S', create: '+', email: '@' };
    return map[kind] || '·';
  }

  function renderCases() {
    updateCasesBadge();
    var listW = $('#casesListWrap');
    var kanW = $('#casesKanbanWrap');
    if (listW) listW.style.display = caseViewMode === 'list' ? '' : 'none';
    if (kanW) kanW.style.display = caseViewMode === 'kanban' ? '' : 'none';
    $$('[data-case-view]').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-case-view') === caseViewMode);
    });
    if (caseViewMode === 'kanban') {
      renderCasesKanban();
      renderCaseDetail($('#caseDetailKanban'));
    } else {
      renderCasesList();
      renderCaseDetail($('#caseDetail'));
    }
  }

  function renderCasesList() {
    var body = $('#casesBody');
    if (!body) return;
    var list = filteredCases();
    body.innerHTML = list.map(function (c) {
      var on = state.caseId === c.id ? ' on' : '';
      return '<tr class="' + on.trim() + '" data-case="' + c.id + '">' +
        '<td style="font-family:var(--mono);font-size:0.78rem;font-weight:700">' + esc(c.number) + '</td>' +
        '<td><div class="title">' + esc(c.title) + '</div><div class="sub">' + esc(c.shop || '') + ' · ' + esc(c.channel || '') + '</div></td>' +
        '<td><span class="cs-badge type-' + c.type + '">' + esc(CASE_TYPE[c.type] || c.type) + '</span></td>' +
        '<td><span class="cs-badge ' + c.status + '">' + esc(CASE_ST[c.status] || c.status) + '</span></td>' +
        '<td><span class="cs-badge pri-' + c.priority + '">' + esc(CASE_PRI[c.priority] || c.priority) + '</span></td>' +
        '<td class="sub">' + esc(c.clientName || '—') + (c.orderId ? '<br>' + esc(c.orderId) : '') + '</td>' +
        '<td>' + esc(c.assignee || '—') + '</td></tr>';
    }).join('') || '<tr><td colspan="7" style="padding:16px;color:var(--ink-faint)">Нет обращений</td></tr>';
  }

  function renderCasesKanban() {
    var el = $('#casesKanban');
    if (!el) return;
    var list = filteredCases();
    el.innerHTML = CASE_ST_ORDER.map(function (st) {
      var col = list.filter(function (c) { return c.status === st; });
      var cards = col.map(function (c) {
        var on = state.caseId === c.id ? ' on' : '';
        return '<div class="cs-kcard' + on + '" data-case="' + c.id + '">' +
          '<div class="kt">' + esc(c.title) + '</div>' +
          '<div class="km">' +
            '<span class="cs-badge type-' + c.type + '">' + esc(CASE_TYPE[c.type] || '') + '</span>' +
            '<span class="cs-badge pri-' + c.priority + '">' + esc(CASE_PRI[c.priority] || '') + '</span>' +
            '<span>' + esc(c.clientName || '') + '</span>' +
          '</div>' +
          (st !== 'closed'
            ? '<button type="button" class="adv" data-case-advance="' + c.id + '">→ следующий статус</button>'
            : '') +
          '</div>';
      }).join('') || '<div class="cs-empty" style="padding:8px">Пусто</div>';
      return '<div class="cs-kcol">' +
        '<div class="cs-kcol-head st-' + st + '"><span>' + esc(CASE_ST[st]) + '</span><span class="cnt">' + col.length + '</span></div>' +
        '<div class="cs-kcards">' + cards + '</div></div>';
    }).join('');
  }

  function renderCaseDetail(el) {
    if (!el) return;
    var c = cases.filter(function (x) { return x.id === state.caseId; })[0];
    if (!c) {
      el.innerHTML = '<div class="cs-empty">Выберите обращение · Case + Stream (EspoCRM)</div>';
      return;
    }
    var streamHtml = (c.stream || []).slice().reverse().map(function (s) {
      return '<div class="cs-stream-item">' +
        '<div class="cs-stream-ico ' + esc(s.kind || 'note') + '">' + caseStreamIco(s.kind) + '</div>' +
        '<div><div class="cs-stream-head"><span class="cs-stream-who">' + esc(s.who) + '</span>' +
        '<span class="cs-stream-when">' + esc(s.when) + '</span></div>' +
        '<div class="cs-stream-text">' + esc(s.text) + '</div></div></div>';
    }).join('') || '<div class="cs-empty">Лента пуста</div>';

    el.innerHTML =
      '<h3>' + esc(c.title) + '</h3>' +
      '<div class="meta">' + esc(c.number) + ' · ' +
        '<span class="cs-badge type-' + c.type + '">' + esc(CASE_TYPE[c.type] || c.type) + '</span> · ' +
        '<span class="cs-badge ' + c.status + '">' + esc(CASE_ST[c.status] || c.status) + '</span> · ' +
        '<span class="cs-badge pri-' + c.priority + '">' + esc(CASE_PRI[c.priority] || c.priority) + '</span>' +
      '</div>' +
      '<div class="body">' + esc(c.body || '') + '</div>' +
      '<div class="row"><span>Клиент</span><b>' + esc(c.clientName || '—') + '</b></div>' +
      '<div class="row"><span>Заказ</span><b>' + esc(c.orderId || '—') + '</b></div>' +
      '<div class="row"><span>Точка</span><b>' + esc(c.shop || '—') + '</b></div>' +
      '<div class="row"><span>Канал</span><b>' + esc(c.channel || '—') + '</b></div>' +
      '<div class="row"><span>Ответственный</span><b>' + esc(c.assignee || '—') + '</b></div>' +
      '<div class="row"><span>Создано</span><b>' + esc(c.created || '—') + '</b></div>' +
      '<div class="actions">' +
        '<button type="button" class="btn terra" id="btnCaseAdvance">→ статус</button>' +
        '<button type="button" class="btn" id="btnCaseOpenOrder"' + (c.orderId ? '' : ' disabled') + '>Заказ</button>' +
        '<button type="button" class="btn" id="btnCaseOpenClient"' + (c.clientId ? '' : ' disabled') + '>Клиент</button>' +
        '<button type="button" class="btn ghost" id="btnCaseClose">Закрыть</button>' +
      '</div>' +
      '<div class="cs-stream-title">Лента (Stream)</div>' +
      '<div class="cs-stream">' + streamHtml + '</div>' +
      '<div class="cs-compose">' +
        '<textarea id="caseNoteText" placeholder="Заметка в ленту…"></textarea>' +
        '<button type="button" class="btn terra" id="btnCaseNote">Добавить в Stream</button>' +
      '</div>';

    var ba = $('#btnCaseAdvance');
    if (ba) ba.onclick = function () { advanceCase(c.id); };
    var bc = $('#btnCaseClose');
    if (bc) bc.onclick = function () {
      c.status = 'closed';
      c.stream.push({ kind: 'status', who: state.assignee || 'Анна К.', when: 'сейчас', text: 'Статус → Закрыто' });
      renderCases();
      toast('Обращение закрыто');
    };
    var bo = $('#btnCaseOpenOrder');
    if (bo) bo.onclick = function () {
      if (!c.orderId) return;
      switchView('orders');
      if (typeof openOrderDrawer === 'function') openOrderDrawer(c.orderId);
    };
    var bcl = $('#btnCaseOpenClient');
    if (bcl) bcl.onclick = function () {
      if (!c.clientId) return;
      state.clientId = c.clientId;
      switchView('clients');
      if (typeof renderClients === 'function') renderClients();
    };
    var bn = $('#btnCaseNote');
    if (bn) bn.onclick = function () {
      var ta = $('#caseNoteText');
      var t = ta && ta.value.trim();
      if (!t) { toast('Введите текст'); return; }
      c.stream.push({ kind: 'note', who: state.assignee || 'Анна К.', when: 'сейчас', text: t });
      renderCases();
      toast('В ленте');
    };
  }

  function advanceCase(id) {
    var c = cases.filter(function (x) { return x.id === id; })[0];
    if (!c) return;
    var i = CASE_ST_ORDER.indexOf(c.status);
    if (i < 0 || i >= CASE_ST_ORDER.length - 1) {
      toast('Уже закрыто');
      return;
    }
    c.status = CASE_ST_ORDER[i + 1];
    c.stream.push({
      kind: 'status',
      who: state.assignee || 'Анна К.',
      when: 'сейчас',
      text: 'Статус → ' + (CASE_ST[c.status] || c.status)
    });
    if (c.status === 'assigned' && (!c.assignee || c.assignee === '—')) {
      c.assignee = state.assignee || 'Анна К.';
    }
    renderCases();
    toast(CASE_ST[c.status]);
  }

"""

if "function renderCases()" not in text and "function updateCasesBadge" not in text:
    text = text.replace(
        "  /* ────────────────────────── INIT ────────────────────────── */",
        CASES_JS + "\n  /* ────────────────────────── INIT ────────────────────────── */",
    )

# bind events inside bind()
BIND = r"""
    /* Cases (EspoCRM → Обращения) */
    var cs = $('#caseSearch');
    if (cs) cs.addEventListener('input', function () { caseSearchQ = this.value; renderCases(); });
    var csf = $('#caseStatusFilter');
    if (csf) csf.addEventListener('change', function () { caseFilterStatus = this.value; renderCases(); });
    var ctf = $('#caseTypeFilter');
    if (ctf) ctf.addEventListener('change', function () { caseFilterType = this.value; renderCases(); });
    $$('[data-case-view]').forEach(function (b) {
      b.addEventListener('click', function () {
        caseViewMode = b.getAttribute('data-case-view');
        renderCases();
      });
    });
    var bac = $('#btnAddCase');
    if (bac) bac.addEventListener('click', function () {
      var n = cases.length + 100;
      var id = 'CS-' + n;
      cases.unshift({
        id: id, number: id,
        title: 'Новое обращение',
        type: 'question', priority: 'med', status: 'new',
        clientId: null, clientName: '—', orderId: null,
        shop: state.shop === '*' ? 'Мира 14' : state.shop,
        assignee: state.assignee || 'Анна К.',
        channel: 'manual', created: 'сейчас',
        body: 'Опишите жалобу или обратную связь…',
        stream: [{ kind: 'create', who: state.assignee || 'Анна К.', when: 'сейчас', text: 'Создано вручную' }]
      });
      state.caseId = id;
      renderCases();
      toast('Обращение создано');
    });
    document.addEventListener('click', function (e) {
      var row = e.target.closest('[data-case]');
      if (row && !e.target.closest('[data-case-advance]')) {
        state.caseId = row.getAttribute('data-case');
        renderCases();
        return;
      }
      var adv = e.target.closest('[data-case-advance]');
      if (adv) {
        e.stopPropagation();
        advanceCase(adv.getAttribute('data-case-advance'));
      }
    });
"""

# inject after Mail bind block if present, else after function bind() {
if "Cases (EspoCRM" not in text:
    if "/* Mail (Krayin) + Settings nav */" in text:
        # insert before Mail handlers end - better after mail refresh handler
        marker = "    if (mRef) mRef.addEventListener('click', function () { renderMail(); toast('Почта обновлена'); });"
        if marker in text:
            text = text.replace(marker, marker + "\n" + BIND)
        else:
            m = re.search(r"function bind\(\)\s*\{", text)
            if not m:
                raise SystemExit("bind() not found")
            text = text[: m.end()] + "\n" + BIND + text[m.end() :]
    else:
        m = re.search(r"function bind\(\)\s*\{", text)
        if not m:
            raise SystemExit("bind() not found")
        text = text[: m.end()] + "\n" + BIND + text[m.end() :]

# init
if "renderCases();" not in text.split("INIT")[-1] if "INIT" in text else True:
    text = text.replace(
        "  renderMail();\n  updateMailBadge();\n  updateShopBanner();",
        "  renderMail();\n  updateMailBadge();\n  renderCases();\n  updateCasesBadge();\n  updateShopBanner();",
    )

# shop change re-render cases
if "if (state.view === 'settings') renderSettings();" in text and "cases" not in text[text.find("function setShop"):text.find("function setShop")+500]:
    text = text.replace(
        "    if (state.view === 'settings') renderSettings();\n    updateStats();",
        "    if (state.view === 'settings') renderSettings();\n    if (state.view === 'cases') renderCases();\n    updateStats();",
    )

BASE.write_text(text, encoding="utf-8")
print("Wrote", BASE, BASE.stat().st_size)

for c in COPIES:
    c.write_text(text, encoding="utf-8")
    print("Mirrored", c)

# validate braces
s = re.search(r"<script>(.*?)</script>", text, re.S).group(1)
print("braces", s.count("{"), s.count("}"))
assert s.count("{") == s.count("}"), "brace mismatch"
assert "function renderCases" in s
assert 'data-view="cases"' in text
print("OK")
