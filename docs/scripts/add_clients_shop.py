# -*- coding: utf-8 -*-
"""Add Twenty-style clients + global shop switcher to kp/demo/demo.html"""
from pathlib import Path

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
text = BASE.read_text(encoding="utf-8")

CSS = r"""
  /* ═══ Shop switcher + Clients (Twenty) ═══ */
  .sb-shop {
    margin: 10px 4px 4px; width: calc(100% - 8px);
    display: flex; align-items: center; justify-content: space-between; gap: 8px;
    padding: 10px 12px; border-radius: 12px; border: 1px solid var(--border);
    background: var(--bg); cursor: pointer; font-family: var(--font); text-align: left;
    color: var(--ink); transition: border-color 0.15s, background 0.15s;
  }
  .sb-shop:hover { border-color: var(--terra); background: var(--terra-soft); }
  .sb-shop .label { font-size: 0.68rem; font-weight: 700; color: var(--ink-faint); text-transform: uppercase; letter-spacing: 0.04em; }
  .sb-shop .val { font-size: 0.86rem; font-weight: 800; margin-top: 2px; letter-spacing: -0.01em; }
  .sb-shop .chev { color: var(--ink-mute); font-size: 0.75rem; }
  .sb-shop-menu {
    display: none; margin: 0 4px 8px; padding: 6px;
    background: var(--bg-2); border: 1px solid var(--border); border-radius: 12px;
    box-shadow: var(--shadow-sm);
  }
  .sb-shop-menu.show { display: block; }
  .sb-shop-menu button {
    display: block; width: 100%; text-align: left; border: 0; background: transparent;
    padding: 9px 10px; border-radius: 8px; cursor: pointer; font-family: var(--font);
    font-size: 0.84rem; font-weight: 600; color: var(--ink-dim);
  }
  .sb-shop-menu button:hover { background: var(--bg-3); color: var(--ink); }
  .sb-shop-menu button.on { background: var(--terra-soft); color: var(--terra); }
  .sb-shop-menu .hint {
    font-size: 0.72rem; color: var(--ink-faint); padding: 8px 10px 4px; line-height: 1.35;
  }
  .people-layout {
    display: grid; grid-template-columns: 1fr minmax(280px, 360px); gap: 14px; align-items: start;
  }
  .people-toolbar {
    display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; align-items: center;
  }
  .people-toolbar input {
    flex: 1; min-width: 180px; border: 1px solid var(--border-2); border-radius: 10px;
    padding: 10px 12px; font-family: var(--font); font-size: 0.9rem; background: var(--bg-2); outline: none;
  }
  .people-toolbar input:focus { border-color: var(--terra); }
  .people-table {
    width: 100%; border-collapse: collapse; background: var(--bg-2);
    border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden;
    box-shadow: var(--shadow-sm);
  }
  .people-table th {
    text-align: left; font-size: 0.72rem; font-weight: 700; color: var(--ink-faint);
    padding: 10px 12px; border-bottom: 1px solid var(--border); background: var(--bg);
  }
  .people-table td {
    padding: 12px; border-bottom: 1px solid var(--border); font-size: 0.88rem; color: var(--ink-dim);
    cursor: pointer;
  }
  .people-table tr:last-child td { border-bottom: 0; }
  .people-table tr:hover td { background: var(--bg-3); }
  .people-table tr.on td { background: var(--terra-soft); }
  .people-table .nm { font-weight: 800; color: var(--ink); letter-spacing: -0.01em; }
  .people-table .meta { font-size: 0.76rem; color: var(--ink-mute); }
  .people-detail {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 16px; box-shadow: var(--shadow-sm); position: sticky; top: 72px;
  }
  .people-detail .hd { display: flex; gap: 12px; align-items: center; margin-bottom: 14px; }
  .people-detail .hd .av { width: 48px; height: 48px; font-size: 1rem; }
  .people-detail h3 { font-size: 1.05rem; font-weight: 800; letter-spacing: -0.02em; }
  .people-detail .sub { font-size: 0.78rem; color: var(--ink-mute); margin-top: 2px; }
  .people-detail .row {
    display: flex; justify-content: space-between; gap: 10px;
    padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 0.86rem;
  }
  .people-detail .row span { color: var(--ink-mute); font-weight: 600; font-size: 0.76rem; }
  .people-detail .orders { margin-top: 12px; }
  .people-detail .orders a {
    display: block; color: var(--terra); font-weight: 700; font-size: 0.84rem;
    text-decoration: none; padding: 6px 0;
  }
  .shop-scope-banner {
    display: none; align-items: center; gap: 8px; flex-wrap: wrap;
    font-size: 0.82rem; font-weight: 600; color: var(--ink-dim);
    background: var(--terra-soft); border: 1px solid #efd5c6; border-radius: 12px;
    padding: 10px 12px; margin-bottom: 12px;
  }
  .shop-scope-banner.show { display: flex; }
  .shop-scope-banner b { color: var(--terra); }
  @media (max-width: 900px) {
    .people-layout { grid-template-columns: 1fr; }
    .people-detail { position: static; }
  }
"""

if "/* ═══ Shop switcher + Clients (Twenty) ═══ */" not in text:
    text = text.replace("</style>", CSS + "\n</style>")

old_brand = """    <div class="b-name">Bloom CRM <span class="pro">ПРОТОТИП</span></div>
  </div>

  <div class="sb-label">Меню</div>"""

new_brand = """    <div class="b-name">Bloom CRM <span class="pro">ПРОТОТИП</span></div>
  </div>

  <button type="button" class="sb-shop" id="shopSwitcher" title="Глобальный магазин (доступ сотрудников)">
    <div>
      <div class="label">Магазин</div>
      <div class="val" id="currentShopLabel">Вся сеть</div>
    </div>
    <span class="chev">▾</span>
  </button>
  <div class="sb-shop-menu" id="shopMenu">
    <div class="hint">Глобальный контекст точки. Позже — права сотрудников только на выбранный магазин.</div>
    <button type="button" data-shop="*" class="on">Вся сеть</button>
    <button type="button" data-shop="Мира 14">Мира 14</button>
    <button type="button" data-shop="Ленина 92">Ленина 92</button>
    <button type="button" data-shop="Рижская 8">Рижская 8</button>
  </div>

  <div class="sb-label">Меню</div>"""

if old_brand not in text:
    raise SystemExit("brand block not found")
text = text.replace(old_brand, new_brand)

old_nav = """    <button class="sb-link" data-view="orders"><span class="idx">02</span>Заказы <span class="badge" id="navNew">0</span></button>
    <button class="sb-link" data-view="chats"><span class="idx">03</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">04</span>Витрина</button>
    <button class="sb-link" data-view="analytics"><span class="idx">05</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">06</span>Настройки</button>"""

new_nav = """    <button class="sb-link" data-view="orders"><span class="idx">02</span>Заказы <span class="badge" id="navNew">0</span></button>
    <button class="sb-link" data-view="clients"><span class="idx">03</span>Клиенты</button>
    <button class="sb-link" data-view="chats"><span class="idx">04</span>Чаты <span class="badge" id="navUnread">0</span></button>
    <button class="sb-link" data-view="vitrina"><span class="idx">05</span>Витрина</button>
    <button class="sb-link" data-view="analytics"><span class="idx">06</span>Отчёты</button>
    <button class="sb-link" data-view="settings"><span class="idx">07</span>Настройки</button>"""

if old_nav not in text:
    raise SystemExit("nav not found")
text = text.replace(old_nav, new_nav)

if 'id="shopScopeBanner"' not in text:
    text = text.replace(
        """    <div class="proto-chips">
      <span class="chip">Chatwoot · inbox + note + заказ из чата</span>
      <span class="chip">Twenty · ⌘K</span>
      <span class="chip">Dolibarr · оплата ∥ статус · витрина</span>
      <span class="chip sage">Mega · витрина / настройки / drawer</span>
    </div>""",
        """    <div class="proto-chips">
      <span class="chip">Chatwoot · inbox + note + заказ из чата</span>
      <span class="chip">Twenty · клиенты + ⌘K</span>
      <span class="chip">Dolibarr · оплата ∥ статус · витрина</span>
      <span class="chip sage">Mega · витрина / настройки / drawer</span>
    </div>
    <div class="shop-scope-banner" id="shopScopeBanner">
      <span>Контекст магазина: <b id="shopScopeText">Вся сеть</b></span>
      <span style="opacity:.75">· заказы, чаты и клиенты фильтруются · позже ACL сотрудников</span>
    </div>""",
    )

if 'data-section="clients"' not in text:
    text = text.replace(
        "    <!-- ═════════════ 05 · VITRINA (Dolibarr stock) ═════════════ -->",
        """    <!-- ═════════════ CLIENTS (Twenty people) ═════════════ -->
    <section data-section="clients" style="display:none">
      <div class="people-toolbar">
        <input type="search" id="clientSearch" placeholder="Имя, телефон, канал…" autocomplete="off" />
        <button type="button" class="btn terra" id="btnAddClient">+ Клиент</button>
      </div>
      <div class="people-layout">
        <div>
          <table class="people-table">
            <thead>
              <tr><th>Клиент</th><th>Канал</th><th>Точка</th><th>Заказы</th><th>Сумма</th></tr>
            </thead>
            <tbody id="clientsBody"></tbody>
          </table>
        </div>
        <aside class="people-detail" id="clientDetail">
          <div style="color:var(--ink-faint);font-size:0.86rem">Выберите клиента в таблице · как People в Twenty</div>
        </aside>
      </div>
    </section>

    <!-- ═════════════ 05 · VITRINA (Dolibarr stock) ═════════════ -->""",
    )

text = text.replace(
    """    noteMode: false,
    openOrderId: null,
    assignee: 'Анна К.'
  };""",
    """    noteMode: false,
    openOrderId: null,
    assignee: 'Анна К.',
    shop: '*',
    clientId: null
  };

  var clientsSeed = [
    { id: 'c1', name: 'Марина К.', phone: '+7 900 111-22-33', channel: 'wa', shop: 'Мира 14', email: 'marina@mail.ru', tags: ['постоянный'] },
    { id: 'c2', name: 'Алексей', phone: '+7 900 222-33-44', channel: 'tg', shop: 'Ленина 92', email: '', tags: ['8 марта'] },
    { id: 'c3', name: 'Елена С.', phone: '+7 900 333-44-55', channel: 'max', shop: 'Рижская 8', email: 'elena@yandex.ru', tags: [] },
    { id: 'c4', name: 'Ирина', phone: '+7 900 444-55-66', channel: 'fw', shop: 'Мира 14', email: '', tags: ['маркетплейс'] },
    { id: 'c5', name: 'Дмитрий П.', phone: '+7 900 555-66-77', channel: 'wa', shop: 'Ленина 92', email: 'dmitry@mail.ru', tags: ['B2B'] },
    { id: 'c6', name: 'Ольга', phone: '+7 900 666-77-88', channel: 'fw', shop: 'Рижская 8', email: '', tags: ['новый'] }
  ];
  var clients = JSON.parse(JSON.stringify(clientsSeed));""",
)

text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', chats: 'Чаты', vitrina: 'Витрина', analytics: 'Отчёты', settings: 'Настройки' };",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', clients: 'Клиенты', chats: 'Чаты', vitrina: 'Витрина', analytics: 'Отчёты', settings: 'Настройки' };",
)

if "function shopFilter(" not in text:
    text = text.replace(
        "  function cardHtml(o) {",
        """  function shopFilter(list, key) {
    key = key || 'shop';
    if (!state.shop || state.shop === '*') return list;
    return list.filter(function (x) { return x[key] === state.shop; });
  }

  function updateShopBanner() {
    var b = $('#shopScopeBanner');
    var t = $('#shopScopeText');
    var lab = $('#currentShopLabel');
    var name = state.shop === '*' ? 'Вся сеть' : state.shop;
    if (t) t.textContent = name;
    if (lab) lab.textContent = name;
    if (b) b.classList.toggle('show', state.shop !== '*');
    $$('#shopMenu button[data-shop]').forEach(function (btn) {
      btn.classList.toggle('on', btn.getAttribute('data-shop') === state.shop);
    });
  }

  function setShop(shop) {
    state.shop = shop || '*';
    updateShopBanner();
    renderAllKanban();
    renderChats();
    if (state.view === 'clients') renderClients();
    if (state.view === 'chats') { renderChat(); renderContact(); }
    if (state.view === 'settings') renderSettings();
    updateStats();
    toast(state.shop === '*' ? 'Контекст: вся сеть' : 'Магазин: ' + state.shop);
  }

  function cardHtml(o) {""",
    )

text = text.replace(
    "      var list = state.orders.filter(function (o) { return o.status === st; });",
    "      var list = shopFilter(state.orders).filter(function (o) { return o.status === st; });",
)

text = text.replace(
    """  function updateStats() {
    var o = state.orders;""",
    """  function updateStats() {
    var o = shopFilter(state.orders);""",
)

text = text.replace(
    """    var list = chats.filter(function (c) {
      if (!q) return true;
      return (c.name + ' ' + CH_NAMES[c.channel] + ' ' + lastMsg(c)).toLowerCase().indexOf(q) >= 0;
    });""",
    """    var list = shopFilter(chats).filter(function (c) {
      if (!q) return true;
      return (c.name + ' ' + CH_NAMES[c.channel] + ' ' + lastMsg(c)).toLowerCase().indexOf(q) >= 0;
    });""",
)

text = text.replace(
    """    if (view === 'analytics') renderReports();
    if (view === 'vitrina') renderVitrina();
    if (view === 'settings') renderSettings();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    var crumb = $('#crumbView');""",
    """    if (view === 'analytics') renderReports();
    if (view === 'vitrina') renderVitrina();
    if (view === 'settings') renderSettings();
    if (view === 'clients') renderClients();
    if (view === 'chats') { renderChats(); renderChat(); renderContact(); }
    updateShopBanner();
    var crumb = $('#crumbView');""",
)

CLIENT_JS = r"""
  /* ────────────────────────── CLIENTS (Twenty) ────────────────────────── */
  function clientStats(c) {
    var ords = shopFilter(state.orders).filter(function (o) {
      return (c.orderIds || []).indexOf(o.id) >= 0 ||
        (o.shop === c.shop && (
          (c.channel === 'fw' && o.channel === 'fw') ||
          (c.channel !== 'fw' && o.channel === c.channel)
        ));
    });
    var sum = ords.reduce(function (s, o) { return s + (o.price || 0); }, 0);
    return { count: ords.length, sum: sum, orders: ords };
  }

  function renderClients() {
    var q = (($('#clientSearch') && $('#clientSearch').value) || '').toLowerCase();
    var body = $('#clientsBody');
    if (!body) return;
    var list = shopFilter(clients).filter(function (c) {
      if (!q) return true;
      return (c.name + ' ' + c.phone + ' ' + (c.email || '') + ' ' + (CH_NAMES[c.channel] || '')).toLowerCase().indexOf(q) >= 0;
    });
    body.innerHTML = list.map(function (c) {
      var st = clientStats(c);
      var on = state.clientId === c.id ? ' on' : '';
      return '<tr class="' + on.trim() + '" data-client="' + c.id + '">' +
        '<td><div class="nm">' + esc(c.name) + '</div><div class="meta">' + esc(c.phone) + '</div></td>' +
        '<td>' + (CH_NAMES[c.channel] || c.channel) + '</td>' +
        '<td>' + esc(c.shop) + '</td>' +
        '<td>' + st.count + '</td>' +
        '<td>' + fmtPrice(st.sum) + '</td></tr>';
    }).join('') || '<tr><td colspan="5" style="color:var(--ink-faint);padding:16px">Нет клиентов в этом магазине</td></tr>';
    renderClientDetail();
  }

  function renderClientDetail() {
    var el = $('#clientDetail');
    if (!el) return;
    var c = clients.filter(function (x) { return x.id === state.clientId; })[0];
    if (!c) {
      el.innerHTML = '<div style="color:var(--ink-faint);font-size:0.86rem">Выберите клиента · People как в Twenty</div>';
      return;
    }
    var st = clientStats(c);
    var av = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : c.channel === 'max' ? 'max' : 'fw';
    el.innerHTML =
      '<div class="hd"><span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<div><h3>' + esc(c.name) + '</h3><div class="sub">' + (CH_NAMES[c.channel] || '') + ' · ' + esc(c.shop) + '</div></div></div>' +
      '<div class="row"><span>Телефон</span><b>' + esc(c.phone) + '</b></div>' +
      '<div class="row"><span>Email</span><b>' + esc(c.email || '—') + '</b></div>' +
      '<div class="row"><span>Заказов</span><b>' + st.count + '</b></div>' +
      '<div class="row"><span>Сумма</span><b>' + fmtPrice(st.sum) + '</b></div>' +
      '<div class="row"><span>Теги</span><b>' + (c.tags && c.tags.length ? c.tags.join(', ') : '—') + '</b></div>' +
      '<div class="orders"><b style="font-size:0.78rem;color:var(--ink-faint)">Заказы</b>' +
      (st.orders.length ? st.orders.map(function (o) {
        return '<a href="#" data-open-order="' + o.id + '">' + o.id + ' · ' + esc(o.name) + ' · ' + fmtPrice(o.price) + '</a>';
      }).join('') : '<div style="color:var(--ink-faint);font-size:0.84rem;margin-top:6px">Пока нет заказов</div>') +
      '</div>' +
      '<div style="margin-top:14px;display:flex;flex-direction:column;gap:8px">' +
      '<button type="button" class="btn terra" id="btnClientChat">Открыть чат</button>' +
      '<button type="button" class="btn" id="btnClientOrder">+ Заказ клиенту</button>' +
      '</div>';
    var bc = $('#btnClientChat');
    if (bc) bc.onclick = function () {
      var chat = chats.filter(function (ch) { return ch.name === c.name || (ch.channel === c.channel && ch.shop === c.shop); })[0];
      if (chat) { switchView('chats'); selectChat(chat.id); }
      else toast('Чат не найден');
    };
    var bo = $('#btnClientOrder');
    if (bo) bo.onclick = function () {
      openModal();
      var mc = $('#mClient'); if (mc) mc.value = c.name;
      var ms = $('#mShop'); if (ms) ms.value = c.shop;
      var ch = $('#mChannel');
      if (ch) ch.value = c.channel === 'fw' ? 'fw' : c.channel;
    };
  }

"""

if "CLIENTS (Twenty)" not in text:
    text = text.replace(
        "  /* ────────────────────────── INIT ────────────────────────── */",
        CLIENT_JS + "\n  /* ────────────────────────── INIT ────────────────────────── */",
    )

BIND_ADD = r"""
    var sw = $('#shopSwitcher');
    var sm = $('#shopMenu');
    if (sw && sm) {
      sw.addEventListener('click', function (e) {
        e.stopPropagation();
        sm.classList.toggle('show');
      });
      sm.addEventListener('click', function (e) {
        var b = e.target.closest('[data-shop]');
        if (!b) return;
        e.stopPropagation();
        setShop(b.getAttribute('data-shop'));
        sm.classList.remove('show');
      });
      document.addEventListener('click', function () { sm.classList.remove('show'); });
    }

    var cs = $('#clientSearch');
    if (cs) cs.addEventListener('input', renderClients);
    var bac = $('#btnAddClient');
    if (bac) bac.addEventListener('click', function () {
      var id = 'c' + (clients.length + 1);
      var shop = state.shop === '*' ? 'Мира 14' : state.shop;
      clients.unshift({ id: id, name: 'Новый клиент', phone: '+7 900 000-00-00', channel: 'wa', shop: shop, email: '', tags: ['новый'] });
      state.clientId = id;
      renderClients();
      toast('Клиент добавлен · ' + shop);
    });
    var cbody = $('#clientsBody');
    if (cbody) cbody.addEventListener('click', function (e) {
      var tr = e.target.closest('[data-client]');
      if (!tr) return;
      state.clientId = tr.getAttribute('data-client');
      renderClients();
    });

"""

marker = """    var cmdk = $('#cmdk');
    if (cmdk) {
      cmdk.addEventListener('click', function (e) { if (e.target === cmdk) closeCmdk(); });
      $('#cmdkInput').addEventListener('input', function () { renderCmdk(this.value); });
      $('#cmdkList').addEventListener('click', function (e) {
        var it = e.target.closest('.cmdk-item');
        if (it) runCmdkItem(it.getAttribute('data-k'), it.getAttribute('data-v'));
      });
    }
  }"""

if "shopSwitcher" in text and "setShop(b.getAttribute" not in text:
    if marker not in text:
        raise SystemExit("cmdk bind marker not found")
    text = text.replace(marker, BIND_ADD + marker)

text = text.replace(
    """    products.forEach(function (p) {
      items.push({ t: 'SKU · ' + p.name, k: 'sku', v: p.id });
    });""",
    """    products.forEach(function (p) {
      items.push({ t: 'SKU · ' + p.name, k: 'sku', v: p.id });
    });
    shopFilter(clients).forEach(function (c) {
      items.push({ t: 'Клиент · ' + c.name, k: 'client', v: c.id });
    });""",
)

text = text.replace(
    """    else if (k === 'sku') switchView('vitrina');
  }""",
    """    else if (k === 'sku') switchView('vitrina');
    else if (k === 'client') { state.clientId = v; switchView('clients'); }
  }""",
)

text = text.replace(
    """  function renderSettings() {
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
  }""",
    """  function renderSettings() {
    var shops = $('#setShops');
    var users = $('#setUsers');
    if (shops) {
      shops.innerHTML = ['*'].concat(SIM_SHOPS).map(function (s) {
        var label = s === '*' ? 'Вся сеть' : s;
        var active = state.shop === s ? ' · сейчас' : '';
        return '<li>' + esc(label) + '<span>контекст' + active + '</span></li>';
      }).join('');
    }
    if (users) {
      var scope = state.shop === '*' ? 'сеть' : state.shop;
      users.innerHTML =
        '<li>Анна К. <span>менеджер · ' + esc(scope) + '</span></li>' +
        '<li>Игорь М. <span>доступ: Мира 14</span></li>' +
        '<li>Света П. <span>флорист · точка</span></li>' +
        '<li style="opacity:.75">Позже: ACL по выбранному магазину<span>roadmap</span></li>';
    }
  }""",
)

text = text.replace(
    """  renderVitrina();
  renderSettings();
  bind();
  startSim();
})();""",
    """  renderVitrina();
  renderSettings();
  updateShopBanner();
  renderClients();
  bind();
  startSim();
})();""",
)

BASE.write_text(text, encoding="utf-8")
for c in COPIES:
    c.write_text(text, encoding="utf-8")
print("OK", BASE.stat().st_size)
