# -*- coding: utf-8 -*-
"""Add ERPNext-style order list view + richer nomenclature to kp/demo/demo.html"""
from pathlib import Path

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
text = BASE.read_text(encoding="utf-8")

CSS = r"""
  /* ═══ ERPNext: order list + nomenclature ═══ */
  .view-toggle {
    display: inline-flex; gap: 4px; background: var(--bg-3);
    padding: 4px; border-radius: 10px; border: 1px solid var(--border);
  }
  .view-toggle button {
    border: 0; background: transparent; cursor: pointer; font-family: var(--font);
    font-size: 0.78rem; font-weight: 700; color: var(--ink-mute);
    padding: 7px 12px; border-radius: 8px;
  }
  .view-toggle button.on {
    background: var(--bg-2); color: var(--ink); box-shadow: var(--shadow-sm);
  }
  .orders-toolbar {
    display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
    margin-bottom: 12px;
  }
  .orders-toolbar .grow { flex: 1; min-width: 160px; }
  .orders-toolbar input, .orders-toolbar select {
    border: 1px solid var(--border-2); border-radius: 10px; padding: 9px 12px;
    font-family: var(--font); font-size: 0.86rem; background: var(--bg-2); outline: none;
  }
  .orders-toolbar input:focus, .orders-toolbar select:focus { border-color: var(--terra); }
  .so-list {
    width: 100%; border-collapse: collapse; background: var(--bg-2);
    border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
    box-shadow: var(--shadow-sm);
  }
  .so-list th {
    text-align: left; font-size: 0.7rem; font-weight: 700; color: var(--ink-faint);
    text-transform: uppercase; letter-spacing: 0.04em;
    padding: 10px 12px; border-bottom: 1px solid var(--border); background: var(--bg);
  }
  .so-list td {
    padding: 11px 12px; border-bottom: 1px solid var(--border);
    font-size: 0.86rem; color: var(--ink-dim); vertical-align: middle;
  }
  .so-list tr:last-child td { border-bottom: 0; }
  .so-list tr { cursor: pointer; }
  .so-list tr:hover td { background: var(--bg-3); }
  .so-list tr.is-new td { background: var(--terra-soft); }
  .so-list .id { font-weight: 800; color: var(--ink); font-family: var(--mono); font-size: 0.78rem; }
  .so-list .item { font-weight: 700; color: var(--ink); }
  .so-list .meta { font-size: 0.72rem; color: var(--ink-mute); }
  .so-list .price { font-weight: 800; color: var(--terra); white-space: nowrap; }
  .so-axes { display: flex; flex-wrap: wrap; gap: 4px; }
  .axis {
    font-size: 0.68rem; font-weight: 700; padding: 3px 8px; border-radius: 999px;
    background: var(--bg-3); color: var(--ink-mute);
  }
  .axis.ff-new { background: var(--terra-soft); color: var(--terra); }
  .axis.ff-accepted, .axis.ff-assembled { background: var(--plum-soft); color: var(--plum); }
  .axis.ff-delivering { background: var(--amber-soft); color: #A07A20; }
  .axis.ff-done { background: var(--sage-soft); color: var(--sage); }
  .axis.pay-paid { background: var(--sage-soft); color: var(--sage); }
  .axis.pay-pending { background: var(--amber-soft); color: #A07A20; }
  .axis.pay-cod { background: var(--plum-soft); color: var(--plum); }
  .axis.ch-fw { background: var(--terra-soft); color: var(--terra); }
  .axis.ch-wa { background: var(--sage-soft); color: var(--sage); }
  .axis.ch-tg { background: var(--plum-soft); color: var(--plum); }
  .axis.ch-max { background: var(--amber-soft); color: #A07A20; }
  #ordersKanbanWrap, #ordersListWrap { display: none; }
  #ordersKanbanWrap.on, #ordersListWrap.on { display: block; }

  .nom-head {
    display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 12px;
  }
  .nom-head input, .nom-head select {
    border: 1px solid var(--border-2); border-radius: 10px; padding: 9px 12px;
    font-family: var(--font); font-size: 0.86rem; background: var(--bg-2);
  }
  .nom-table {
    width: 100%; border-collapse: collapse; background: var(--bg-2);
    border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
    box-shadow: var(--shadow-sm); margin-bottom: 16px;
  }
  .nom-table th {
    text-align: left; font-size: 0.7rem; font-weight: 700; color: var(--ink-faint);
    text-transform: uppercase; letter-spacing: 0.04em;
    padding: 10px 12px; border-bottom: 1px solid var(--border); background: var(--bg);
  }
  .nom-table td {
    padding: 11px 12px; border-bottom: 1px solid var(--border);
    font-size: 0.86rem; color: var(--ink-dim); vertical-align: middle;
  }
  .nom-table tr:last-child td { border-bottom: 0; }
  .nom-table tr.hidden-row { opacity: 0.5; }
  .nom-table .sku { font-family: var(--mono); font-size: 0.74rem; font-weight: 700; color: var(--ink-mute); }
  .nom-table .nm { font-weight: 800; color: var(--ink); }
  .nom-table .stock-bar {
    height: 6px; border-radius: 99px; background: var(--bg-3); overflow: hidden; width: 72px; display: inline-block; vertical-align: middle; margin-right: 8px;
  }
  .nom-table .stock-bar i { display: block; height: 100%; background: var(--sage); border-radius: 99px; }
  .nom-table .stock-bar.low i { background: var(--terra); }
  .nom-table .stock-bar.out i { background: var(--red); width: 100% !important; opacity: 0.35; }
  .nom-api-note {
    font-size: 0.8rem; color: var(--ink-mute); line-height: 1.45;
    background: var(--bg); border: 1px dashed var(--border-2); border-radius: 12px;
    padding: 12px 14px; margin-bottom: 14px;
  }
  .nom-api-note b { color: var(--ink); }
  .nom-actions button {
    border: 1px solid var(--border-2); background: var(--bg); border-radius: 8px;
    padding: 5px 9px; cursor: pointer; font-family: var(--font); font-size: 0.74rem; font-weight: 700;
    margin-right: 4px;
  }
  .nom-actions button:hover { border-color: var(--terra); color: var(--terra); }
"""

if "/* ═══ ERPNext: order list + nomenclature ═══ */" not in text:
    text = text.replace("</style>", CSS + "\n</style>")

# Rename Витрина → Номенклатура in nav
text = text.replace(
    '<button class="sb-link" data-view="vitrina"><span class="idx">05</span>Витрина</button>',
    '<button class="sb-link" data-view="vitrina"><span class="idx">05</span>Номенклатура</button>',
)
text = text.replace(
    "vitrina: 'Витрина'",
    "vitrina: 'Номенклатура'",
)

# Orders section HTML replace
old_orders = """    <section data-section="orders" style="display:none">
      <div class="live-bar" id="ordersLive">
        <span class="live-dot" aria-hidden="true"></span>
        <span>Живая имитация · <b>новые заказы и смена статусов</b></span>
        <span class="live-event" id="liveEvent"></span>
      </div>
      <div class="kanban" id="kanban2">"""

new_orders = """    <section data-section="orders" style="display:none">
      <div class="live-bar" id="ordersLive">
        <span class="live-dot" aria-hidden="true"></span>
        <span>Живая имитация · <b>новые заказы и смена статусов</b></span>
        <span class="live-event" id="liveEvent"></span>
      </div>
      <div class="orders-toolbar">
        <div class="view-toggle" id="ordersViewToggle">
          <button type="button" data-oview="kanban">Канбан</button>
          <button type="button" class="on" data-oview="list">Список · ERPNext</button>
        </div>
        <input type="search" id="ordersSearch" class="grow" placeholder="№ заказа, товар, точка…" autocomplete="off" />
        <select id="ordersStatusFilter">
          <option value="*">Все статусы</option>
          <option value="new">Новый</option>
          <option value="accepted">Принят</option>
          <option value="assembled">Собран</option>
          <option value="delivering">В доставке</option>
          <option value="done">Доставлен</option>
        </select>
      </div>
      <div id="ordersListWrap" class="on">
        <table class="so-list">
          <thead>
            <tr>
              <th>№</th>
              <th>Товар / клиентский заказ</th>
              <th>Точка</th>
              <th>Оси статуса (ERPNext-style)</th>
              <th>Сумма</th>
            </tr>
          </thead>
          <tbody id="ordersListBody"></tbody>
        </table>
      </div>
      <div id="ordersKanbanWrap">
      <div class="kanban" id="kanban2">"""

if old_orders not in text:
    raise SystemExit("orders block start not found")
text = text.replace(old_orders, new_orders)

# close kanban wrap after kanban ends
old_kanban_end = """        <div class="kb-col" data-status="done">
          <div class="kb-head">Доставлен <span class="n">05</span></div>
          <div class="kb-body"></div>
        </div>
      </div>
    </section>

    <!-- ═════════════ 03 · CHATS"""

# Note: chats might be 04 now - check
if old_kanban_end not in text:
    old_kanban_end = """        <div class="kb-col" data-status="done">
          <div class="kb-head">Доставлен <span class="n">05</span></div>
          <div class="kb-body"></div>
        </div>
      </div>
    </section>

    <!-- ═════════════ CLIENTS"""
    new_kanban_end = """        <div class="kb-col" data-status="done">
          <div class="kb-head">Доставлен <span class="n">05</span></div>
          <div class="kb-body"></div>
        </div>
      </div>
      </div>
    </section>

    <!-- ═════════════ CLIENTS"""
    if old_kanban_end not in text:
        # try chats comment
        import re
        m = re.search(
            r'(        <div class="kb-col" data-status="done">.*?</div>\n      </div>\n)(    </section>)',
            text,
            re.S,
        )
        if not m:
            raise SystemExit("kanban end not found")
        text = text[: m.start()] + m.group(1) + "      </div>\n" + m.group(2) + text[m.end() :]
    else:
        text = text.replace(old_kanban_end, new_kanban_end)
else:
    text = text.replace(
        old_kanban_end,
        """        <div class="kb-col" data-status="done">
          <div class="kb-head">Доставлен <span class="n">05</span></div>
          <div class="kb-body"></div>
        </div>
      </div>
      </div>
    </section>

    <!-- ═════════════ 03 · CHATS""",
    )

# Vitrina section enhance
old_vit = """    <section data-section="vitrina" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Dolibarr · остатки / цены / hide</span>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap">
        <button type="button" class="btn" id="vitFilterAll">Все</button>
        <button type="button" class="btn" id="vitFilterLow">Мало на складе</button>
        <button type="button" class="btn" id="vitFilterHidden">Скрытые</button>
      </div>
      <div class="vit-grid" id="vitGrid"></div>
    </section>"""

new_vit = """    <section data-section="vitrina" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">ERPNext · Item / Stock</span>
        <span class="chip">Dolibarr · остатки</span>
        <span class="chip sage">API сайта · указатель остатков (план)</span>
      </div>
      <div class="nom-api-note">
        <b>Номенклатура</b> — справочник SKU как в ERPNext Item.
        Поля <b>stock</b> / <b>siteStock</b> заготовлены под синхронизацию с API витрины сайта
        (указатель остатков на их сайте). Сейчас — mock; кнопки ± имитируют локальный склад Bloom.
      </div>
      <div class="nom-head">
        <input type="search" id="nomSearch" placeholder="Код, название…" autocomplete="off" style="flex:1;min-width:180px" />
        <select id="nomGroup">
          <option value="*">Все группы</option>
          <option value="Букеты">Букеты</option>
          <option value="Композиции">Композиции</option>
          <option value="Горшечные">Горшечные</option>
          <option value="Подарки">Подарки</option>
        </select>
        <button type="button" class="btn" id="vitFilterAll">Все</button>
        <button type="button" class="btn" id="vitFilterLow">Мало</button>
        <button type="button" class="btn" id="vitFilterHidden">Скрытые</button>
        <div class="view-toggle" id="nomViewToggle">
          <button type="button" class="on" data-nview="table">Список</button>
          <button type="button" data-nview="cards">Карточки</button>
        </div>
      </div>
      <div id="nomTableWrap" class="on">
        <table class="nom-table">
          <thead>
            <tr>
              <th>Код</th>
              <th>Наименование</th>
              <th>Группа</th>
              <th>Склад Bloom</th>
              <th>На сайте (API)</th>
              <th>Цена</th>
              <th></th>
            </tr>
          </thead>
          <tbody id="nomTableBody"></tbody>
        </table>
      </div>
      <div class="vit-grid" id="vitGrid" style="display:none"></div>
    </section>"""

if old_vit not in text:
    raise SystemExit("vitrina section not found")
text = text.replace(old_vit, new_vit)

# products data enrich
old_prod = """  var products = [
    { id: 'sku-1', name: 'Букет пионов, 15 шт.', price: 3200, stock: 12, hidden: false },
    { id: 'sku-2', name: 'Сборный · роза + эустома', price: 2450, stock: 4, hidden: false },
    { id: 'sku-3', name: 'Композиция «Нежность»', price: 4100, stock: 2, hidden: false },
    { id: 'sku-4', name: 'Корзина «Счастье»', price: 7600, stock: 1, hidden: false },
    { id: 'sku-5', name: 'Тюльпаны, 21 шт.', price: 1990, stock: 28, hidden: false },
    { id: 'sku-6', name: 'Орхидея в кашпо', price: 5300, stock: 0, hidden: true }
  ];
  var vitFilter = 'all';"""

new_prod = """  var products = [
    { id: 'sku-1', code: 'BLM-PN-15', name: 'Букет пионов, 15 шт.', group: 'Букеты', price: 3200, stock: 12, siteStock: 11, hidden: false },
    { id: 'sku-2', code: 'BLM-MIX-01', name: 'Сборный · роза + эустома', group: 'Букеты', price: 2450, stock: 4, siteStock: 4, hidden: false },
    { id: 'sku-3', code: 'BLM-CMP-N', name: 'Композиция «Нежность»', group: 'Композиции', price: 4100, stock: 2, siteStock: 2, hidden: false },
    { id: 'sku-4', code: 'BLM-BASK-S', name: 'Корзина «Счастье»', group: 'Композиции', price: 7600, stock: 1, siteStock: 0, hidden: false },
    { id: 'sku-5', code: 'BLM-TUL-21', name: 'Тюльпаны, 21 шт.', group: 'Букеты', price: 1990, stock: 28, siteStock: 30, hidden: false },
    { id: 'sku-6', code: 'BLM-ORC-01', name: 'Орхидея в кашпо', group: 'Горшечные', price: 5300, stock: 0, siteStock: 0, hidden: true },
    { id: 'sku-7', code: 'BLM-GFT-40', name: 'Медвежонок 40 см', group: 'Подарки', price: 1500, stock: 9, siteStock: 9, hidden: false },
    { id: 'sku-8', code: 'BLM-ROS-25', name: 'Розы, 25 шт.', group: 'Букеты', price: 3800, stock: 6, siteStock: 5, hidden: false }
  ];
  var vitFilter = 'all';
  var ordersView = 'list';
  var nomView = 'table';
  var ordersSearch = '';
  var ordersStatusFilter = '*';
  var nomSearch = '';
  var nomGroup = '*';"""

if old_prod not in text:
    raise SystemExit("products block not found")
text = text.replace(old_prod, new_prod)

# renderAllKanban also list
text = text.replace(
    """  function renderAllKanban() {
    if (kanban1) renderKanban(kanban1);
    if (kanban2) renderKanban(kanban2);
    updateStats();
    $$('.stat').forEach(function (s) {
      s.classList.remove('tick');
      void s.offsetWidth;
      s.classList.add('tick');
    });
  }""",
    """  function renderAllKanban() {
    if (kanban1) renderKanban(kanban1);
    if (kanban2) renderKanban(kanban2);
    renderOrdersList();
    updateStats();
    $$('.stat').forEach(function (s) {
      s.classList.remove('tick');
      void s.offsetWidth;
      s.classList.add('tick');
    });
  }

  function fulfillmentAxis(st) {
    return NAMES[st] || st;
  }

  function renderOrdersList() {
    var body = $('#ordersListBody');
    if (!body) return;
    var q = (ordersSearch || '').toLowerCase();
    var list = shopFilter(state.orders).filter(function (o) {
      if (ordersStatusFilter !== '*' && o.status !== ordersStatusFilter) return false;
      if (!q) return true;
      return (o.id + ' ' + o.name + ' ' + o.shop + ' ' + (CH_NAMES[o.channel] || '')).toLowerCase().indexOf(q) >= 0;
    });
    body.innerHTML = list.map(function (o) {
      var pay = o.pay || (o.channel === 'fw' ? 'paid' : 'pending');
      var anim = state.animIds[o.id] || '';
      return '<tr class="' + anim + '" data-id="' + o.id + '">' +
        '<td class="id">' + esc(o.id) + '</td>' +
        '<td><div class="item">' + esc(o.name) + '</div><div class="meta">' + esc(CH_NAMES[o.channel] || o.channel) + '</div></td>' +
        '<td>' + esc(o.shop) + '</td>' +
        '<td><div class="so-axes">' +
          '<span class="axis ff-' + o.status + '" title="Fulfillment">⚙ ' + fulfillmentAxis(o.status) + '</span>' +
          '<span class="axis pay-' + pay + '" title="Payment">₽ ' + (PAY_NAMES[pay] || pay) + '</span>' +
          '<span class="axis ch-' + o.channel + '">' + (CH_NAMES[o.channel] || o.channel) + '</span>' +
        '</div></td>' +
        '<td class="price">' + fmtPrice(o.price) + '</td></tr>';
    }).join('') || '<tr><td colspan="5" style="padding:16px;color:var(--ink-faint)">Нет заказов</td></tr>';
  }

  function setOrdersView(mode) {
    ordersView = mode || 'list';
    var kw = $('#ordersKanbanWrap');
    var lw = $('#ordersListWrap');
    if (kw) kw.classList.toggle('on', ordersView === 'kanban');
    if (lw) lw.classList.toggle('on', ordersView === 'list');
    $$('#ordersViewToggle button').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-oview') === ordersView);
    });
    if (ordersView === 'list') renderOrdersList();
    else renderAllKanban();
  }""",
)

# replace renderVitrina fully
old_rv = """  function renderVitrina() {
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
  }"""

new_rv = """  function filteredProducts() {
    var q = (nomSearch || '').toLowerCase();
    return products.filter(function (p) {
      if (vitFilter === 'low') { if (!(p.stock > 0 && p.stock <= 3)) return false; }
      if (vitFilter === 'hidden') { if (!p.hidden) return false; }
      if (nomGroup !== '*' && p.group !== nomGroup) return false;
      if (q && (p.code + ' ' + p.name + ' ' + (p.group || '')).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
  }

  function stockBar(p) {
    var max = 30;
    var pct = p.stock <= 0 ? 100 : Math.min(100, Math.round(p.stock / max * 100));
    var cls = p.stock <= 0 ? 'out' : (p.stock <= 3 ? 'low' : '');
    return '<span class="stock-bar ' + cls + '"><i style="width:' + pct + '%"></i></span><b>' + p.stock + '</b>';
  }

  function renderVitrina() {
    var list = filteredProducts();
    var tbody = $('#nomTableBody');
    var grid = $('#vitGrid');
    var tw = $('#nomTableWrap');
    if (tw) tw.style.display = nomView === 'table' ? 'block' : 'none';
    if (grid) grid.style.display = nomView === 'cards' ? 'grid' : 'none';
    $$('#nomViewToggle button').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-nview') === nomView);
    });

    if (tbody && nomView === 'table') {
      tbody.innerHTML = list.map(function (p) {
        var site = (p.siteStock != null ? p.siteStock : '—');
        var sync = (p.siteStock != null && p.siteStock !== p.stock)
          ? '<span class="meta" style="color:var(--terra)">расхождение</span>'
          : '<span class="meta">ok</span>';
        return '<tr class="' + (p.hidden ? 'hidden-row' : '') + '">' +
          '<td class="sku">' + esc(p.code || p.id) + '</td>' +
          '<td class="nm">' + esc(p.name) + (p.hidden ? ' <span class="meta">· скрыт</span>' : '') + '</td>' +
          '<td>' + esc(p.group || '—') + '</td>' +
          '<td>' + stockBar(p) + '</td>' +
          '<td><b>' + site + '</b> ' + sync + '</td>' +
          '<td><b>' + fmtPrice(p.price) + '</b></td>' +
          '<td class="nom-actions">' +
            '<button type="button" data-vit="minus" data-id="' + p.id + '">−</button>' +
            '<button type="button" data-vit="plus" data-id="' + p.id + '">+</button>' +
            '<button type="button" data-vit="sync" data-id="' + p.id + '" title="Подтянуть с сайта">API</button>' +
            '<button type="button" data-vit="hide" data-id="' + p.id + '">' + (p.hidden ? 'показать' : 'скрыть') + '</button>' +
          '</td></tr>';
      }).join('') || '<tr><td colspan="7" style="padding:16px;color:var(--ink-faint)">Нет позиций</td></tr>';
    }

    if (grid && nomView === 'cards') {
      grid.innerHTML = list.map(function (p) {
        return '<div class="vit-card' + (p.hidden ? ' hidden-sku' : '') + '" data-sku="' + p.id + '">' +
          '<div class="meta" style="font-family:var(--mono);font-size:0.72rem;margin-bottom:4px">' + esc(p.code || p.id) + '</div>' +
          '<div class="nm">' + esc(p.name) + '</div>' +
          '<div class="pr">' + fmtPrice(p.price) + '</div>' +
          '<div class="st' + (p.stock <= 3 ? ' low' : '') + '">Bloom: <b>' + p.stock + '</b> · сайт: <b>' + (p.siteStock != null ? p.siteStock : '—') + '</b></div>' +
          '<div class="vit-actions">' +
            '<button type="button" data-vit="minus" data-id="' + p.id + '">−</button>' +
            '<button type="button" data-vit="plus" data-id="' + p.id + '">+</button>' +
            '<button type="button" data-vit="sync" data-id="' + p.id + '">API</button>' +
            '<button type="button" data-vit="hide" data-id="' + p.id + '">' + (p.hidden ? 'показать' : 'скрыть') + '</button>' +
          '</div></div>';
      }).join('') || '<div style="color:var(--ink-faint)">Нет позиций</div>';
    }
  }"""

if old_rv not in text:
    raise SystemExit("renderVitrina not found")
text = text.replace(old_rv, new_rv)

# switchView orders set view
text = text.replace(
    """    if (view === 'orders') {
      liveSay('Имитация запущена');
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 400);
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 1100);
    }""",
    """    if (view === 'orders') {
      setOrdersView(ordersView);
      liveSay('Имитация запущена');
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 400);
      setTimeout(function () { if (!state.simPaused && state.view === 'orders') simTick(); }, 1100);
    }""",
)

# vit actions sync + bind orders view
text = text.replace(
    """        if (act === 'plus') p.stock++;
        if (act === 'minus') p.stock = Math.max(0, p.stock - 1);
        if (act === 'price') p.price = Math.max(100, p.price + 100);
        if (act === 'hide') p.hidden = !p.hidden;
        renderVitrina();
        toast(p.name + ' обновлён');""",
    """        if (act === 'plus') p.stock++;
        if (act === 'minus') p.stock = Math.max(0, p.stock - 1);
        if (act === 'price') p.price = Math.max(100, p.price + 100);
        if (act === 'hide') p.hidden = !p.hidden;
        if (act === 'sync') {
          // mock: pull site stock pointer into Bloom (future API)
          if (p.siteStock != null) p.stock = p.siteStock;
          toast('Остаток с сайта → Bloom: ' + p.stock);
        } else {
          toast(p.name + ' обновлён');
        }
        // mock site drift
        if (act === 'plus' || act === 'minus') {
          /* siteStock stays until API sync */
        }
        renderVitrina();""",
)

# bind orders toolbar
bind_extra = r"""
    var ovt = $('#ordersViewToggle');
    if (ovt) ovt.addEventListener('click', function (e) {
      var b = e.target.closest('[data-oview]');
      if (b) setOrdersView(b.getAttribute('data-oview'));
    });
    var os = $('#ordersSearch');
    if (os) os.addEventListener('input', function () { ordersSearch = this.value; renderOrdersList(); });
    var of = $('#ordersStatusFilter');
    if (of) of.addEventListener('change', function () { ordersStatusFilter = this.value; renderOrdersList(); });
    var olb = $('#ordersListBody');
    if (olb) olb.addEventListener('click', function (e) {
      var tr = e.target.closest('tr[data-id]');
      if (tr) openOrderDrawer(tr.getAttribute('data-id'));
    });
    var nvt = $('#nomViewToggle');
    if (nvt) nvt.addEventListener('click', function (e) {
      var b = e.target.closest('[data-nview]');
      if (!b) return;
      nomView = b.getAttribute('data-nview');
      renderVitrina();
    });
    var ns = $('#nomSearch');
    if (ns) ns.addEventListener('input', function () { nomSearch = this.value; renderVitrina(); });
    var ng = $('#nomGroup');
    if (ng) ng.addEventListener('change', function () { nomGroup = this.value; renderVitrina(); });

"""

marker = """    var sw = $('#shopSwitcher');"""
if "ordersViewToggle" not in text.split("function bind")[1][:3000] if "function bind" in text else True:
    if marker in text and "ordersViewToggle" not in text[text.find("function bind") : text.find("function bind") + 8000]:
        text = text.replace(marker, bind_extra + marker)

# init setOrdersView
text = text.replace(
    """  renderVitrina();
  renderSettings();
  updateShopBanner();
  renderClients();
  bind();
  startSim();
})();""",
    """  renderVitrina();
  renderSettings();
  updateShopBanner();
  renderClients();
  setOrdersView('list');
  bind();
  startSim();
})();""",
)

# proto chip ERPNext
text = text.replace(
    '<span class="chip">Dolibarr · оплата ∥ статус · витрина</span>',
    '<span class="chip">ERPNext · список заказов + номенклатура</span>\n      <span class="chip">Dolibarr · оплата ∥ статус</span>',
)

BASE.write_text(text, encoding="utf-8")
for c in COPIES:
    c.write_text(text, encoding="utf-8")
print("OK", BASE.stat().st_size)
# sanity
assert "so-list" in text
assert "nom-table" in text
assert "setOrdersView" in text
assert "siteStock" in text
print("asserts ok")
