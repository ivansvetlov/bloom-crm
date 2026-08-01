# -*- coding: utf-8 -*-
"""Add Dolibarr-style invoices + multi-warehouse stock page to kp/demo/demo.html"""
from pathlib import Path
import re

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
text = BASE.read_text(encoding="utf-8")

CSS = r"""
  /* ═══ Dolibarr: invoices + warehouses ═══ */
  .inv-table, .wh-table {
    width: 100%; border-collapse: collapse; background: var(--bg-2);
    border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
    box-shadow: var(--shadow-sm);
  }
  .inv-table th, .wh-table th {
    text-align: left; font-size: 0.7rem; font-weight: 700; color: var(--ink-faint);
    text-transform: uppercase; letter-spacing: 0.04em;
    padding: 10px 12px; border-bottom: 1px solid var(--border); background: var(--bg);
  }
  .inv-table td, .wh-table td {
    padding: 11px 12px; border-bottom: 1px solid var(--border);
    font-size: 0.86rem; color: var(--ink-dim); vertical-align: middle;
  }
  .inv-table tr:last-child td, .wh-table tr:last-child td { border-bottom: 0; }
  .inv-table tr { cursor: pointer; }
  .inv-table tr:hover td { background: var(--bg-3); }
  .inv-st {
    font-size: 0.68rem; font-weight: 700; padding: 3px 8px; border-radius: 999px;
  }
  .inv-st.draft { background: var(--bg-3); color: var(--ink-mute); }
  .inv-st.validated { background: var(--plum-soft); color: var(--plum); }
  .inv-st.paid { background: var(--sage-soft); color: var(--sage); }
  .inv-st.cancelled { background: var(--red-soft); color: var(--red); }
  .inv-toolbar, .wh-toolbar {
    display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px;
  }
  .inv-toolbar select, .wh-toolbar select, .inv-toolbar input {
    border: 1px solid var(--border-2); border-radius: 10px; padding: 9px 12px;
    font-family: var(--font); font-size: 0.86rem; background: var(--bg-2);
  }
  .wh-grid {
    display: grid; grid-template-columns: 220px 1fr; gap: 14px; align-items: start;
  }
  .wh-side {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 10px; box-shadow: var(--shadow-sm);
  }
  .wh-side button {
    display: block; width: 100%; text-align: left; border: 0; background: transparent;
    padding: 10px 12px; border-radius: 10px; cursor: pointer; font-family: var(--font);
    font-size: 0.86rem; font-weight: 700; color: var(--ink-dim); margin-bottom: 4px;
  }
  .wh-side button:hover { background: var(--bg-3); }
  .wh-side button.on { background: var(--terra-soft); color: var(--terra); }
  .wh-side .wh-meta { font-size: 0.72rem; font-weight: 600; color: var(--ink-faint); display: block; margin-top: 2px; }
  .wh-main {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 14px; box-shadow: var(--shadow-sm); min-height: 280px;
  }
  .wh-main h3 { font-size: 0.95rem; font-weight: 800; margin-bottom: 10px; }
  .wh-matrix {
    width: 100%; border-collapse: collapse; font-size: 0.82rem;
  }
  .wh-matrix th, .wh-matrix td {
    padding: 8px 10px; border-bottom: 1px solid var(--border); text-align: left;
  }
  .wh-matrix th { font-size: 0.7rem; color: var(--ink-faint); text-transform: uppercase; }
  .wh-matrix .num { text-align: right; font-weight: 800; font-variant-numeric: tabular-nums; }
  .wh-matrix input {
    width: 64px; border: 1px solid var(--border-2); border-radius: 8px; padding: 4px 6px;
    font-family: var(--mono); font-size: 0.8rem; text-align: right;
  }
  .move-box {
    margin-top: 14px; padding: 12px; background: var(--bg); border-radius: 12px; border: 1px solid var(--border);
  }
  .move-box h4 { font-size: 0.84rem; font-weight: 800; margin-bottom: 8px; }
  .move-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .move-row select, .move-row input {
    border: 1px solid var(--border-2); border-radius: 8px; padding: 8px 10px;
    font-family: var(--font); font-size: 0.84rem; background: #fff;
  }
  @media (max-width: 900px) {
    .wh-grid { grid-template-columns: 1fr; }
  }
"""

if "/* ═══ Dolibarr: invoices + warehouses ═══ */" not in text:
    text = text.replace("</style>", CSS + "\n</style>")

# Nav renumber + add invoices & warehouses
old_nav = """    <button class="sb-link" data-view="vitrina"><span class="idx">05</span>Номенклатура</button>
    <button class="sb-link" data-view="analytics"><span class="idx">06</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">07</span>Настройки</button>"""

new_nav = """    <button class="sb-link" data-view="vitrina"><span class="idx">05</span>Номенклатура</button>
    <button class="sb-link" data-view="warehouses"><span class="idx">06</span>Склады</button>
    <button class="sb-link" data-view="invoices"><span class="idx">07</span>Счета</button>
    <button class="sb-link" data-view="analytics"><span class="idx">08</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">09</span>Настройки</button>"""

if old_nav not in text:
    raise SystemExit("nav not found")
text = text.replace(old_nav, new_nav)

# HTML sections before settings
SECTIONS = r"""
    <!-- ═════════════ WAREHOUSES (Dolibarr multi-warehouse) ═════════════ -->
    <section data-section="warehouses" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Dolibarr · multi-warehouse</span>
        <span class="chip sage">Перемещения · остатки по точкам</span>
      </div>
      <div class="nom-api-note">
        <b>Склады</b> — остатки SKU по складам сети (как multi-warehouse в Dolibarr).
        Позже: связь с API витрины сайта + резерв под заказы.
      </div>
      <div class="wh-grid">
        <aside class="wh-side" id="whSide"></aside>
        <div class="wh-main">
          <h3 id="whTitle">Склад</h3>
          <table class="wh-matrix">
            <thead>
              <tr><th>Код</th><th>Товар</th><th class="num">Остаток</th><th class="num">Резерв</th><th class="num">Доступно</th><th></th></tr>
            </thead>
            <tbody id="whBody"></tbody>
          </table>
          <div class="move-box">
            <h4>Перемещение между складами</h4>
            <div class="move-row">
              <select id="mvFrom"></select>
              <span>→</span>
              <select id="mvTo"></select>
              <select id="mvSku"></select>
              <input type="number" id="mvQty" value="1" min="1" style="width:72px" />
              <button type="button" class="btn terra" id="btnMoveStock">Переместить</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═════════════ INVOICES (Dolibarr Facture) ═════════════ -->
    <section data-section="invoices" style="display:none">
      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Dolibarr · Facture / счета</span>
        <span class="chip">Цепочка: Заказ → Счёт → Оплата</span>
      </div>
      <div class="inv-toolbar">
        <select id="invFilter">
          <option value="*">Все статусы</option>
          <option value="draft">Черновик</option>
          <option value="validated">Выставлен</option>
          <option value="paid">Оплачен</option>
          <option value="cancelled">Отменён</option>
        </select>
        <button type="button" class="btn terra" id="btnInvFromOrder">+ Счёт из заказа</button>
        <button type="button" class="btn" id="btnInvDraft">+ Черновик</button>
      </div>
      <table class="inv-table">
        <thead>
          <tr>
            <th>№ счёта</th>
            <th>Заказ</th>
            <th>Клиент / описание</th>
            <th>Точка</th>
            <th>Статус</th>
            <th>Сумма</th>
            <th></th>
          </tr>
        </thead>
        <tbody id="invBody"></tbody>
      </table>
    </section>

"""

if 'data-section="invoices"' not in text:
    text = text.replace(
        '    <section data-section="settings" style="display:none">',
        SECTIONS + '    <section data-section="settings" style="display:none">',
    )

# VIEW_NAMES
text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', chats: 'Чаты', vitrina: 'Номенклатура', analytics: 'Отчёты', settings: 'Настройки' };",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', chats: 'Чаты', vitrina: 'Номенклатура', warehouses: 'Склады', invoices: 'Счета', analytics: 'Отчёты', settings: 'Настройки' };",
)

# switchView hooks
text = text.replace(
    """    if (view === 'clients') renderClients();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    updateShopBanner();""",
    """    if (view === 'clients') renderClients();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    if (view === 'warehouses') renderWarehouses();
    if (view === 'invoices') renderInvoices();
    updateShopBanner();""",
)

# data: warehouses + invoices after products
WH_DATA = r"""
  var warehouses = [
    { id: 'wh-center', name: 'Склад · Мира 14', shop: 'Мира 14', type: 'точка' },
    { id: 'wh-south', name: 'Склад · Ленина 92', shop: 'Ленина 92', type: 'точка' },
    { id: 'wh-north', name: 'Склад · Рижская 8', shop: 'Рижская 8', type: 'точка' },
    { id: 'wh-hub', name: 'Хаб · центральный', shop: '*', type: 'хаб' }
  ];
  // stockByWh[whId][productId] = qty
  var stockByWh = {};
  var activeWh = 'wh-center';
  var invFilter = '*';
  var invSeq = 100;

  function initStockMatrix() {
    warehouses.forEach(function (w) {
      stockByWh[w.id] = stockByWh[w.id] || {};
      products.forEach(function (p, i) {
        if (stockByWh[w.id][p.id] == null) {
          // distribute mock stock
          var base = p.stock || 0;
          if (w.id === 'wh-hub') stockByWh[w.id][p.id] = Math.max(0, base + 5);
          else if (w.shop === 'Мира 14') stockByWh[w.id][p.id] = Math.max(0, Math.floor(base * 0.45));
          else if (w.shop === 'Ленина 92') stockByWh[w.id][p.id] = Math.max(0, Math.floor(base * 0.35));
          else stockByWh[w.id][p.id] = Math.max(0, base - Math.floor(base * 0.8));
        }
      });
    });
  }
  initStockMatrix();

  var invoices = [
    { id: 'INV-2091', orderId: 'FW-1037', title: 'Пионовидная роза, 7 шт.', shop: 'Рижская 8', amount: 2700, status: 'paid', client: 'Ирина' },
    { id: 'INV-2092', orderId: 'FW-1038', title: 'Букет гербер, 25 шт.', shop: 'Ленина 92', amount: 2800, status: 'validated', client: 'Алексей' },
    { id: 'INV-2093', orderId: 'WA-881', title: 'Торт «Красный бархат»', shop: 'Рижская 8', amount: 1890, status: 'draft', client: 'Марина К.' }
  ];
"""

if "var warehouses =" not in text:
    # insert after nomGroup vars
    anchor = "  var nomGroup = '*';"
    if anchor not in text:
        raise SystemExit("nomGroup anchor not found")
    text = text.replace(anchor, anchor + "\n" + WH_DATA)

# order drawer: create invoice button in odFoot - patch openOrderDrawer
text = text.replace(
    """    $('#odFoot').innerHTML =
      (next ? '<button type="button" class="btn terra" id="odAdvance">→ ' + NAMES[next] + '</button>' : '') +
      '<button type="button" class="btn" id="odTogglePay">Сменить оплату</button>';""",
    """    $('#odFoot').innerHTML =
      (next ? '<button type="button" class="btn terra" id="odAdvance">→ ' + NAMES[next] + '</button>' : '') +
      '<button type="button" class="btn" id="odTogglePay">Сменить оплату</button>' +
      '<button type="button" class="btn" id="odMakeInv">+ Счёт (Dolibarr)</button>';""",
)

text = text.replace(
    """    $('#odTogglePay').onclick = function () {
      var cycle = ['pending', 'paid', 'cod'];
      var i = cycle.indexOf(o.pay || 'pending');
      o.pay = cycle[(i + 1) % cycle.length];
      o.history = o.history || [];
      o.history.push({ t: Date.now(), text: 'Оплата: ' + PAY_NAMES[o.pay] });
      renderAllKanban();
      openOrderDrawer(id);
      toast('Оплата: ' + PAY_NAMES[o.pay]);
    };
  }""",
    """    $('#odTogglePay').onclick = function () {
      var cycle = ['pending', 'paid', 'cod'];
      var i = cycle.indexOf(o.pay || 'pending');
      o.pay = cycle[(i + 1) % cycle.length];
      o.history = o.history || [];
      o.history.push({ t: Date.now(), text: 'Оплата: ' + PAY_NAMES[o.pay] });
      renderAllKanban();
      openOrderDrawer(id);
      toast('Оплата: ' + PAY_NAMES[o.pay]);
    };
    var mi = $('#odMakeInv');
    if (mi) mi.onclick = function () { createInvoiceFromOrder(id); };
  }""",
)

INV_WH_JS = r"""
  /* ────────────────────────── WAREHOUSES (Dolibarr) ────────────────────────── */
  function renderWarehouses() {
    var side = $('#whSide');
    var body = $('#whBody');
    if (!side || !body) return;
    var list = warehouses.filter(function (w) {
      if (state.shop === '*' || w.shop === '*') return true;
      return w.shop === state.shop || w.id === 'wh-hub';
    });
    if (!list.filter(function (w) { return w.id === activeWh; }).length) {
      activeWh = list[0] ? list[0].id : 'wh-center';
    }
    side.innerHTML = list.map(function (w) {
      return '<button type="button" class="' + (w.id === activeWh ? 'on' : '') + '" data-wh="' + w.id + '">' +
        esc(w.name) + '<span class="wh-meta">' + esc(w.type) + (w.shop !== '*' ? ' · ' + esc(w.shop) : '') + '</span></button>';
    }).join('');

    var wh = warehouses.filter(function (w) { return w.id === activeWh; })[0];
    $('#whTitle').textContent = wh ? wh.name : 'Склад';
    var st = stockByWh[activeWh] || {};
    body.innerHTML = products.map(function (p) {
      var qty = st[p.id] || 0;
      var reserve = Math.min(qty, p.stock <= 3 ? 1 : 0);
      var free = Math.max(0, qty - reserve);
      return '<tr>' +
        '<td class="sku">' + esc(p.code || p.id) + '</td>' +
        '<td>' + esc(p.name) + '</td>' +
        '<td class="num"><input type="number" min="0" value="' + qty + '" data-wh-qty="' + p.id + '" /></td>' +
        '<td class="num">' + reserve + '</td>' +
        '<td class="num"><b>' + free + '</b></td>' +
        '<td><button type="button" class="btn" style="padding:4px 8px;font-size:0.74rem" data-wh-save="' + p.id + '">OK</button></td></tr>';
    }).join('');

    // move selects
    var mf = $('#mvFrom'), mt = $('#mvTo'), ms = $('#mvSku');
    if (mf && mt && ms) {
      var optsW = warehouses.map(function (w) {
        return '<option value="' + w.id + '">' + esc(w.name) + '</option>';
      }).join('');
      mf.innerHTML = optsW;
      mt.innerHTML = optsW;
      mf.value = activeWh;
      mt.value = warehouses[0] && warehouses[0].id !== activeWh ? warehouses[0].id : (warehouses[1] ? warehouses[1].id : activeWh);
      ms.innerHTML = products.map(function (p) {
        return '<option value="' + p.id + '">' + esc(p.code || p.id) + ' · ' + esc(p.name) + '</option>';
      }).join('');
    }
  }

  function saveWhQty(pid, qty) {
    stockByWh[activeWh] = stockByWh[activeWh] || {};
    stockByWh[activeWh][pid] = Math.max(0, parseInt(qty, 10) || 0);
    // roll up to product.stock for display
    var total = 0;
    warehouses.forEach(function (w) {
      total += (stockByWh[w.id] && stockByWh[w.id][pid]) || 0;
    });
    var p = products.filter(function (x) { return x.id === pid; })[0];
    if (p) p.stock = total;
    renderWarehouses();
    renderVitrina();
    toast('Остаток на складе обновлён');
  }

  function moveStock() {
    var from = $('#mvFrom').value;
    var to = $('#mvTo').value;
    var sku = $('#mvSku').value;
    var qty = Math.max(1, parseInt($('#mvQty').value, 10) || 1);
    if (from === to) { toast('Склады должны отличаться'); return; }
    stockByWh[from] = stockByWh[from] || {};
    stockByWh[to] = stockByWh[to] || {};
    var have = stockByWh[from][sku] || 0;
    if (have < qty) { toast('Недостаточно на складе-источнике'); return; }
    stockByWh[from][sku] = have - qty;
    stockByWh[to][sku] = (stockByWh[to][sku] || 0) + qty;
    var total = 0;
    warehouses.forEach(function (w) { total += (stockByWh[w.id] && stockByWh[w.id][sku]) || 0; });
    var p = products.filter(function (x) { return x.id === sku; })[0];
    if (p) p.stock = total;
    renderWarehouses();
    renderVitrina();
    log('Перемещение <b>' + qty + ' шт.</b> · ' + esc(p ? p.name : sku), 'ok');
    toast('Перемещено ' + qty + ' шт.');
  }

  /* ────────────────────────── INVOICES (Dolibarr Facture) ────────────────────────── */
  var INV_ST = {
    draft: 'Черновик',
    validated: 'Выставлен',
    paid: 'Оплачен',
    cancelled: 'Отменён'
  };

  function renderInvoices() {
    var body = $('#invBody');
    if (!body) return;
    var list = shopFilter(invoices).filter(function (inv) {
      if (invFilter !== '*' && inv.status !== invFilter) return false;
      return true;
    });
    body.innerHTML = list.map(function (inv) {
      return '<tr data-inv="' + inv.id + '">' +
        '<td><b style="font-family:var(--mono);font-size:0.78rem">' + esc(inv.id) + '</b></td>' +
        '<td><a href="#" data-open-order="' + esc(inv.orderId || '') + '" style="color:var(--terra);font-weight:700">' + esc(inv.orderId || '—') + '</a></td>' +
        '<td>' + esc(inv.client || '') + '<div class="meta" style="font-size:0.72rem;color:var(--ink-mute)">' + esc(inv.title || '') + '</div></td>' +
        '<td>' + esc(inv.shop) + '</td>' +
        '<td><span class="inv-st ' + inv.status + '">' + (INV_ST[inv.status] || inv.status) + '</span></td>' +
        '<td><b>' + fmtPrice(inv.amount) + '</b></td>' +
        '<td class="nom-actions">' +
          (inv.status === 'draft' ? '<button type="button" data-inv-act="validate" data-id="' + inv.id + '">Выставить</button>' : '') +
          (inv.status === 'validated' ? '<button type="button" data-inv-act="pay" data-id="' + inv.id + '">Оплатить</button>' : '') +
          (inv.status !== 'cancelled' && inv.status !== 'paid' ? '<button type="button" data-inv-act="cancel" data-id="' + inv.id + '">Отмена</button>' : '') +
        '</td></tr>';
    }).join('') || '<tr><td colspan="7" style="padding:16px;color:var(--ink-faint)">Нет счетов</td></tr>';
  }

  function createInvoiceFromOrder(orderId) {
    var o = state.orders.filter(function (x) { return x.id === orderId; })[0];
    if (!o) { toast('Заказ не найден'); return; }
    // already has invoice?
    var exists = invoices.filter(function (i) { return i.orderId === orderId && i.status !== 'cancelled'; })[0];
    if (exists) { toast('Счёт уже есть: ' + exists.id); switchView('invoices'); return; }
    invSeq++;
    var inv = {
      id: 'INV-' + invSeq,
      orderId: o.id,
      title: o.name,
      shop: o.shop,
      amount: o.price,
      status: o.pay === 'paid' ? 'paid' : 'draft',
      client: o.client || o.name
    };
    invoices.unshift(inv);
    o.history = o.history || [];
    o.history.push({ t: Date.now(), text: 'Счёт ' + inv.id + ' создан (Dolibarr Facture)' });
    if (state.openOrderId === o.id) openOrderDrawer(o.id);
    log('Счёт <b>' + inv.id + '</b> по заказу ' + o.id, 'ok');
    toast('Счёт ' + inv.id);
    if (state.view === 'invoices') renderInvoices();
  }

  function createDraftInvoice() {
    invSeq++;
    var shop = state.shop === '*' ? 'Мира 14' : state.shop;
    invoices.unshift({
      id: 'INV-' + invSeq,
      orderId: '',
      title: 'Услуги / доставка',
      shop: shop,
      amount: 500,
      status: 'draft',
      client: 'Клиент'
    });
    renderInvoices();
    toast('Черновик счёта');
  }

  function invAction(id, act) {
    var inv = invoices.filter(function (i) { return i.id === id; })[0];
    if (!inv) return;
    if (act === 'validate' && inv.status === 'draft') inv.status = 'validated';
    else if (act === 'pay' && inv.status === 'validated') {
      inv.status = 'paid';
      var o = state.orders.filter(function (x) { return x.id === inv.orderId; })[0];
      if (o) {
        o.pay = 'paid';
        o.history = o.history || [];
        o.history.push({ t: Date.now(), text: 'Оплата по счёту ' + inv.id });
        renderAllKanban();
      }
    } else if (act === 'cancel' && inv.status !== 'paid') inv.status = 'cancelled';
    renderInvoices();
    toast(INV_ST[inv.status] || inv.status);
  }

"""

if "WAREHOUSES (Dolibarr)" not in text:
    text = text.replace(
        "  /* ────────────────────────── INIT ────────────────────────── */",
        INV_WH_JS + "\n  /* ────────────────────────── INIT ────────────────────────── */",
    )

# bind warehouse + invoices
BIND = r"""
    // warehouses
    var whSide = $('#whSide');
    if (whSide) whSide.addEventListener('click', function (e) {
      var b = e.target.closest('[data-wh]');
      if (!b) return;
      activeWh = b.getAttribute('data-wh');
      renderWarehouses();
    });
    var whMain = $('#whBody');
    if (whMain) whMain.addEventListener('click', function (e) {
      var b = e.target.closest('[data-wh-save]');
      if (!b) return;
      var pid = b.getAttribute('data-wh-save');
      var inp = $('#whBody input[data-wh-qty="' + pid + '"]');
      if (inp) saveWhQty(pid, inp.value);
    });
    var bm = $('#btnMoveStock');
    if (bm) bm.addEventListener('click', moveStock);

    // invoices
    var invF = $('#invFilter');
    if (invF) invF.addEventListener('change', function () { invFilter = this.value; renderInvoices(); });
    var bif = $('#btnInvFromOrder');
    if (bif) bif.addEventListener('click', function () {
      var open = state.openOrderId || (shopFilter(state.orders)[0] && shopFilter(state.orders)[0].id);
      if (!open) { toast('Нет заказа для счёта'); return; }
      createInvoiceFromOrder(open);
      switchView('invoices');
    });
    var bid = $('#btnInvDraft');
    if (bid) bid.addEventListener('click', createDraftInvoice);
    var ib = $('#invBody');
    if (ib) ib.addEventListener('click', function (e) {
      var act = e.target.closest('[data-inv-act]');
      if (act) {
        invAction(act.getAttribute('data-id'), act.getAttribute('data-inv-act'));
        return;
      }
    });

"""

marker = "    var sw = $('#shopSwitcher');"
if "btnMoveStock" not in text and marker in text:
    text = text.replace(marker, BIND + marker)

# init
text = text.replace(
    """  setOrdersView('list');
  bind();
  startSim();
})();""",
    """  setOrdersView('list');
  if (typeof initStockMatrix === 'function') initStockMatrix();
  bind();
  startSim();
})();""",
)

# proto chips
text = text.replace(
    '<span class="chip">ERPNext · список заказов + номенклатура</span>',
    '<span class="chip">ERPNext · список заказов + номенклатура</span>\n      <span class="chip">Dolibarr · счета + склады</span>',
)

BASE.write_text(text, encoding="utf-8")
for c in COPIES:
    c.write_text(text, encoding="utf-8")
print("OK", BASE.stat().st_size)
assert 'data-section="invoices"' in text
assert 'data-section="warehouses"' in text
assert "createInvoiceFromOrder" in text
print("asserts ok")
