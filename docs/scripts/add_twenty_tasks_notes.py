# -*- coding: utf-8 -*-
"""Add Twenty-style Tasks + Notes workspace modules to kp/demo/demo.html"""
from pathlib import Path

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
text = BASE.read_text(encoding="utf-8")

CSS = r"""
  /* ═══ Twenty: Tasks + Notes ═══ */
  .tw-toolbar {
    display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px;
  }
  .tw-toolbar input, .tw-toolbar select {
    border: 1px solid var(--border-2); border-radius: 10px; padding: 9px 12px;
    font-family: var(--font); font-size: 0.86rem; background: var(--bg-2); outline: none;
  }
  .tw-toolbar input { flex: 1; min-width: 160px; }
  .tw-toolbar input:focus, .tw-toolbar select:focus { border-color: var(--terra); }
  .tw-layout {
    display: grid; grid-template-columns: 1fr minmax(280px, 340px); gap: 14px; align-items: start;
  }
  .tw-table {
    width: 100%; border-collapse: collapse; background: var(--bg-2);
    border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
    box-shadow: var(--shadow-sm);
  }
  .tw-table th {
    text-align: left; font-size: 0.7rem; font-weight: 700; color: var(--ink-faint);
    text-transform: uppercase; letter-spacing: 0.04em;
    padding: 10px 12px; border-bottom: 1px solid var(--border); background: var(--bg);
  }
  .tw-table td {
    padding: 11px 12px; border-bottom: 1px solid var(--border);
    font-size: 0.86rem; color: var(--ink-dim); vertical-align: middle; cursor: pointer;
  }
  .tw-table tr:last-child td { border-bottom: 0; }
  .tw-table tr:hover td { background: var(--bg-3); }
  .tw-table tr.on td { background: var(--terra-soft); }
  .tw-table .title { font-weight: 800; color: var(--ink); letter-spacing: -0.01em; }
  .tw-table .sub { font-size: 0.72rem; color: var(--ink-mute); margin-top: 2px; }
  .tw-table .done .title { text-decoration: line-through; opacity: 0.65; }
  .tw-badge {
    font-size: 0.65rem; font-weight: 800; padding: 3px 8px; border-radius: 999px;
    background: var(--bg-3); color: var(--ink-mute);
  }
  .tw-badge.todo { background: var(--amber-soft); color: #A07A20; }
  .tw-badge.doing { background: var(--plum-soft); color: var(--plum); }
  .tw-badge.done { background: var(--sage-soft); color: var(--sage); }
  .tw-badge.note { background: var(--terra-soft); color: var(--terra); }
  .tw-detail {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 16px; box-shadow: var(--shadow-sm); position: sticky; top: 72px; min-height: 200px;
  }
  .tw-detail h3 { font-size: 1.02rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 6px; }
  .tw-detail .meta { font-size: 0.78rem; color: var(--ink-mute); margin-bottom: 12px; }
  .tw-detail .body {
    font-size: 0.9rem; color: var(--ink-dim); line-height: 1.5;
    white-space: pre-wrap; background: var(--bg); border-radius: 12px; padding: 12px;
    border: 1px solid var(--border); margin-bottom: 12px; min-height: 80px;
  }
  .tw-detail .row {
    display: flex; justify-content: space-between; gap: 8px; padding: 8px 0;
    border-bottom: 1px solid var(--border); font-size: 0.84rem;
  }
  .tw-detail .row span { color: var(--ink-mute); font-weight: 600; font-size: 0.74rem; }
  .tw-detail .actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
  .tw-empty { color: var(--ink-faint); font-size: 0.86rem; padding: 8px 0; }
  .tw-check {
    width: 18px; height: 18px; border-radius: 6px; border: 2px solid var(--border-2);
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.7rem; color: transparent; flex-shrink: 0; margin-right: 8px; vertical-align: middle;
  }
  .tw-check.on { background: var(--sage); border-color: var(--sage); color: #fff; }
  @media (max-width: 900px) {
    .tw-layout { grid-template-columns: 1fr; }
    .tw-detail { position: static; }
  }
"""

if "/* ═══ Twenty: Tasks + Notes ═══ */" not in text:
    text = text.replace("</style>", CSS + "\n</style>")

# Nav: insert after clients
old_nav = """    <button class="sb-link" data-view="clients"><span class="idx">03</span>Клиенты</button>
    <button class="sb-link" data-view="chats"><span class="idx">04</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">05</span>Номенклатура</button>
    <button class="sb-link" data-view="warehouses"><span class="idx">06</span>Склады</button>
    <button class="sb-link" data-view="invoices"><span class="idx">07</span>Счета</button>
    <button class="sb-link" data-view="analytics"><span class="idx">08</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">09</span>Настройки</button>"""

new_nav = """    <button class="sb-link" data-view="clients"><span class="idx">03</span>Клиенты</button>
    <button class="sb-link" data-view="tasks"><span class="idx">04</span>Задачи</button>
    <button class="sb-link" data-view="notes"><span class="idx">05</span>Заметки</button>
    <button class="sb-link" data-view="chats"><span class="idx">06</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">07</span>Номенклатура</button>
    <button class="sb-link" data-view="warehouses"><span class="idx">08</span>Склады</button>
    <button class="sb-link" data-view="invoices"><span class="idx">09</span>Счета</button>
    <button class="sb-link" data-view="analytics"><span class="idx">10</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">11</span>Настройки</button>"""

if old_nav not in text:
    raise SystemExit("nav block not found")
text = text.replace(old_nav, new_nav)

SECTIONS = r"""
    <!-- ═════════════ TASKS (Twenty) ═════════════ -->
    <section data-section="tasks" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Twenty · Tasks workspace</span>
      </div>
      <div class="tw-toolbar">
        <input type="search" id="taskSearch" placeholder="Поиск задач…" autocomplete="off" />
        <select id="taskStatusFilter">
          <option value="*">Все статусы</option>
          <option value="todo">К выполнению</option>
          <option value="doing">В работе</option>
          <option value="done">Готово</option>
        </select>
        <button type="button" class="btn terra" id="btnAddTask">+ Задача</button>
      </div>
      <div class="tw-layout">
        <div>
          <table class="tw-table">
            <thead>
              <tr><th></th><th>Задача</th><th>Статус</th><th>Связь</th><th>Срок</th><th>Исполнитель</th></tr>
            </thead>
            <tbody id="tasksBody"></tbody>
          </table>
        </div>
        <aside class="tw-detail" id="taskDetail">
          <div class="tw-empty">Выберите задачу · как Tasks в Twenty</div>
        </aside>
      </div>
    </section>

    <!-- ═════════════ NOTES (Twenty) ═════════════ -->
    <section data-section="notes" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Twenty · Notes workspace</span>
      </div>
      <div class="tw-toolbar">
        <input type="search" id="noteSearch" placeholder="Поиск заметок…" autocomplete="off" />
        <button type="button" class="btn terra" id="btnAddNote">+ Заметка</button>
      </div>
      <div class="tw-layout">
        <div>
          <table class="tw-table">
            <thead>
              <tr><th>Заметка</th><th>Связь</th><th>Автор</th><th>Обновлено</th></tr>
            </thead>
            <tbody id="notesBody"></tbody>
          </table>
        </div>
        <aside class="tw-detail" id="noteDetail">
          <div class="tw-empty">Выберите заметку · как Notes в Twenty</div>
        </aside>
      </div>
    </section>

"""

if 'data-section="tasks"' not in text:
    text = text.replace(
        '    <section data-section="clients" style="display:none">',
        SECTIONS + '    <section data-section="clients" style="display:none">',
    )

# VIEW_NAMES
text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', chats: 'Чаты', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', tasks: 'Задачи', notes: 'Заметки', chats: 'Чаты', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
)

text = text.replace(
    """    if (view === 'clients') renderClients();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
    """    if (view === 'clients') renderClients();
    if (view === 'tasks') renderTasks();
    if (view === 'notes') renderNotes();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
)

# seed data after clients
DATA = r"""
  var tasksSeed = [
    { id: 't1', title: 'Согласовать фото букета с клиентом', status: 'todo', due: 'сегодня 14:00', assignee: 'Анна К.', relType: 'order', relId: 'FW-1042', relLabel: 'FW-1042', body: 'Марина ждёт фото до выезда курьера.' },
    { id: 't2', title: 'Проверить остаток пионов на Мира 14', status: 'doing', due: 'сегодня 16:00', assignee: 'Света П.', relType: 'sku', relId: 'sku-1', relLabel: 'BLM-PN-15', body: 'Сверить Bloom-склад с указателем на сайте.' },
    { id: 't3', title: 'Ответить в Telegram — доставка на Строителей', status: 'todo', due: 'сегодня 12:30', assignee: 'Анна К.', relType: 'chat', relId: 'tg', relLabel: 'Алексей · TG', body: 'Клиент спросил про офис.' },
    { id: 't4', title: 'Выставить счёт INV по герберам', status: 'todo', due: 'завтра', assignee: 'Анна К.', relType: 'order', relId: 'FW-1038', relLabel: 'FW-1038', body: 'Dolibarr-цепочка: заказ → счёт.' },
    { id: 't5', title: 'Обучение смены: статусы канбана', status: 'done', due: 'вчера', assignee: 'Игорь М.', relType: 'shop', relId: 'Ленина 92', relLabel: 'Ленина 92', body: 'Провели разбор 12 недель.' }
  ];
  var notesSeed = [
    { id: 'n1', title: 'VIP-клиенты к 8 Марта', body: 'Марина К. и ещё 4 постоянных — держать слоты доставки до 12:00.\nНе предлагать замены без фото.', author: 'Анна К.', relType: 'client', relId: 'c1', relLabel: 'Марина К.', updated: 'сегодня 09:40' },
    { id: 'n2', title: 'API остатков сайта', body: 'Поле siteStock в номенклатуре — временный mock.\nНужен endpoint витрины: GET /stock?sku=\nРасхождения подсвечивать красным.', author: 'Анна К.', relType: 'sku', relId: 'sku-1', relLabel: 'Номенклатура', updated: 'вчера' },
    { id: 'n3', title: 'Хаб-склад', body: 'Перемещения с хаба на точки — по утрам.\nНе отпускать заказ в доставку при stock=0 на точке.', author: 'Игорь М.', relType: 'shop', relId: 'wh-hub', relLabel: 'Хаб', updated: '2 дня назад' },
    { id: 'n4', title: 'Шаблоны ответов WA', body: '«Фото до отправки» и «Счёт ссылкой» — самые частые canned.\nДобавить шаблон самовывоза.', author: 'Анна К.', relType: 'chat', relId: 'wa', relLabel: 'Inbox', updated: 'сегодня 11:05' }
  ];
  var tasks = JSON.parse(JSON.stringify(tasksSeed));
  var notes = JSON.parse(JSON.stringify(notesSeed));
  var taskFilter = '*';
  var taskSearch = '';
  var noteSearch = '';
"""

if "var tasksSeed" not in text:
    text = text.replace(
        "  var clients = JSON.parse(JSON.stringify(clientsSeed));",
        "  var clients = JSON.parse(JSON.stringify(clientsSeed));\n" + DATA,
    )

# state fields
text = text.replace(
    """    shop: '*',
    clientId: null
  };""",
    """    shop: '*',
    clientId: null,
    taskId: null,
    noteId: null
  };""",
)

TASKS_JS = r"""
  /* ────────────────────────── TASKS + NOTES (Twenty) ────────────────────────── */
  var TASK_ST = { todo: 'К выполнению', doing: 'В работе', done: 'Готово' };

  function filteredTasks() {
    var q = (taskSearch || '').toLowerCase();
    return tasks.filter(function (t) {
      if (taskFilter !== '*' && t.status !== taskFilter) return false;
      // soft shop scope: show all network tasks always; filter by shop relation if shop selected
      if (state.shop !== '*' && t.relType === 'shop' && t.relId !== state.shop) return false;
      if (state.shop !== '*' && t.relType === 'order') {
        var o = state.orders.filter(function (x) { return x.id === t.relId; })[0];
        if (o && o.shop !== state.shop) return false;
      }
      if (q && (t.title + ' ' + (t.body || '') + ' ' + (t.relLabel || '') + ' ' + (t.assignee || '')).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
  }

  function renderTasks() {
    var body = $('#tasksBody');
    if (!body) return;
    var list = filteredTasks();
    body.innerHTML = list.map(function (t) {
      var on = state.taskId === t.id ? ' on' : '';
      var doneCls = t.status === 'done' ? ' done' : '';
      return '<tr class="' + on.trim() + doneCls + '" data-task="' + t.id + '">' +
        '<td><span class="tw-check' + (t.status === 'done' ? ' on' : '') + '" data-task-toggle="' + t.id + '">✓</span></td>' +
        '<td><div class="title">' + esc(t.title) + '</div><div class="sub">' + esc((t.body || '').slice(0, 60)) + ((t.body || '').length > 60 ? '…' : '') + '</div></td>' +
        '<td><span class="tw-badge ' + t.status + '">' + (TASK_ST[t.status] || t.status) + '</span></td>' +
        '<td class="sub">' + esc(t.relLabel || '—') + '</td>' +
        '<td>' + esc(t.due || '—') + '</td>' +
        '<td>' + esc(t.assignee || '—') + '</td></tr>';
    }).join('') || '<tr><td colspan="6" style="padding:16px;color:var(--ink-faint)">Нет задач</td></tr>';
    renderTaskDetail();
  }

  function renderTaskDetail() {
    var el = $('#taskDetail');
    if (!el) return;
    var t = tasks.filter(function (x) { return x.id === state.taskId; })[0];
    if (!t) {
      el.innerHTML = '<div class="tw-empty">Выберите задачу · workspace Tasks (Twenty)</div>';
      return;
    }
    el.innerHTML =
      '<h3>' + esc(t.title) + '</h3>' +
      '<div class="meta">' + (TASK_ST[t.status] || t.status) + ' · ' + esc(t.due || 'без срока') + ' · ' + esc(t.assignee || '—') + '</div>' +
      '<div class="body">' + esc(t.body || '') + '</div>' +
      '<div class="row"><span>Связь</span><b>' + esc(t.relLabel || '—') + ' (' + esc(t.relType || '') + ')</b></div>' +
      '<div class="row"><span>ID</span><b style="font-family:var(--mono);font-size:0.78rem">' + esc(t.id) + '</b></div>' +
      '<div class="actions">' +
        '<button type="button" class="btn terra" id="btnTaskCycle">Сменить статус</button>' +
        '<button type="button" class="btn" id="btnTaskOpenRel">Открыть связь</button>' +
        '<button type="button" class="btn" id="btnTaskDone">Готово</button>' +
      '</div>';
    var bc = $('#btnTaskCycle');
    if (bc) bc.onclick = function () {
      var order = ['todo', 'doing', 'done'];
      var i = order.indexOf(t.status);
      t.status = order[(i + 1) % order.length];
      renderTasks();
      toast(TASK_ST[t.status]);
    };
    var bd = $('#btnTaskDone');
    if (bd) bd.onclick = function () { t.status = 'done'; renderTasks(); toast('Задача выполнена'); };
    var br = $('#btnTaskOpenRel');
    if (br) br.onclick = function () { openTaskRel(t); };
  }

  function openTaskRel(t) {
    if (t.relType === 'order' && t.relId) { switchView('orders'); openOrderDrawer(t.relId); }
    else if (t.relType === 'chat' && t.relId) { switchView('chats'); selectChat(t.relId); }
    else if (t.relType === 'sku') switchView('vitrina');
    else if (t.relType === 'shop') { setShop(t.relId); switchView('orders'); }
    else toast('Связь: ' + (t.relLabel || '—'));
  }

  function filteredNotes() {
    var q = (noteSearch || '').toLowerCase();
    return notes.filter(function (n) {
      if (q && (n.title + ' ' + n.body + ' ' + (n.relLabel || '') + ' ' + (n.author || '')).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
  }

  function renderNotes() {
    var body = $('#notesBody');
    if (!body) return;
    var list = filteredNotes();
    body.innerHTML = list.map(function (n) {
      var on = state.noteId === n.id ? ' on' : '';
      return '<tr class="' + on.trim() + '" data-note="' + n.id + '">' +
        '<td><div class="title">' + esc(n.title) + '</div><div class="sub">' + esc((n.body || '').replace(/\n/g, ' ').slice(0, 70)) + '…</div></td>' +
        '<td><span class="tw-badge note">' + esc(n.relLabel || '—') + '</span></td>' +
        '<td>' + esc(n.author || '—') + '</td>' +
        '<td class="sub">' + esc(n.updated || '') + '</td></tr>';
    }).join('') || '<tr><td colspan="4" style="padding:16px;color:var(--ink-faint)">Нет заметок</td></tr>';
    renderNoteDetail();
  }

  function renderNoteDetail() {
    var el = $('#noteDetail');
    if (!el) return;
    var n = notes.filter(function (x) { return x.id === state.noteId; })[0];
    if (!n) {
      el.innerHTML = '<div class="tw-empty">Выберите заметку · workspace Notes (Twenty)</div>';
      return;
    }
    el.innerHTML =
      '<h3>' + esc(n.title) + '</h3>' +
      '<div class="meta">' + esc(n.author || '') + ' · ' + esc(n.updated || '') + '</div>' +
      '<div class="body">' + esc(n.body || '') + '</div>' +
      '<div class="row"><span>Связь</span><b>' + esc(n.relLabel || '—') + '</b></div>' +
      '<div class="actions">' +
        '<button type="button" class="btn terra" id="btnNoteOpenRel">Открыть связь</button>' +
        '<button type="button" class="btn" id="btnNoteToTask">→ в задачу</button>' +
      '</div>';
    var br = $('#btnNoteOpenRel');
    if (br) br.onclick = function () {
      openTaskRel({ relType: n.relType, relId: n.relId, relLabel: n.relLabel });
    };
    var bt = $('#btnNoteToTask');
    if (bt) bt.onclick = function () {
      var id = 't' + (tasks.length + 1);
      tasks.unshift({
        id: id, title: n.title, status: 'todo', due: 'сегодня', assignee: state.assignee,
        relType: n.relType, relId: n.relId, relLabel: n.relLabel, body: n.body
      });
      state.taskId = id;
      switchView('tasks');
      toast('Задача создана из заметки');
    };
  }

"""

if "TASKS + NOTES (Twenty)" not in text:
    text = text.replace(
        "  /* ────────────────────────── INIT ────────────────────────── */",
        TASKS_JS + "\n  /* ────────────────────────── INIT ────────────────────────── */",
    )

text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', chats: 'Чаты', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', tasks: 'Задачи', notes: 'Заметки', chats: 'Чаты', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
)

# fix if already partially updated VIEW_NAMES
if "tasks: 'Задачи'" not in text:
    text = text.replace(
        "clients: 'Клиенты', chats: 'Чаты'",
        "clients: 'Клиенты', tasks: 'Задачи', notes: 'Заметки', chats: 'Чаты'",
    )

text = text.replace(
    """    if (view === 'clients') renderClients();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
    """    if (view === 'clients') renderClients();
    if (view === 'tasks') renderTasks();
    if (view === 'notes') renderNotes();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();""",
)

# bind
BIND = r"""
    var ts = $('#taskSearch');
    if (ts) ts.addEventListener('input', function () { taskSearch = this.value; renderTasks(); });
    var tf = $('#taskStatusFilter');
    if (tf) tf.addEventListener('change', function () { taskFilter = this.value; renderTasks(); });
    var bat = $('#btnAddTask');
    if (bat) bat.addEventListener('click', function () {
      var id = 't' + (tasks.length + 1);
      tasks.unshift({
        id: id, title: 'Новая задача', status: 'todo', due: 'сегодня', assignee: state.assignee,
        relType: 'shop', relId: state.shop === '*' ? 'Мира 14' : state.shop,
        relLabel: state.shop === '*' ? 'Сеть' : state.shop,
        body: 'Описание задачи…'
      });
      state.taskId = id;
      renderTasks();
      toast('Задача создана');
    });
    var tb = $('#tasksBody');
    if (tb) tb.addEventListener('click', function (e) {
      var tog = e.target.closest('[data-task-toggle]');
      if (tog) {
        e.stopPropagation();
        var tid = tog.getAttribute('data-task-toggle');
        var t = tasks.filter(function (x) { return x.id === tid; })[0];
        if (t) { t.status = t.status === 'done' ? 'todo' : 'done'; renderTasks(); }
        return;
      }
      var tr = e.target.closest('[data-task]');
      if (tr) { state.taskId = tr.getAttribute('data-task'); renderTasks(); }
    });

    var ns = $('#noteSearch');
    if (ns) ns.addEventListener('input', function () { noteSearch = this.value; renderNotes(); });
    var ban = $('#btnAddNote');
    if (ban) ban.addEventListener('click', function () {
      var id = 'n' + (notes.length + 1);
      notes.unshift({
        id: id, title: 'Новая заметка', body: 'Текст заметки…', author: state.assignee,
        relType: 'shop', relId: state.shop, relLabel: state.shop === '*' ? 'Сеть' : state.shop,
        updated: 'только что'
      });
      state.noteId = id;
      renderNotes();
      toast('Заметка создана');
    });
    var nb = $('#notesBody');
    if (nb) nb.addEventListener('click', function (e) {
      var tr = e.target.closest('[data-note]');
      if (tr) { state.noteId = tr.getAttribute('data-note'); renderNotes(); }
    });

"""

marker = "    var sw = $('#shopSwitcher');"
if "btnAddTask" not in text and marker in text:
    text = text.replace(marker, BIND + marker)

# cmdk
text = text.replace(
    """    shopFilter(clients).forEach(function (c) {
      items.push({ t: 'Клиент · ' + c.name, k: 'client', v: c.id });
    });""",
    """    shopFilter(clients).forEach(function (c) {
      items.push({ t: 'Клиент · ' + c.name, k: 'client', v: c.id });
    });
    tasks.forEach(function (t) {
      items.push({ t: 'Задача · ' + t.title, k: 'task', v: t.id });
    });
    notes.forEach(function (n) {
      items.push({ t: 'Заметка · ' + n.title, k: 'note', v: n.id });
    });""",
)

text = text.replace(
    """    else if (k === 'client') { state.clientId = v; switchView('clients'); }
  }""",
    """    else if (k === 'client') { state.clientId = v; switchView('clients'); }
    else if (k === 'task') { state.taskId = v; switchView('tasks'); }
    else if (k === 'note') { state.noteId = v; switchView('notes'); }
  }""",
)

text = text.replace(
    """  renderClients();
  setOrdersView('list');
  bind();
  startSim();
})();""",
    """  renderClients();
  renderTasks();
  renderNotes();
  setOrdersView('list');
  bind();
  startSim();
})();""",
)

# chip
text = text.replace(
    '<span class="chip">Twenty · клиенты + ⌘K</span>',
    '<span class="chip">Twenty · клиенты + задачи + заметки + ⌘K</span>',
)

BASE.write_text(text, encoding="utf-8")
for c in COPIES:
    c.write_text(text, encoding="utf-8")
print("OK", BASE.stat().st_size)
assert 'data-section="tasks"' in text and 'data-section="notes"' in text
assert "renderTasks" in text and "renderNotes" in text
print("asserts ok")
