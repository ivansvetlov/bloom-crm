# -*- coding: utf-8 -*-
"""Patch demo.html: TG-like chats window + richer Reports section."""
from __future__ import annotations

from pathlib import Path

DEMO = Path(__file__).resolve().parents[1] / "demo.html"
text = DEMO.read_text(encoding="utf-8")

# ── 1) CSS: replace chat styles + add report styles ──────────────
old_chat_css_start = "  .chat-shell { display: grid;"
old_chat_css_end = "  .g { color: var(--sage); font-weight: 700; }"

i0 = text.find(old_chat_css_start)
i1 = text.find(old_chat_css_end)
if i0 < 0 or i1 < 0:
    raise SystemExit("chat css markers not found")

new_chat_css = r'''  /* ═════════════ TG-LIKE CHATS (Bloom tokens) ═════════════ */
  .content.chat-mode {
    max-width: none;
    padding: 12px 16px 16px;
  }
  .content.chat-mode .demo-note,
  .content.chat-mode .footer { display: none; }
  .content.reports-mode { max-width: 1280px; }

  .tg-app {
    display: grid;
    grid-template-columns: 320px 1fr;
    height: calc(100vh - var(--topbar-h) - 40px);
    min-height: 520px;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid var(--border);
    background: var(--bg-2);
    box-shadow: var(--shadow);
  }
  .tg-list {
    display: flex; flex-direction: column;
    background: #fff;
    border-right: 1px solid var(--border);
    min-width: 0;
  }
  .tg-list-head {
    padding: 12px 12px 10px;
    border-bottom: 1px solid var(--border);
    display: flex; flex-direction: column; gap: 10px;
  }
  .tg-list-title {
    font-size: 0.95rem; font-weight: 800; letter-spacing: -0.02em;
    display: flex; align-items: center; justify-content: space-between;
  }
  .tg-list-title span {
    font-size: 0.72rem; font-weight: 700; color: var(--terra);
    background: var(--terra-soft); padding: 3px 8px; border-radius: 999px;
  }
  .tg-search {
    display: flex; align-items: center; gap: 8px;
    background: var(--bg-3); border-radius: 12px; padding: 9px 12px;
    border: 1px solid transparent;
  }
  .tg-search:focus-within { border-color: var(--border-2); background: #fff; }
  .tg-search input {
    border: 0; outline: 0; background: transparent; width: 100%;
    font-family: var(--font); font-size: 0.86rem; color: var(--ink);
  }
  .tg-search input::placeholder { color: var(--ink-faint); }
  .tg-dialogs { flex: 1; overflow-y: auto; padding: 6px; }
  .chat-tab {
    display: grid;
    grid-template-columns: 48px 1fr auto;
    gap: 10px; align-items: center;
    width: 100%; text-align: left;
    border: 0; background: transparent; cursor: pointer;
    padding: 10px 10px; border-radius: 14px;
    font-family: var(--font); color: var(--ink);
    transition: background 0.12s;
  }
  .chat-tab:hover { background: var(--bg-3); }
  .chat-tab.on { background: var(--terra-soft); }
  .chat-tab .av { width: 48px; height: 48px; font-size: 0.95rem; }
  .chat-tab .meta-col { min-width: 0; }
  .chat-tab .row1 {
    display: flex; align-items: baseline; justify-content: space-between; gap: 8px;
  }
  .chat-tab .nm { font-size: 0.92rem; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .chat-tab .tm { font-size: 0.72rem; color: var(--ink-faint); flex-shrink: 0; font-weight: 600; }
  .chat-tab .row2 {
    display: flex; align-items: center; gap: 8px; margin-top: 2px;
  }
  .chat-tab .prev {
    flex: 1; min-width: 0;
    font-size: 0.8rem; color: var(--ink-mute);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .chat-tab .prev b { color: var(--ink-dim); font-weight: 600; }
  .chat-tab .unread {
    margin-left: auto; font-size: 0.68rem; font-weight: 800;
    background: var(--sage); color: #fff; border-radius: 999px;
    min-width: 20px; text-align: center; padding: 2px 7px;
  }
  .chat-tab .cn-pill {
    font-size: 0.62rem; font-weight: 700; color: var(--ink-faint);
    background: var(--bg-3); padding: 2px 6px; border-radius: 6px; flex-shrink: 0;
  }

  .av {
    width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 700; color: #fff;
  }
  .av.wa { background: linear-gradient(145deg, #7aa87d, var(--sage)); }
  .av.tg { background: linear-gradient(145deg, #9a7a94, var(--plum)); }
  .av.max { background: linear-gradient(145deg, #e0b85a, var(--amber)); color: #3f2e00; }
  .av.fw { background: linear-gradient(145deg, #f08a6a, var(--terra)); }

  .tg-main { display: flex; flex-direction: column; min-width: 0; background: #F3EEE9; position: relative; }
  .tg-main::before {
    content: ""; position: absolute; inset: 0; pointer-events: none; opacity: 0.35;
    background-image:
      radial-gradient(circle at 20% 20%, rgba(224,107,74,0.07) 0 1px, transparent 1.5px),
      radial-gradient(circle at 70% 40%, rgba(111,143,114,0.08) 0 1px, transparent 1.5px),
      radial-gradient(circle at 40% 80%, rgba(122,90,116,0.06) 0 1px, transparent 1.5px);
    background-size: 28px 28px;
  }
  .chat-head {
    position: relative; z-index: 1;
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 16px; border-bottom: 1px solid var(--border);
    background: rgba(255,255,255,0.92); backdrop-filter: blur(10px);
  }
  .chat-head .who { display: flex; align-items: center; gap: 12px; min-width: 0; }
  .chat-head .nm { font-size: 0.95rem; font-weight: 800; letter-spacing: -0.02em; }
  .chat-head .ch { font-size: 0.75rem; color: var(--sage); font-weight: 600; }
  .chat-head .meta {
    font-size: 0.74rem; font-weight: 700; color: var(--sage);
    background: var(--sage-soft); padding: 6px 12px; border-radius: 999px;
  }
  .chat-head .actions { display: flex; gap: 6px; }
  .chat-head .ico-btn {
    width: 36px; height: 36px; border-radius: 50%; border: 0; cursor: pointer;
    background: transparent; color: var(--ink-mute);
    display: grid; place-items: center;
  }
  .chat-head .ico-btn:hover { background: var(--bg-3); color: var(--ink); }

  .chat-body {
    position: relative; z-index: 1;
    flex: 1; overflow-y: auto; padding: 18px 18px 10px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .bubble {
    max-width: min(72%, 460px); align-self: flex-start;
    background: #fff; border: 0; border-radius: 16px 16px 16px 6px;
    padding: 8px 10px 6px 12px; font-size: 0.92rem; color: var(--ink-dim);
    animation: pop 0.22s var(--ease);
    box-shadow: 0 1px 1px rgba(28,25,23,0.06);
    line-height: 1.4;
  }
  .bubble.me {
    align-self: flex-end;
    background: linear-gradient(180deg, #f4c4b4 0%, #efb39f 100%);
    color: #3b2219;
    border-radius: 16px 16px 6px 16px;
    box-shadow: 0 1px 1px rgba(196,92,62,0.12);
  }
  @keyframes pop { from { transform: translateY(4px); opacity: 0; } to { transform: none; opacity: 1; } }
  .bubble .time {
    display: inline-block; float: right; margin: 6px 0 0 10px;
    font-size: 0.68rem; opacity: 0.55; font-weight: 600; line-height: 1;
  }
  .bubble.me .time { opacity: 0.65; }

  .chat-input {
    position: relative; z-index: 1;
    display: flex; align-items: center; gap: 8px;
    padding: 10px 12px 12px; border-top: 1px solid var(--border);
    background: rgba(255,255,255,0.95);
  }
  .chat-input .ico-btn {
    width: 40px; height: 40px; border-radius: 50%; border: 0; cursor: pointer;
    background: transparent; color: var(--ink-mute); flex-shrink: 0;
    display: grid; place-items: center;
  }
  .chat-input .ico-btn:hover { background: var(--bg-3); color: var(--ink); }
  .chat-input input {
    flex: 1; border: 0; border-radius: 22px; padding: 12px 16px;
    font-family: var(--font); font-size: 0.92rem; background: var(--bg-3); color: var(--ink);
    outline: none;
  }
  .chat-input input:focus { background: #fff; box-shadow: inset 0 0 0 1px var(--border-2); }
  .chat-input input::placeholder { color: var(--ink-faint); }
  .chat-input .send {
    width: 42px; height: 42px; border-radius: 50%; border: 0; cursor: pointer; flex-shrink: 0;
    background: var(--terra); color: #fff;
    display: grid; place-items: center;
    box-shadow: 0 6px 16px rgba(224,107,74,0.28);
  }
  .chat-input .send:hover { background: var(--terra-2); }

  /* ═════════════ REPORTS ═════════════ */
  .rep-tabs {
    display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px;
  }
  .rep-tab {
    border: 1px solid var(--border-2); background: var(--bg-2); color: var(--ink-mute);
    font-family: var(--font); font-size: 0.82rem; font-weight: 700;
    padding: 9px 14px; border-radius: 999px; cursor: pointer;
    transition: all 0.15s;
  }
  .rep-tab:hover { color: var(--ink); border-color: var(--ink-mute); }
  .rep-tab.on {
    background: var(--terra); border-color: transparent; color: #fff;
    box-shadow: 0 4px 14px rgba(224,107,74,0.25);
  }
  .rep-panel { display: none; }
  .rep-panel.on { display: block; }
  .rep-grid-2 {
    display: grid; grid-template-columns: 1.2fr 1fr; gap: 14px; margin-bottom: 14px;
  }
  .rep-grid-3 {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 14px;
  }
  .rep-card {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 16px; box-shadow: var(--shadow-sm); min-width: 0;
  }
  .rep-card h3 {
    font-size: 0.88rem; font-weight: 800; letter-spacing: -0.01em; margin-bottom: 12px;
    display: flex; align-items: center; justify-content: space-between; gap: 8px;
  }
  .rep-card h3 em {
    font-style: normal; font-size: 0.72rem; font-weight: 700; color: var(--ink-faint);
  }
  .spark {
    display: flex; align-items: flex-end; gap: 4px; height: 88px;
  }
  .spark i {
    flex: 1; border-radius: 6px 6px 2px 2px;
    background: linear-gradient(180deg, var(--terra), #f0b49f);
    min-width: 0; display: block;
  }
  .spark.sage i { background: linear-gradient(180deg, var(--sage), #b7d0b9); }
  .spark.plum i { background: linear-gradient(180deg, var(--plum), #c9b0c4); }
  .tbl { width: 100%; border-collapse: collapse; font-size: 0.84rem; }
  .tbl th {
    text-align: left; font-size: 0.72rem; font-weight: 700; color: var(--ink-faint);
    padding: 0 0 10px; border-bottom: 1px solid var(--border);
  }
  .tbl td { padding: 10px 0; border-bottom: 1px solid var(--border); color: var(--ink-dim); }
  .tbl tr:last-child td { border-bottom: 0; }
  .tbl b { color: var(--ink); font-weight: 700; }
  .tbl .num { text-align: right; font-weight: 800; font-variant-numeric: tabular-nums; }
  .funnel { display: flex; flex-direction: column; gap: 8px; }
  .funnel .step {
    display: flex; align-items: center; gap: 10px;
  }
  .funnel .bar {
    flex: 1; height: 28px; border-radius: 8px;
    background: var(--terra-soft); overflow: hidden; position: relative;
  }
  .funnel .bar > i {
    display: block; height: 100%; border-radius: 8px;
    background: linear-gradient(90deg, var(--terra), #f08a6a);
  }
  .funnel .lbl { width: 92px; font-size: 0.78rem; font-weight: 700; color: var(--ink-mute); }
  .funnel .val { width: 48px; text-align: right; font-weight: 800; font-size: 0.84rem; }
  .heat {
    display: grid; grid-template-columns: 48px repeat(7, 1fr); gap: 4px; font-size: 0.68rem;
  }
  .heat .h { color: var(--ink-faint); font-weight: 700; text-align: center; padding: 4px 0; }
  .heat .c {
    aspect-ratio: 1; border-radius: 6px;
    background: var(--bg-3);
  }
  .heat .c.l1 { background: #fce4db; }
  .heat .c.l2 { background: #f5b89f; }
  .heat .c.l3 { background: #e07a58; }
  .heat .c.l4 { background: #c45c3e; }
  .pill-row { display: flex; flex-wrap: wrap; gap: 8px; }
  .pill-row span {
    font-size: 0.78rem; font-weight: 700; padding: 8px 12px; border-radius: 999px;
    background: var(--bg-3); color: var(--ink-dim);
  }
  .pill-row span b { color: var(--terra); }

  .g { color: var(--sage); font-weight: 700; }
'''

text = text[:i0] + new_chat_css + text[i1:]

# responsive chat
text = text.replace(
    """    .chat-shell { grid-template-columns: 1fr; height: auto; }
    .chat-side { flex-direction: row; border-right: none; border-bottom: 1px solid var(--border); overflow-x: auto; }
    .chat-tab { width: auto; white-space: nowrap; }""",
    """    .tg-app { grid-template-columns: 1fr; height: calc(100vh - var(--topbar-h) - 28px); }
    .tg-list { max-height: 38vh; border-right: 0; border-bottom: 1px solid var(--border); }
    .rep-grid-2, .rep-grid-3 { grid-template-columns: 1fr; }""",
)

# ── 2) Sidebar label ──
text = text.replace(
    '<button class="sb-link" data-view="analytics"><span class="idx">04</span>Цифры</button>',
    '<button class="sb-link" data-view="analytics"><span class="idx">04</span>Отчёты</button>',
)

# ── 3) Chats HTML ──
old_chats = """    <!-- ═════════════ 03 · CHATS ═════════════ -->
    <section data-section="chats" style="display:none">
      <div class="sec-head"><span class="sec-num">03</span><span class="sec-tag">чаты</span></div>
      <h2 class="sec-h">Переписки с клиентами</h2>
      <p class="sec-lede">Клиенты пишут <strong>как обычно</strong> — вы отвечаете из одного окна. Напишите сообщение и посмотрите ответ.</p>

      <div class="panel chat-shell">
        <div class="chat-side" id="chatSide"></div>
        <div class="chat-main">
          <div class="chat-head">
            <div class="who" id="chHead"></div>
            <span class="meta" id="chMeta">онлайн</span>
          </div>
          <div class="chat-body" id="chBody"></div>
          <div class="chat-input">
            <input id="chInput" type="text" placeholder="Написать клиенту…" autocomplete="off">
            <button class="btn terra" id="chSend">Отправить</button>
          </div>
        </div>
      </div>
    </section>"""

new_chats = """    <!-- ═════════════ 03 · CHATS (TG-like window) ═════════════ -->
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

if old_chats not in text:
    raise SystemExit("chats block not found")
text = text.replace(old_chats, new_chats)

# ── 4) Analytics → Reports HTML ──
old_an = """    <!-- ═════════════ 04 · ANALYTICS ═════════════ -->
    <section data-section="analytics" style="display:none">
      <div class="sec-head"><span class="sec-num">04</span><span class="sec-tag">цифры</span></div>
      <h2 class="sec-h">Как идут продажи</h2>
      <p class="sec-lede">Откуда приходят заказы и как растёт средний чек — простые цифры для владельца магазина.</p>

      <div class="stat-grid">
        <div class="stat">
          <div class="stat-label">Заказов за неделю</div>
          <div class="stat-val" id="anWeek">0</div>
          <div class="stat-delta up">▲ 12% к прошлой неделе</div>
        </div>
        <div class="stat">
          <div class="stat-label">Средний чек</div>
          <div class="stat-val" id="anAov">0 ₽</div>
          <div class="stat-delta up">▲ 4%</div>
        </div>
        <div class="stat">
          <div class="stat-label">Из чата в заказ</div>
          <div class="stat-val" id="anConv">0%</div>
          <div class="stat-delta up">▲ чуть выше обычного</div>
        </div>
        <div class="stat">
          <div class="stat-label">Возвраты</div>
          <div class="stat-val" id="anRet">0%</div>
          <div class="stat-delta">спокойно</div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head">
          <div class="panel-title">Откуда приходят заказы · 7 дней</div>
        </div>
        <div class="panel-body" style="padding:20px">
          <div id="barChart" style="display:flex;flex-direction:column;gap:14px"></div>
        </div>
      </div>
    </section>"""

new_an = """    <!-- ═════════════ 04 · REPORTS ═════════════ -->
    <section data-section="analytics" style="display:none">
      <div class="rep-tabs" id="repTabs">
        <button type="button" class="rep-tab on" data-rep="sales">Продажи</button>
        <button type="button" class="rep-tab" data-rep="channels">Каналы</button>
        <button type="button" class="rep-tab" data-rep="shops">Точки</button>
        <button type="button" class="rep-tab" data-rep="products">Товары</button>
        <button type="button" class="rep-tab" data-rep="ops">Операции</button>
      </div>

      <div class="rep-panel on" data-rep-panel="sales">
        <div class="stat-grid">
          <div class="stat">
            <div class="stat-label">Заказов за неделю</div>
            <div class="stat-val" id="anWeek">0</div>
            <div class="stat-delta up">▲ 12% к прошлой неделе</div>
          </div>
          <div class="stat">
            <div class="stat-label">Выручка · 7 дней</div>
            <div class="stat-val" id="anRev">0 ₽</div>
            <div class="stat-delta up">▲ 9%</div>
          </div>
          <div class="stat">
            <div class="stat-label">Средний чек</div>
            <div class="stat-val" id="anAov">0 ₽</div>
            <div class="stat-delta up">▲ 4%</div>
          </div>
          <div class="stat">
            <div class="stat-label">Повторные клиенты</div>
            <div class="stat-val" id="anRetClients">28%</div>
            <div class="stat-delta up">▲ 3 п.п.</div>
          </div>
        </div>
        <div class="rep-grid-2">
          <div class="rep-card">
            <h3>Выручка по дням <em>пн–вс</em></h3>
            <div class="spark" id="sparkRev"></div>
          </div>
          <div class="rep-card">
            <h3>Заказы по дням <em>шт.</em></h3>
            <div class="spark sage" id="sparkOrd"></div>
          </div>
        </div>
        <div class="rep-card">
          <h3>Сводка недели</h3>
          <div class="pill-row" id="salesPills"></div>
        </div>
      </div>

      <div class="rep-panel" data-rep-panel="channels">
        <div class="rep-grid-2">
          <div class="rep-card">
            <h3>Откуда заказы <em>7 дней</em></h3>
            <div id="barChart" style="display:flex;flex-direction:column;gap:14px"></div>
          </div>
          <div class="rep-card">
            <h3>Воронка: чат → заказ</h3>
            <div class="funnel" id="funnel"></div>
          </div>
        </div>
        <div class="stat-grid">
          <div class="stat">
            <div class="stat-label">Из чата в заказ</div>
            <div class="stat-val" id="anConv">34%</div>
            <div class="stat-delta up">▲ чуть выше обычного</div>
          </div>
          <div class="stat">
            <div class="stat-label">Ответ &lt; 3 мин</div>
            <div class="stat-val">81%</div>
            <div class="stat-delta up">SLA ок</div>
          </div>
          <div class="stat">
            <div class="stat-label">Непрочитанные</div>
            <div class="stat-val" id="anUnreadRep">0</div>
            <div class="stat-delta warn">нужен ответ</div>
          </div>
          <div class="stat">
            <div class="stat-label">Возвраты</div>
            <div class="stat-val" id="anRet">1.2%</div>
            <div class="stat-delta">спокойно</div>
          </div>
        </div>
      </div>

      <div class="rep-panel" data-rep-panel="shops">
        <div class="rep-grid-2">
          <div class="rep-card">
            <h3>Точки · рейтинг</h3>
            <table class="tbl" id="shopTable"></table>
          </div>
          <div class="rep-card">
            <h3>Нагрузка по часам <em>пн–вс</em></h3>
            <div class="heat" id="heat"></div>
          </div>
        </div>
      </div>

      <div class="rep-panel" data-rep-panel="products">
        <div class="rep-grid-2">
          <div class="rep-card">
            <h3>Топ букетов <em>по выручке</em></h3>
            <table class="tbl" id="prodTable"></table>
          </div>
          <div class="rep-card">
            <h3>Категории <em>доля</em></h3>
            <div class="spark plum" id="sparkCat" style="height:120px;margin-bottom:12px"></div>
            <div class="pill-row" id="catPills"></div>
          </div>
        </div>
      </div>

      <div class="rep-panel" data-rep-panel="ops">
        <div class="stat-grid">
          <div class="stat">
            <div class="stat-label">Собрано вовремя</div>
            <div class="stat-val">94%</div>
            <div class="stat-delta up">норма</div>
          </div>
          <div class="stat">
            <div class="stat-label">Среднее время сборки</div>
            <div class="stat-val">38 м</div>
            <div class="stat-delta">−4 мин</div>
          </div>
          <div class="stat">
            <div class="stat-label">Доставка в слот</div>
            <div class="stat-val">91%</div>
            <div class="stat-delta up">▲ 2 п.п.</div>
          </div>
          <div class="stat">
            <div class="stat-label">Отмены</div>
            <div class="stat-val">2.1%</div>
            <div class="stat-delta">без всплеска</div>
          </div>
        </div>
        <div class="rep-grid-2">
          <div class="rep-card">
            <h3>Курьеры · сегодня</h3>
            <table class="tbl" id="courierTable"></table>
          </div>
          <div class="rep-card">
            <h3>Статусы сейчас</h3>
            <div class="pill-row" id="opsPills"></div>
          </div>
        </div>
      </div>
    </section>"""

if old_an not in text:
    raise SystemExit("analytics block not found")
text = text.replace(old_an, new_an)

# ── 5) JS patches ──
text = text.replace(
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', chats: 'Чаты', analytics: 'Цифры' };\n  function switchView(view) {\n    $$('[data-section]').forEach(function (s) { s.style.display = 'none'; });\n    var sec = $('[data-section=\"' + view + '\"]');\n    if (sec) sec.style.display = 'block';\n    $$('.sb-link').forEach(function (b) { b.classList.toggle('active', b.getAttribute('data-view') === view); });\n    window.scrollTo({ top: 0, behavior: 'smooth' });\n  }",
    "var VIEW_NAMES = { overview: 'Сегодня', orders: 'Заказы', chats: 'Чаты', analytics: 'Отчёты' };\n  function switchView(view) {\n    $$('[data-section]').forEach(function (s) { s.style.display = 'none'; });\n    var sec = $('[data-section=\"' + view + '\"]');\n    if (sec) sec.style.display = 'block';\n    $$('.sb-link').forEach(function (b) { b.classList.toggle('active', b.getAttribute('data-view') === view); });\n    var content = $('.content');\n    if (content) {\n      content.classList.toggle('chat-mode', view === 'chats');\n      content.classList.toggle('reports-mode', view === 'analytics');\n    }\n    if (view === 'analytics') renderReports();\n    window.scrollTo({ top: 0, behavior: 'smooth' });\n  }",
)

text = text.replace(
    """  function chatHtml(c) {
    var av = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : 'max';
    var unread = c.unread > 0 ? '<span class="unread">' + c.unread + '</span>' : '';
    return '<button class="chat-tab' + (c.id === chats[state.chatIdx].id ? ' on' : '') + '" data-chat="' + c.id + '">' +
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<span><div>' + esc(c.name) + '</div><div class="cn">' + CH_NAMES[c.channel] + '</div></span>' +
      unread + '</button>';
  }""",
    """  function lastMsg(c) {
    if (!c.msgs || !c.msgs.length) return 'Нет сообщений';
    var m = c.msgs[c.msgs.length - 1];
    return (m.me ? 'Вы: ' : '') + m.text;
  }
  function chatHtml(c) {
    var av = c.channel === 'wa' ? 'wa' : c.channel === 'tg' ? 'tg' : 'max';
    var unread = c.unread > 0 ? '<span class="unread">' + c.unread + '</span>' : '';
    var now = new Date();
    var tm = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
    return '<button class="chat-tab' + (c.id === chats[state.chatIdx].id ? ' on' : '') + '" data-chat="' + c.id + '">' +
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<span class="meta-col">' +
        '<div class="row1"><div class="nm">' + esc(c.name) + '</div><div class="tm">' + tm + '</div></div>' +
        '<div class="row2"><span class="cn-pill">' + CH_NAMES[c.channel] + '</span><div class="prev">' + esc(lastMsg(c)) + '</div>' + unread + '</div>' +
      '</span></button>';
  }""",
)

text = text.replace(
    """  function renderChats() {
    $('#chatSide').innerHTML = chats.map(chatHtml).join('');
  }""",
    """  function renderChats() {
    var side = $('#chatSide');
    if (!side) return;
    var q = (($('#tgSearch') && $('#tgSearch').value) || '').trim().toLowerCase();
    var list = chats.filter(function (c) {
      if (!q) return true;
      return (c.name + ' ' + CH_NAMES[c.channel] + ' ' + lastMsg(c)).toLowerCase().indexOf(q) >= 0;
    });
    side.innerHTML = list.map(chatHtml).join('') ||
      '<div style="padding:16px;color:var(--ink-faint);font-size:0.86rem;text-align:center">Ничего не найдено</div>';
    var cnt = $('#tgCount');
    if (cnt) cnt.textContent = String(chats.length);
  }""",
)

text = text.replace(
    """    $('#chHead').innerHTML =
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<div><div class="nm">' + esc(c.name) + '</div><div class="ch">' + CH_NAMES[c.channel] + ' · ' + esc(c.shop) + '</div></div>';
    $('#chMeta').textContent = 'онлайн';""",
    """    $('#chHead').innerHTML =
      '<span class="av ' + av + '">' + c.name.charAt(0) + '</span>' +
      '<div><div class="nm">' + esc(c.name) + '</div><div class="ch">' + CH_NAMES[c.channel] + ' · ' + esc(c.shop) + '</div></div>';
    $('#chMeta').textContent = 'в сети';""",
)

# Expand renderChart + add renderReports
old_chart = """  /* ────────────────────────── BAR CHART ────────────────────────── */
  function renderChart() {
    var data = [
      { label: 'Маркетплейс', value: 62, color: 'var(--terra)' },
      { label: 'WhatsApp', value: 24, color: 'var(--sage)' },
      { label: 'Telegram', value: 9, color: 'var(--plum)' },
      { label: 'MAX', value: 5, color: 'var(--amber)' }
    ];
    var max = 62;
    $('#barChart').innerHTML = data.map(function (d) {
      return '<div style="display:flex;align-items:center;gap:14px">' +
        '<div style="width:110px;font-size:0.84rem;font-weight:600;color:var(--ink-mute)">' + d.label + '</div>' +
        '<div style="flex:1;height:24px;background:var(--bg-3);border-radius:999px;overflow:hidden">' +
        '<div style="width:' + Math.round(d.value / max * 100) + '%;height:100%;background:' + d.color + ';border-radius:999px;transition:width .5s var(--ease)"></div>' +
        '</div>' +
        '<div style="width:52px;text-align:right;font-size:0.9rem;font-weight:800;color:var(--ink)">' + d.value + '%</div>' +
        '</div>';
    }).join('');
  }"""

new_chart = """  /* ────────────────────────── REPORTS ────────────────────────── */
  function sparkHtml(values, max) {
    max = max || Math.max.apply(null, values) || 1;
    return values.map(function (v) {
      var h = Math.max(8, Math.round(v / max * 100));
      return '<i style="height:' + h + '%"></i>';
    }).join('');
  }

  function renderChart() {
    var el = $('#barChart');
    if (!el) return;
    var data = [
      { label: 'Маркетплейс', value: 62, color: 'var(--terra)' },
      { label: 'WhatsApp', value: 24, color: 'var(--sage)' },
      { label: 'Telegram', value: 9, color: 'var(--plum)' },
      { label: 'MAX', value: 5, color: 'var(--amber)' }
    ];
    var max = 62;
    el.innerHTML = data.map(function (d) {
      return '<div style="display:flex;align-items:center;gap:14px">' +
        '<div style="width:110px;font-size:0.84rem;font-weight:600;color:var(--ink-mute)">' + d.label + '</div>' +
        '<div style="flex:1;height:24px;background:var(--bg-3);border-radius:999px;overflow:hidden">' +
        '<div style="width:' + Math.round(d.value / max * 100) + '%;height:100%;background:' + d.color + ';border-radius:999px;transition:width .5s var(--ease)"></div>' +
        '</div>' +
        '<div style="width:52px;text-align:right;font-size:0.9rem;font-weight:800;color:var(--ink)">' + d.value + '%</div>' +
        '</div>';
    }).join('');
  }

  function renderReports() {
    var revDays = [42, 55, 48, 61, 70, 88, 76];
    var ordDays = [11, 14, 12, 16, 18, 22, 19];
    var catVals = [34, 22, 18, 14, 12];
    var sr = $('#sparkRev');
    var so = $('#sparkOrd');
    var sc = $('#sparkCat');
    if (sr) sr.innerHTML = sparkHtml(revDays, 100);
    if (so) so.innerHTML = sparkHtml(ordDays, 24);
    if (sc) sc.innerHTML = sparkHtml(catVals, 40);

    var weekSum = revDays.reduce(function (a, b) { return a + b; }, 0) * 1000;
    setText('#anRev', fmtPrice(weekSum));
    setText('#anWeek', seed.length * 4);
    setText('#anAov', fmtPrice(Math.round((seed.reduce(function (s, x) { return s + x.price; }, 0)) / seed.length * 0.95)));
    setText('#anConv', '34%');
    setText('#anRet', '1.2%');
    var unread = chats.reduce(function (s, c) { return s + c.unread; }, 0);
    setText('#anUnreadRep', unread);

    var pills = $('#salesPills');
    if (pills) {
      pills.innerHTML =
        '<span>Пик: <b>сб 12–15</b></span>' +
        '<span>Лучший день: <b>суббота</b></span>' +
        '<span>План недели: <b>91%</b></span>' +
        '<span>Новые клиенты: <b>17</b></span>';
    }

    var funnel = $('#funnel');
    if (funnel) {
      var steps = [
        { l: 'Диалоги', v: 100, w: 100 },
        { l: 'Ответ', v: 86, w: 86 },
        { l: 'Корзина', v: 51, w: 51 },
        { l: 'Оплата', v: 34, w: 34 }
      ];
      funnel.innerHTML = steps.map(function (s) {
        return '<div class="step"><div class="lbl">' + s.l + '</div><div class="bar"><i style="width:' + s.w + '%"></i></div><div class="val">' + s.v + '%</div></div>';
      }).join('');
    }

    var shopTable = $('#shopTable');
    if (shopTable) {
      var shops = [
        ['Мира 14', '94', '318 400 ₽', '▲'],
        ['Ленина 92', '61', '204 100 ₽', '▲'],
        ['Рижская 8', '31', '98 700 ₽', '—']
      ];
      shopTable.innerHTML = '<tr><th>Точка</th><th class="num">Заказы</th><th class="num">Выручка</th><th class="num">Тренд</th></tr>' +
        shops.map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="num">' + r[3] + '</td></tr>';
        }).join('');
    }

    var heat = $('#heat');
    if (heat) {
      var days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'];
      var hours = ['10', '12', '14', '16', '18'];
      var levels = [
        [1,1,2,2,3,4,2],
        [1,2,2,3,3,4,3],
        [2,2,3,3,4,4,3],
        [1,2,2,3,3,4,2],
        [1,1,2,2,3,3,2]
      ];
      var html = '<div class="h"></div>' + days.map(function (d) { return '<div class="h">' + d + '</div>'; }).join('');
      hours.forEach(function (h, hi) {
        html += '<div class="h">' + h + '</div>';
        levels[hi].forEach(function (lv) {
          html += '<div class="c l' + lv + '" title="' + h + ':00"></div>';
        });
      });
      heat.innerHTML = html;
    }

    var prodTable = $('#prodTable');
    if (prodTable) {
      var prods = [
        ['Букет пионов, 15 шт.', '42', '134 400 ₽'],
        ['Сборный · роза + эустома', '31', '75 950 ₽'],
        ['Композиция «Нежность»', '18', '73 800 ₽'],
        ['Корзина «Счастье»', '9', '68 400 ₽'],
        ['Тюльпаны, 21 шт.', '27', '53 730 ₽']
      ];
      prodTable.innerHTML = '<tr><th>Товар</th><th class="num">Шт.</th><th class="num">Выручка</th></tr>' +
        prods.map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td></tr>';
        }).join('');
    }

    var catPills = $('#catPills');
    if (catPills) {
      catPills.innerHTML =
        '<span>Пионы <b>34%</b></span><span>Розы <b>22%</b></span><span>Сборные <b>18%</b></span><span>Корзины <b>14%</b></span><span>Прочее <b>12%</b></span>';
    }

    var courierTable = $('#courierTable');
    if (courierTable) {
      var crs = [
        ['Игорь', '7', '5', 'в слоте'],
        ['Аня', '6', '4', 'в пути'],
        ['Сергей', '5', '5', 'свободен']
      ];
      courierTable.innerHTML = '<tr><th>Курьер</th><th class="num">Рейсы</th><th class="num">Сдано</th><th>Статус</th></tr>' +
        crs.map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td><td>' + r[3] + '</td></tr>';
        }).join('');
    }

    var opsPills = $('#opsPills');
    if (opsPills) {
      var o = state.orders;
      var n = function (st) { return o.filter(function (x) { return x.status === st; }).length; };
      opsPills.innerHTML =
        '<span>Новые <b>' + n('new') + '</b></span>' +
        '<span>В сборке <b>' + n('assembled') + '</b></span>' +
        '<span>В доставке <b>' + n('delivering') + '</b></span>' +
        '<span>Готово <b>' + n('done') + '</b></span>';
    }

    renderChart();
  }"""

if old_chart not in text:
    raise SystemExit("chart block not found")
text = text.replace(old_chart, new_chart)

# updateStats still sets anWeek etc - keep. Add anRev if null-safe via setText.

# reset also call renderReports if needed
text = text.replace(
    "    renderChart();\n    if (termLog) {",
    "    renderChart();\n    renderReports();\n    if (termLog) {",
)

# bind report tabs + search
old_bind_chat = """    $('#chSend').addEventListener('click', sendMessage);
    $('#chInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendMessage(); });

    $('#chatSide').addEventListener('click', function (e) {
      var tab = e.target.closest('.chat-tab');
      if (tab) selectChat(tab.getAttribute('data-chat'));
    });"""

new_bind_chat = """    $('#chSend').addEventListener('click', sendMessage);
    $('#chInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') sendMessage(); });

    $('#chatSide').addEventListener('click', function (e) {
      var tab = e.target.closest('.chat-tab');
      if (tab) selectChat(tab.getAttribute('data-chat'));
    });

    var tgSearch = $('#tgSearch');
    if (tgSearch) tgSearch.addEventListener('input', renderChats);

    $$('.rep-tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        var id = tab.getAttribute('data-rep');
        $$('.rep-tab').forEach(function (t) { t.classList.toggle('on', t === tab); });
        $$('[data-rep-panel]').forEach(function (p) {
          p.classList.toggle('on', p.getAttribute('data-rep-panel') === id);
        });
      });
    });"""

if old_bind_chat not in text:
    raise SystemExit("bind chat block not found")
text = text.replace(old_bind_chat, new_bind_chat)

text = text.replace(
    "  renderChart();\n  bind();\n})();",
    "  renderChart();\n  renderReports();\n  bind();\n})();",
)

DEMO.write_text(text, encoding="utf-8")
print("patched", DEMO, "bytes", DEMO.stat().st_size)
