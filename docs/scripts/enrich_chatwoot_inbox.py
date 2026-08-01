# -*- coding: utf-8 -*-
"""Port Chatwoot inbox patterns into Bloom-styled chats in kp/demo/demo.html"""
from pathlib import Path

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html")
COPIES = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
text = BASE.read_text(encoding="utf-8")

CSS = r"""
  /* ═══ Chatwoot inbox features · Bloom style ═══ */
  .cw-tabs {
    display: flex; gap: 4px; padding: 0 0 10px; border-bottom: 1px solid var(--border); margin-bottom: 10px;
  }
  .cw-tab {
    flex: 1; border: 0; background: transparent; cursor: pointer; font-family: var(--font);
    font-size: 0.72rem; font-weight: 800; color: var(--ink-mute); padding: 8px 6px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center; gap: 4px;
  }
  .cw-tab:hover { background: var(--bg-3); color: var(--ink); }
  .cw-tab.on { background: var(--terra-soft); color: var(--terra); }
  .cw-tab .n {
    font-size: 0.65rem; background: var(--bg-3); color: var(--ink-mute);
    border-radius: 999px; min-width: 18px; padding: 1px 5px; font-weight: 800;
  }
  .cw-tab.on .n { background: #fff; color: var(--terra); }
  .cw-channels {
    display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px;
  }
  .cw-ch {
    border: 1px solid var(--border); background: var(--bg-2); cursor: pointer;
    font-family: var(--font); font-size: 0.68rem; font-weight: 700; color: var(--ink-mute);
    padding: 5px 9px; border-radius: 999px;
  }
  .cw-ch:hover { border-color: var(--terra); color: var(--terra); }
  .cw-ch.on { background: var(--terra); border-color: transparent; color: #fff; }
  .cw-ch.wa.on { background: var(--sage); }
  .cw-ch.tg.on { background: var(--plum); }
  .cw-ch.max.on { background: var(--amber); color: #3f2e00; }
  .chat-tab .labels { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 3px; }
  .cw-label {
    font-size: 0.6rem; font-weight: 800; padding: 2px 6px; border-radius: 999px;
    background: var(--bg-3); color: var(--ink-mute);
  }
  .cw-label.open { background: var(--sage-soft); color: var(--sage); }
  .cw-label.pending { background: var(--amber-soft); color: #A07A20; }
  .cw-label.snoozed { background: var(--plum-soft); color: var(--plum); }
  .cw-label.resolved { background: var(--bg-3); color: var(--ink-faint); }
  .cw-label.prio { background: var(--red-soft); color: var(--red); }
  .cw-label.tag { background: var(--terra-soft); color: var(--terra); }
  .cw-head-actions { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
  .cw-head-actions .btn { padding: 7px 10px; font-size: 0.74rem; }
  .canned {
    display: none; flex-wrap: wrap; gap: 6px; padding: 8px 12px 0; background: rgba(255,255,255,0.9);
    border-top: 1px solid var(--border); position: relative; z-index: 2;
  }
  .canned.show { display: flex; }
  .canned button {
    border: 1px solid var(--border); background: var(--bg-2); border-radius: 999px;
    padding: 5px 10px; font-size: 0.72rem; font-weight: 700; cursor: pointer;
    font-family: var(--font); color: var(--ink-dim);
  }
  .canned button:hover { border-color: var(--terra); color: var(--terra); }
  .typing-line {
    display: none; font-size: 0.75rem; color: var(--ink-faint); font-weight: 600;
    padding: 0 16px 6px; position: relative; z-index: 1;
  }
  .typing-line.show { display: block; }
  .cw-status-select {
    border: 1px solid var(--border); border-radius: 999px; padding: 5px 10px;
    font-family: var(--font); font-size: 0.72rem; font-weight: 700;
    background: var(--bg-2); color: var(--ink-dim); cursor: pointer;
  }
  .tg-list-head { padding-bottom: 8px; }
  .chat-tab .prio-dot {
    width: 7px; height: 7px; border-radius: 50%; background: var(--red); flex-shrink: 0;
  }
"""

if "/* ═══ Chatwoot inbox features · Bloom style ═══ */" not in text:
    text = text.replace("</style>", CSS + "\n</style>")

OLD_CHAT = """    <!-- ═════════════ 03 · CHATS (TG-like window) ═════════════ -->
    <section data-section="chats" style="display:none">
      <div class="tg-app" id="tgApp">
        <div class="tg-list">
          <div class="tg-list-head">
            <div class="tg-list-title">Чаты <span id="tgCount">3</span></div>
            <div class="tg-search">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
              <input id="tgSearch" type="search" placeholder="Поиск" autocomplete="off">
            </div>
          </div>
          <div class="tg-dialogs" id="chatSide"></div>
        </div>
        <div class="tg-main">
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

NEW_CHAT = """    <!-- ═════════════ CHATS · Chatwoot patterns in Bloom style ═════════════ -->
    <section data-section="chats" style="display:none">
      <div class="tg-app" id="tgApp">
        <div class="tg-list">
          <div class="tg-list-head">
            <div class="tg-list-title">Inbox <span id="tgCount">0</span></div>
            <div class="cw-tabs" id="cwTabs">
              <button type="button" class="cw-tab on" data-inbox="mine">Мои <span class="n" id="cntMine">0</span></button>
              <button type="button" class="cw-tab" data-inbox="unassigned">Без назн. <span class="n" id="cntUnassigned">0</span></button>
              <button type="button" class="cw-tab" data-inbox="all">Все <span class="n" id="cntAll">0</span></button>
              <button type="button" class="cw-tab" data-inbox="snoozed">Отлож. <span class="n" id="cntSnoozed">0</span></button>
            </div>
            <div class="cw-channels" id="cwChannels">
              <button type="button" class="cw-ch on" data-ch="*">Все</button>
              <button type="button" class="cw-ch wa" data-ch="wa">WhatsApp</button>
              <button type="button" class="cw-ch tg" data-ch="tg">Telegram</button>
              <button type="button" class="cw-ch max" data-ch="max">MAX</button>
            </div>
            <div class="tg-search">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
              <input id="tgSearch" type="search" placeholder="Поиск диалогов" autocomplete="off">
            </div>
          </div>
          <div class="tg-dialogs" id="chatSide"></div>
        </div>
        <div class="tg-main">
          <div class="chat-head">
            <div class="who" id="chHead"></div>
            <div class="cw-head-actions">
              <select class="cw-status-select" id="chatStatusSelect" title="Статус диалога">
                <option value="open">Открыт</option>
                <option value="pending">Ожидает</option>
                <option value="snoozed">Отложен</option>
                <option value="resolved">Решён</option>
              </select>
              <button type="button" class="btn" id="btnNoteMode" title="Private note">📝 Заметка</button>
              <button type="button" class="btn" id="btnAssignMe" title="Assign">Назначить мне</button>
              <button type="button" class="btn" id="btnUnassign" title="Unassign">Снять</button>
              <button type="button" class="btn" id="btnSnooze" title="Snooze">Отложить</button>
              <button type="button" class="btn" id="btnPrio" title="Priority">!</button>
              <button type="button" class="btn" id="btnCanned" title="Canned replies">Шаблоны</button>
            </div>
          </div>
          <div class="chat-body" id="chBody"></div>
          <div class="typing-line" id="typingLine">печатает…</div>
          <div class="canned" id="cannedBox">
            <button type="button" data-canned="Здравствуйте! Чем могу помочь с букетом?">Приветствие</button>
            <button type="button" data-canned="Можем собрать к указанному времени, пришлю фото перед отправкой ✿">Фото до отправки</button>
            <button type="button" data-canned="Доставка по адресу есть, слот уточню у курьера.">Доставка</button>
            <button type="button" data-canned="Счёт отправлю ссылкой в этот чат.">Оплата</button>
            <button type="button" data-canned="Приняла! Уже у флориста, вернусь через пару минут.">Принято в работу</button>
          </div>
          <div class="chat-input">
            <button type="button" class="ico-btn" title="Вложение" aria-label="Вложение">📎</button>
            <input id="chInput" type="text" placeholder="Сообщение клиенту…" autocomplete="off">
            <button type="button" class="send" id="chSend" title="Отправить" aria-label="Отправить">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/></svg>
            </button>
          </div>
        </div>
        <aside class="tg-contact" id="tgContact">
          <div class="cc-head">Карточка · Chatwoot</div>
          <div class="cc-body" id="tgContactBody"></div>
          <div class="cc-actions">
            <button type="button" class="btn terra" id="btnOrderFromChat">+ Заказ из чата</button>
            <button type="button" class="btn" id="btnResolveChat">Решить / открыть</button>
            <button type="button" class="btn" id="btnAddLabel">+ Метка «VIP»</button>
          </div>
        </aside>
      </div>
    </section>"""

if OLD_CHAT not in text:
    raise SystemExit("chat HTML block not found — structure changed?")
text = text.replace(OLD_CHAT, NEW_CHAT)

# Expand chats seed data
OLD_CHATS = """  var chats = [
    {
      id: 'wa', name: 'Марина К.', channel: 'wa', shop: 'Мира 14', unread: 2,
      msgs: [
        { me: false, text: 'Добрый день! Можно букет пионов на пятницу, до 12?' },
        { me: true, text: 'Конечно! Соберём нежно-розовый, 15 шт. — 3 200 ₽. Доставим к 11:30 ✿' },
        { me: false, text: 'Отлично, тогда в 11:30 ждём. Оплата по ссылке, да?' },
        { me: false, text: 'И ещё можно маленький бонус-сюрприз положить?' }
      ]
    },
    {
      id: 'tg', name: 'Алексей', channel: 'tg', shop: 'Ленина 92', unread: 1,
      msgs: [
        { me: false, text: 'Здравствуйте! Сколько стоят тюльпаны к 8 Марта?' },
        { me: true, text: 'Добрый день! 21 шт. — 1 990 ₽, 25 шт. — 2 400 ₽. Можно предзаказ.' },
        { me: false, text: 'А доставка в офис на Строителей есть?' }
      ]
    },
    {
      id: 'max', name: 'Елена С.', channel: 'max', shop: 'Рижская 8', unread: 0,
      msgs: [
        { me: false, text: 'Здравствуйте, корзину «Счастье» возможно собрать к завтрашнему утру?' },
        { me: true, text: 'Да! Соберём к 9:00, к 10:00 будет у адресата.' }
      ]
    }
  ];"""

NEW_CHATS = """  var chats = [
    {
      id: 'wa', name: 'Марина К.', channel: 'wa', shop: 'Мира 14', unread: 2,
      status: 'open', assignee: 'Анна К.', priority: true, labels: ['доставка', 'VIP'],
      msgs: [
        { me: false, text: 'Добрый день! Можно букет пионов на пятницу, до 12?' },
        { me: true, text: 'Конечно! Соберём нежно-розовый, 15 шт. — 3 200 ₽. Доставим к 11:30 ✿' },
        { me: false, text: 'Отлично, тогда в 11:30 ждём. Оплата по ссылке, да?' },
        { me: false, text: 'И ещё можно маленький бонус-сюрприз положить?' }
      ]
    },
    {
      id: 'tg', name: 'Алексей', channel: 'tg', shop: 'Ленина 92', unread: 1,
      status: 'pending', assignee: null, priority: false, labels: ['опт'],
      msgs: [
        { me: false, text: 'Здравствуйте! Сколько стоят тюльпаны к 8 Марта?' },
        { me: true, text: 'Добрый день! 21 шт. — 1 990 ₽, 25 шт. — 2 400 ₽. Можно предзаказ.' },
        { me: false, text: 'А доставка в офис на Строителей есть?' }
      ]
    },
    {
      id: 'max', name: 'Елена С.', channel: 'max', shop: 'Рижская 8', unread: 0,
      status: 'open', assignee: 'Анна К.', priority: false, labels: [],
      msgs: [
        { me: false, text: 'Здравствуйте, корзину «Счастье» возможно собрать к завтрашнему утру?' },
        { me: true, text: 'Да! Соберём к 9:00, к 10:00 будет у адресата.' }
      ]
    },
    {
      id: 'wa2', name: 'Ольга Н.', channel: 'wa', shop: 'Мира 14', unread: 0,
      status: 'snoozed', assignee: null, priority: false, labels: ['повтор'],
      msgs: [
        { me: false, text: 'Можно тот же букет, что на прошлой неделе?' },
        { me: true, text: 'Конечно, нашла в истории. На когда?' }
      ]
    },
    {
      id: 'tg2', name: 'Игорь', channel: 'tg', shop: 'Рижская 8', unread: 3,
      status: 'open', assignee: null, priority: true, labels: ['срочно'],
      msgs: [
        { me: false, text: 'Нужен букет сегодня до 15:00, центр' },
        { me: false, text: 'Бюджет до 4000' },
        { me: false, text: 'Есть что-то готовое?' }
      ]
    },
    {
      id: 'max2', name: 'Светлана', channel: 'max', shop: 'Ленина 92', unread: 0,
      status: 'resolved', assignee: 'Анна К.', priority: false, labels: [],
      msgs: [
        { me: false, text: 'Спасибо, всё доставили вовремя!' },
        { me: true, text: 'Рады! Будем ждать снова ✿' }
      ]
    }
  ];
  var inboxFilter = 'mine';
  var channelFilter = '*';
"""

if OLD_CHATS not in text:
    raise SystemExit("chats data not found")
text = text.replace(OLD_CHATS, NEW_CHATS)

# Replace chatHtml, renderChats, renderChat, renderContact with richer versions
# Find function chatHtml through selectChat and replace carefully

import re

# Patch lastMsg / chatHtml / renderChats
old_block = None
m = re.search(
    r"  function lastMsg\(c\) \{.*?\n  function selectChat\(id\) \{.*?\n  \}",
    text,
    re.S,
)
if not m:
    # try without lastMsg
    m = re.search(
        r"  function chatHtml\(c\) \{.*?\n  function selectChat\(id\) \{.*?\n  \}",
        text,
        re.S,
    )
if not m:
    raise SystemExit("chat functions block not found")

NEW_FUNCS = r"""  function lastMsg(c) {
    if (!c.msgs || !c.msgs.length) return 'Нет сообщений';
    var m = c.msgs[c.msgs.length - 1];
    if (m.note) return '📝 ' + m.text;
    return (m.me ? 'Вы: ' : '') + m.text;
  }

  function chatStatusLabel(st) {
    return ({ open: 'Открыт', pending: 'Ожидает', snoozed: 'Отложен', resolved: 'Решён' })[st] || st || 'open';
  }

  function filteredInbox() {
    var q = (($('#tgSearch') && $('#tgSearch').value) || '').toLowerCase();
    return shopFilter(chats).filter(function (c) {
      var st = c.status || 'open';
      var asg = c.assignee || null;
      if (inboxFilter === 'mine' && asg !== state.assignee) return false;
      if (inboxFilter === 'unassigned' && asg) return false;
      if (inboxFilter === 'snoozed' && st !== 'snoozed') return false;
      if (inboxFilter === 'all') { /* ok */ }
      else if (inboxFilter === 'mine' || inboxFilter === 'unassigned') {
        if (st === 'resolved') return false;
      }
      if (channelFilter !== '*' && c.channel !== channelFilter) return false;
      if (q && (c.name + ' ' + CH_NAMES[c.channel] + ' ' + lastMsg(c) + ' ' + (c.labels || []).join(' ')).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
  }

  function updateInboxCounts() {
    var base = shopFilter(chats);
    var mine = 0, un = 0, all = 0, sn = 0;
    base.forEach(function (c) {
      var st = c.status || 'open';
      all++;
      if (st === 'snoozed') sn++;
      if (!c.assignee && st !== 'resolved') un++;
      if (c.assignee === state.assignee && st !== 'resolved') mine++;
    });
    var set = function (id, n) { var el = $(id); if (el) el.textContent = String(n); };
    set('#cntMine', mine);
    set('#cntUnassigned', un);
    set('#cntAll', all);
    set('#cntSnoozed', sn);
    set('#tgCount', filteredInbox().length);
    setText('#navUnread', base.reduce(function (s, c) { return s + (c.unread || 0); }, 0) || '0');
  }

  function chatHtml(c) {
    var av = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : 'max';
    var unread = c.unread > 0 ? '<span class="unread">' + c.unread + '</span>' : '';
    var now = new Date();
    var tm = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
    var st = c.status || 'open';
    var labels = '<div class="labels">' +
      '<span class="cw-label ' + st + '">' + chatStatusLabel(st) + '</span>' +
      (c.priority ? '<span class="cw-label prio">срочно</span>' : '') +
      (c.labels || []).slice(0, 2).map(function (t) { return '<span class="cw-label tag">' + esc(t) + '</span>'; }).join('') +
      '</div>';
    return '<button class="chat-tab' + (c.id === chats[state.chatIdx].id ? ' on' : '') + '" data-chat="' + c.id + '">' +
      (c.priority ? '<span class="prio-dot" title="priority"></span>' : '') +
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<span class="meta-col">' +
        '<div class="row1"><div class="nm">' + esc(c.name) + '</div><div class="tm">' + tm + '</div></div>' +
        '<div class="row2"><span class="cn-pill">' + CH_NAMES[c.channel] + '</span><div class="prev">' + esc(lastMsg(c)) + '</div>' + unread + '</div>' +
        labels +
      '</span></button>';
  }

  function renderChats() {
    var side = $('#chatSide');
    if (!side) return;
    var list = filteredInbox();
    side.innerHTML = list.map(chatHtml).join('') ||
      '<div style="padding:16px;color:var(--ink-faint);font-size:0.86rem;text-align:center">Нет диалогов в этом фильтре</div>';
    updateInboxCounts();
  }

  function renderChat() {
    var c = chats[state.chatIdx];
    if (!c) return;
    // if filtered out, keep showing
    var av = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : 'max';
    $('#chHead').innerHTML =
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<div><div class="nm">' + esc(c.name) + '</div><div class="ch">' + CH_NAMES[c.channel] + ' · ' + esc(c.shop) +
      (c.assignee ? ' · ' + esc(c.assignee) : ' · без назначения') +
      (c.priority ? ' · ⚡' : '') + '</div></div>';
    var sel = $('#chatStatusSelect');
    if (sel) sel.value = c.status || 'open';
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
      return (c.orderIds || []).indexOf(o.id) >= 0 || (o.channel !== 'fw' && o.shop === c.shop && o.channel === c.channel);
    }).slice(0, 4);
    el.innerHTML =
      '<div class="cc-row"><b>Имя</b>' + esc(c.name) + '</div>' +
      '<div class="cc-row"><b>Канал</b>' + CH_NAMES[c.channel] + '</div>' +
      '<div class="cc-row"><b>Точка</b>' + esc(c.shop) + '</div>' +
      '<div class="cc-row"><b>Статус inbox</b>' + chatStatusLabel(c.status || 'open') + '</div>' +
      '<div class="cc-row"><b>Ответственный</b>' + esc(c.assignee || '— не назначен') + '</div>' +
      '<div class="cc-row"><b>Приоритет</b>' + (c.priority ? '⚡ срочно' : 'обычный') + '</div>' +
      '<div class="cc-row"><b>Метки</b>' + ((c.labels && c.labels.length) ? c.labels.map(function (t) {
        return '<span class="cw-label tag">' + esc(t) + '</span>';
      }).join(' ') : '—') + '</div>' +
      '<div class="cc-row"><b>Заказы</b>' + (linked.length ? linked.map(function (o) {
        return '<div style="margin-top:4px"><a href="#" data-open-order="' + o.id + '" style="color:var(--terra);font-weight:700">' + o.id + '</a> · ' + esc(o.name) + '</div>';
      }).join('') : 'нет связанных') + '</div>';
  }

  function selectChat(id) {
    var idx = chats.findIndex(function (c) { return c.id === id; });
    if (idx < 0) return;
    state.chatIdx = idx;
    chats[idx].unread = 0;
    renderChats();
    renderChat();
    updateStats();
  }
"""

text = text[: m.start()] + NEW_FUNCS + text[m.end() :]

# sendMessage typing indicator
text = text.replace(
    """    state.typing = true;
    setTimeout(function () {
      state.typing = false;
      var reply = autoReplies[Math.floor(Math.random() * autoReplies.length)];
      c.msgs.push({ me: false, text: reply });
      renderChat();
      toast(c.name + ' ответила');
    }, 1400);
  }""",
    """    state.typing = true;
    var tl = $('#typingLine');
    if (tl) { tl.textContent = c.name + ' печатает…'; tl.classList.add('show'); }
    setTimeout(function () {
      state.typing = false;
      if (tl) tl.classList.remove('show');
      var reply = autoReplies[Math.floor(Math.random() * autoReplies.length)];
      c.msgs.push({ me: false, text: reply });
      renderChat();
      toast(c.name + ' ответила');
    }, 1400);
  }""",
)

# Enhance resolve / assign binds and add new handlers
# Replace btnAssignMe and btnResolveChat sections
text = text.replace(
    """    var bn = $('#btnNoteMode');
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
    });""",
    """    var bn = $('#btnNoteMode');
    if (bn) bn.addEventListener('click', function () {
      state.noteMode = !state.noteMode;
      bn.classList.toggle('note-on', state.noteMode);
      $('#chInput').placeholder = state.noteMode ? 'Приватная заметка (не видит клиент)…' : 'Сообщение клиенту…';
      toast(state.noteMode ? 'Private note · Chatwoot' : 'Ответ клиенту');
    });
    var ba = $('#btnAssignMe');
    if (ba) ba.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.assignee = state.assignee;
      if (c.status === 'resolved') c.status = 'open';
      c.msgs.push({ me: false, note: true, text: 'Назначено: ' + state.assignee });
      renderChats(); renderChat();
      toast('Назначено: ' + state.assignee);
    });
    var bu = $('#btnUnassign');
    if (bu) bu.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.assignee = null;
      c.msgs.push({ me: false, note: true, text: 'Снято назначение' });
      renderChats(); renderChat();
      toast('Без назначения');
    });
    var bs = $('#btnSnooze');
    if (bs) bs.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.status = c.status === 'snoozed' ? 'open' : 'snoozed';
      c.msgs.push({ me: false, note: true, text: c.status === 'snoozed' ? 'Отложено' : 'Снято с отложения' });
      renderChats(); renderChat();
      toast(chatStatusLabel(c.status));
    });
    var bp = $('#btnPrio');
    if (bp) bp.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.priority = !c.priority;
      renderChats(); renderChat();
      toast(c.priority ? 'Приоритет включён' : 'Приоритет снят');
    });
    var bcan = $('#btnCanned');
    var cbox = $('#cannedBox');
    if (bcan && cbox) bcan.addEventListener('click', function () {
      cbox.classList.toggle('show');
    });
    if (cbox) cbox.addEventListener('click', function (e) {
      var b = e.target.closest('[data-canned]');
      if (!b) return;
      $('#chInput').value = b.getAttribute('data-canned');
      cbox.classList.remove('show');
      $('#chInput').focus();
    });
    var css = $('#chatStatusSelect');
    if (css) css.addEventListener('change', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.status = this.value;
      if (c.status === 'resolved') c.resolved = true;
      else c.resolved = false;
      c.msgs.push({ me: false, note: true, text: 'Статус: ' + chatStatusLabel(c.status) });
      renderChats(); renderChat();
      toast(chatStatusLabel(c.status));
    });
    var br = $('#btnResolveChat');
    if (br) br.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.status = c.status === 'resolved' ? 'open' : 'resolved';
      c.resolved = c.status === 'resolved';
      c.msgs.push({ me: false, note: true, text: c.resolved ? 'Диалог решён' : 'Диалог открыт снова' });
      renderChats(); renderChat();
      toast(chatStatusLabel(c.status));
    });
    var bl = $('#btnAddLabel');
    if (bl) bl.addEventListener('click', function () {
      var c = chats[state.chatIdx];
      if (!c) return;
      c.labels = c.labels || [];
      if (c.labels.indexOf('VIP') < 0) c.labels.push('VIP');
      renderChats(); renderChat();
      toast('Метка VIP');
    });
    // inbox tabs + channels
    var tabs = $('#cwTabs');
    if (tabs) tabs.addEventListener('click', function (e) {
      var t = e.target.closest('[data-inbox]');
      if (!t) return;
      inboxFilter = t.getAttribute('data-inbox');
      $$('#cwTabs .cw-tab').forEach(function (x) { x.classList.toggle('on', x === t); });
      renderChats();
    });
    var chs = $('#cwChannels');
    if (chs) chs.addEventListener('click', function (e) {
      var t = e.target.closest('[data-ch]');
      if (!t) return;
      channelFilter = t.getAttribute('data-ch');
      $$('#cwChannels .cw-ch').forEach(function (x) { x.classList.toggle('on', x === t); });
      renderChats();
    });""",
)

# proto chip
text = text.replace(
    '<span class="chip">Chatwoot · inbox + note + заказ из чата</span>',
    '<span class="chip">Chatwoot · mine/unassigned · labels · snooze · canned · note</span>',
)

BASE.write_text(text, encoding="utf-8")
for c in COPIES:
    c.write_text(text, encoding="utf-8")
print("OK", BASE.stat().st_size)
assert "cw-tabs" in text and "inboxFilter" in text and "cannedBox" in text
print("asserts ok")
