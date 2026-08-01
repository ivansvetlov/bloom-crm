# -*- coding: utf-8 -*-
"""Enrich analytics/reports section in demo.html"""
from pathlib import Path
import re

paths = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]

CSS_EXTRA = r"""
  .rep-head {
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
    gap: 12px; margin-bottom: 14px;
  }
  .rep-head h2 {
    font-size: 1.2rem; font-weight: 900; letter-spacing: -0.03em; margin: 0;
  }
  .rep-head .sub { font-size: 0.82rem; color: var(--ink-mute); margin-top: 2px; }
  .rep-period {
    display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
  }
  .rep-period button {
    border: 1px solid var(--border-2); background: var(--bg-2); color: var(--ink-mute);
    font-family: var(--font); font-size: 0.78rem; font-weight: 750;
    padding: 8px 12px; border-radius: 999px; cursor: pointer;
  }
  .rep-period button.on {
    background: var(--ink); border-color: var(--ink); color: #fff;
  }
  .rep-kpi-row {
    display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-bottom: 14px;
  }
  .rep-kpi {
    background: var(--bg-2); border: 1px solid var(--border); border-radius: 14px;
    padding: 14px 12px; box-shadow: var(--shadow-sm); min-width: 0;
  }
  .rep-kpi .l {
    font-size: 0.66rem; font-weight: 750; text-transform: uppercase; letter-spacing: 0.04em;
    color: var(--ink-faint); margin-bottom: 6px;
  }
  .rep-kpi .v {
    font-size: 1.2rem; font-weight: 900; letter-spacing: -0.03em; color: var(--ink);
    font-variant-numeric: tabular-nums;
  }
  .rep-kpi .d {
    font-size: 0.72rem; font-weight: 700; margin-top: 4px; color: var(--ink-mute);
  }
  .rep-kpi .d.up { color: var(--sage); }
  .rep-kpi .d.down { color: var(--red); }
  .rep-kpi .d.warn { color: #A07A20; }
  .spark-wrap { position: relative; }
  .spark-days {
    display: flex; justify-content: space-between; margin-top: 8px;
    font-size: 0.65rem; font-weight: 700; color: var(--ink-faint);
  }
  .rank-list { display: flex; flex-direction: column; gap: 10px; }
  .rank-row {
    display: grid; grid-template-columns: 22px 1fr auto; gap: 10px; align-items: center;
  }
  .rank-row .n {
    font-family: var(--mono); font-size: 0.72rem; font-weight: 800; color: var(--ink-faint);
  }
  .rank-row .nm { font-size: 0.84rem; font-weight: 750; color: var(--ink); }
  .rank-row .meta { font-size: 0.72rem; color: var(--ink-mute); margin-top: 2px; }
  .rank-bar {
    height: 8px; border-radius: 99px; background: var(--bg-3); overflow: hidden; margin-top: 6px;
  }
  .rank-bar i {
    display: block; height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, var(--terra), #f08a6a);
  }
  .rank-row .val {
    font-size: 0.84rem; font-weight: 800; color: var(--ink); text-align: right;
    font-variant-numeric: tabular-nums; white-space: nowrap;
  }
  .cmp-table td.pos { color: var(--sage); font-weight: 800; }
  .cmp-table td.neg { color: var(--red); font-weight: 800; }
  .split-metrics {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 4px;
  }
  .split-metrics .box {
    background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 12px;
  }
  .split-metrics .box .k { font-size: 0.7rem; font-weight: 750; color: var(--ink-faint); text-transform: uppercase; }
  .split-metrics .box .vv { font-size: 1.1rem; font-weight: 900; margin-top: 4px; }
  .donut-row {
    display: flex; align-items: center; gap: 18px; flex-wrap: wrap;
  }
  .donut {
    width: 120px; height: 120px; border-radius: 50%;
    background: conic-gradient(var(--terra) 0 62%, var(--sage) 62% 86%, var(--plum) 86% 95%, var(--amber) 95% 100%);
    position: relative; flex-shrink: 0;
  }
  .donut::after {
    content: ''; position: absolute; inset: 22px; border-radius: 50%; background: var(--bg-2);
  }
  .legend-list { display: flex; flex-direction: column; gap: 8px; flex: 1; min-width: 140px; }
  .legend-list .lg {
    display: flex; align-items: center; justify-content: space-between; gap: 10px;
    font-size: 0.82rem; font-weight: 700; color: var(--ink-dim);
  }
  .legend-list .dotc {
    width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 8px;
  }
  .alert-list { display: flex; flex-direction: column; gap: 8px; }
  .alert-item {
    display: flex; gap: 10px; align-items: flex-start; padding: 10px 12px;
    background: var(--bg); border: 1px solid var(--border); border-radius: 12px;
    font-size: 0.84rem; color: var(--ink-dim); line-height: 1.4;
  }
  .alert-item b { color: var(--ink); }
  .alert-item .tag {
    font-size: 0.65rem; font-weight: 800; padding: 2px 7px; border-radius: 999px;
    background: var(--amber-soft); color: #A07A20; flex-shrink: 0; margin-top: 2px;
  }
  .alert-item .tag.bad { background: var(--red-soft); color: var(--red); }
  .alert-item .tag.ok { background: var(--sage-soft); color: var(--sage); }
  @media (max-width: 1100px) {
    .rep-kpi-row { grid-template-columns: repeat(3, 1fr); }
    .rep-grid-3 { grid-template-columns: 1fr; }
  }
  @media (max-width: 700px) {
    .rep-kpi-row { grid-template-columns: repeat(2, 1fr); }
    .rep-grid-2 { grid-template-columns: 1fr; }
  }
"""

SECTION = r'''
 <!-- ═════════════ 04 · REPORTS ═════════════ -->
 <section data-section="analytics" style="display:none">
 <div class="rep-head">
 <div>
 <h2>Отчёты</h2>
 <div class="sub">Сеть · продажи, точки, каналы, операции, жалобы</div>
 </div>
 <div class="rep-period" id="repPeriod">
 <button type="button" data-period="today">Сегодня</button>
 <button type="button" data-period="7d" class="on">7 дней</button>
 <button type="button" data-period="30d">30 дней</button>
 <button type="button" data-period="peak">Пик (8 Марта)</button>
 </div>
 </div>

 <div class="rep-tabs" id="repTabs">
 <button type="button" class="rep-tab on" data-rep="overview">Сводка</button>
 <button type="button" class="rep-tab" data-rep="sales">Продажи</button>
 <button type="button" class="rep-tab" data-rep="channels">Каналы</button>
 <button type="button" class="rep-tab" data-rep="shops">Точки</button>
 <button type="button" class="rep-tab" data-rep="products">Товары</button>
 <button type="button" class="rep-tab" data-rep="ops">Операции</button>
 <button type="button" class="rep-tab" data-rep="clients">Клиенты</button>
 <button type="button" class="rep-tab" data-rep="quality">Качество</button>
 </div>

 <!-- OVERVIEW -->
 <div class="rep-panel on" data-rep-panel="overview">
 <div class="rep-kpi-row" id="ovKpis"></div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Выручка по дням <em id="ovRevLabel">7 дней</em></h3>
 <div class="spark-wrap">
 <div class="spark" id="ovSparkRev"></div>
 <div class="spark-days" id="ovSparkDays"></div>
 </div>
 </div>
 <div class="rep-card">
 <h3>Где деньги <em>каналы</em></h3>
 <div class="donut-row">
 <div class="donut" id="ovDonut"></div>
 <div class="legend-list" id="ovChannelLegend"></div>
 </div>
 </div>
 </div>
 <div class="rep-grid-3">
 <div class="rep-card">
 <h3>Точки · топ</h3>
 <div class="rank-list" id="ovShopRank"></div>
 </div>
 <div class="rep-card">
 <h3>Товары · топ выручки</h3>
 <div class="rank-list" id="ovProdRank"></div>
 </div>
 <div class="rep-card">
 <h3>На что смотреть</h3>
 <div class="alert-list" id="ovAlerts"></div>
 </div>
 </div>
 </div>

 <!-- SALES -->
 <div class="rep-panel" data-rep-panel="sales">
 <div class="rep-kpi-row" id="salesKpis"></div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Выручка <em>по дням</em></h3>
 <div class="spark" id="sparkRev"></div>
 <div class="spark-days" id="sparkRevDays"></div>
 </div>
 <div class="rep-card">
 <h3>Заказы <em>шт.</em></h3>
 <div class="spark sage" id="sparkOrd"></div>
 <div class="spark-days" id="sparkOrdDays"></div>
 </div>
 </div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>План / факт <em>неделя</em></h3>
 <div class="split-metrics" id="salesPlan"></div>
 <div class="pill-row" id="salesPills" style="margin-top:12px"></div>
 </div>
 <div class="rep-card">
 <h3>Сравнение с прошлой неделей</h3>
 <table class="tbl cmp-table" id="salesCmp"></table>
 </div>
 </div>
 <div class="rep-card">
 <h3>Выручка по оплате</h3>
 <div id="payBars" style="display:flex;flex-direction:column;gap:12px"></div>
 </div>
 </div>

 <!-- CHANNELS -->
 <div class="rep-panel" data-rep-panel="channels">
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Откуда заказы <em>доля</em></h3>
 <div id="barChart" style="display:flex;flex-direction:column;gap:14px"></div>
 </div>
 <div class="rep-card">
 <h3>Воронка: диалог → оплата</h3>
 <div class="funnel" id="funnel"></div>
 </div>
 </div>
 <div class="rep-kpi-row" style="grid-template-columns:repeat(4,1fr)" id="chKpis"></div>
 <div class="rep-card">
 <h3>Каналы · детально</h3>
 <table class="tbl" id="channelTable"></table>
 </div>
 </div>

 <!-- SHOPS -->
 <div class="rep-panel" data-rep-panel="shops">
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Точки · рейтинг</h3>
 <table class="tbl" id="shopTable"></table>
 </div>
 <div class="rep-card">
 <h3>Нагрузка <em>день × час</em></h3>
 <div class="heat" id="heat"></div>
 </div>
 </div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Сравнение точек</h3>
 <div class="rank-list" id="shopCompare"></div>
 </div>
 <div class="rep-card">
 <h3>Загрузка флористов <em>сегодня</em></h3>
 <table class="tbl" id="floristTable"></table>
 </div>
 </div>
 </div>

 <!-- PRODUCTS -->
 <div class="rep-panel" data-rep-panel="products">
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Топ букетов <em>выручка</em></h3>
 <table class="tbl" id="prodTable"></table>
 </div>
 <div class="rep-card">
 <h3>Категории <em>доля</em></h3>
 <div class="spark plum" id="sparkCat" style="height:120px;margin-bottom:12px"></div>
 <div class="pill-row" id="catPills"></div>
 </div>
 </div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Остатки · риски</h3>
 <table class="tbl" id="stockRiskTable"></table>
 </div>
 <div class="rep-card">
 <h3>Что заканчивается</h3>
 <div class="alert-list" id="stockAlerts"></div>
 </div>
 </div>
 </div>

 <!-- OPS -->
 <div class="rep-panel" data-rep-panel="ops">
 <div class="rep-kpi-row" style="grid-template-columns:repeat(4,1fr)" id="opsKpis"></div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Курьеры · сегодня</h3>
 <table class="tbl" id="courierTable"></table>
 </div>
 <div class="rep-card">
 <h3>Статусы заказов <em>сейчас</em></h3>
 <div class="pill-row" id="opsPills"></div>
 <div style="margin-top:14px" id="opsStatusBars"></div>
 </div>
 </div>
 <div class="rep-card">
 <h3>SLA сборки и доставки</h3>
 <table class="tbl" id="slaTable"></table>
 </div>
 </div>

 <!-- CLIENTS -->
 <div class="rep-panel" data-rep-panel="clients">
 <div class="rep-kpi-row" style="grid-template-columns:repeat(4,1fr)" id="cliKpis"></div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Новые vs повторные</h3>
 <div class="split-metrics" id="cliSplit"></div>
 <div class="rank-list" id="cliSegment" style="margin-top:14px"></div>
 </div>
 <div class="rep-card">
 <h3>VIP · топ по сумме</h3>
 <table class="tbl" id="vipTable"></table>
 </div>
 </div>
 <div class="rep-card">
 <h3>Кого позвать снова <em>давно не заказывали</em></h3>
 <table class="tbl" id="winbackTable"></table>
 </div>
 </div>

 <!-- QUALITY -->
 <div class="rep-panel" data-rep-panel="quality">
 <div class="rep-kpi-row" style="grid-template-columns:repeat(4,1fr)" id="qKpis"></div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Обращения по типу</h3>
 <div class="rank-list" id="qTypeRank"></div>
 </div>
 <div class="rep-card">
 <h3>Причины жалоб</h3>
 <table class="tbl" id="qReasonTable"></table>
 </div>
 </div>
 <div class="rep-grid-2">
 <div class="rep-card">
 <h3>Открытые кейсы</h3>
 <table class="tbl" id="qOpenTable"></table>
 </div>
 <div class="rep-card">
 <h3>Качество по точкам</h3>
 <table class="tbl" id="qShopTable"></table>
 </div>
 </div>
 </div>
 </section>
'''

JS = r'''
  /* ────────────────────────── REPORTS ────────────────────────── */
  var repPeriod = '7d';
  var DAYS7 = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'];

  function sparkHtml(values, max) {
    max = max || Math.max.apply(null, values) || 1;
    return values.map(function (v) {
      var h = Math.max(8, Math.round(v / max * 100));
      return '<i style="height:' + h + '%" title="' + v + '"></i>';
    }).join('');
  }

  function barRow(label, value, max, color) {
    color = color || 'var(--terra)';
    var pct = Math.max(2, Math.round(value / (max || 1) * 100));
    return '<div style="display:flex;align-items:center;gap:12px">' +
      '<div style="width:120px;font-size:0.84rem;font-weight:700;color:var(--ink-mute)">' + esc(label) + '</div>' +
      '<div style="flex:1;height:22px;background:var(--bg-3);border-radius:999px;overflow:hidden">' +
      '<div style="width:' + pct + '%;height:100%;background:' + color + ';border-radius:999px"></div></div>' +
      '<div style="width:64px;text-align:right;font-weight:800">' + value + (value <= 100 && String(label).indexOf('%') < 0 ? '' : '') + '</div></div>';
  }

  function rankHtml(items) {
    var max = 0;
    items.forEach(function (it) { if (it.w > max) max = it.w; });
    return items.map(function (it, i) {
      var pct = Math.max(4, Math.round(it.w / (max || 1) * 100));
      return '<div class="rank-row">' +
        '<div class="n">' + String(i + 1).padStart(2, '0') + '</div>' +
        '<div><div class="nm">' + esc(it.n) + '</div>' +
        (it.m ? '<div class="meta">' + esc(it.m) + '</div>' : '') +
        '<div class="rank-bar"><i style="width:' + pct + '%;background:' + (it.c || 'linear-gradient(90deg,var(--terra),#f08a6a)') + '"></i></div></div>' +
        '<div class="val">' + esc(it.v) + '</div></div>';
    }).join('');
  }

  function periodMult() {
    if (repPeriod === 'today') return 0.18;
    if (repPeriod === '30d') return 3.8;
    if (repPeriod === 'peak') return 2.4;
    return 1;
  }

  function periodLabel() {
    return ({ today: 'сегодня', '7d': '7 дней', '30d': '30 дней', peak: 'пик 8 Марта' })[repPeriod] || '7 дней';
  }

  function liveOrdersAgg() {
    var o = shopFilter(state.orders);
    var byCh = { wa: 0, tg: 0, max: 0, fw: 0, phone: 0, walk: 0 };
    var byShop = {};
    var byPay = { paid: 0, pending: 0, cod: 0 };
    var bySt = { new: 0, accepted: 0, assembled: 0, delivering: 0, done: 0 };
    var rev = 0;
    o.forEach(function (x) {
      byCh[x.channel] = (byCh[x.channel] || 0) + 1;
      byShop[x.shop] = byShop[x.shop] || { n: 0, r: 0 };
      byShop[x.shop].n++;
      byShop[x.shop].r += x.price || 0;
      var pay = x.pay || (x.channel === 'fw' ? 'paid' : 'pending');
      byPay[pay] = (byPay[pay] || 0) + (x.price || 0);
      bySt[x.status] = (bySt[x.status] || 0) + 1;
      rev += x.price || 0;
    });
    return { o: o, byCh: byCh, byShop: byShop, byPay: byPay, bySt: bySt, rev: rev, n: o.length };
  }

  function renderChart() {
    var el = $('#barChart');
    if (!el) return;
    var m = periodMult();
    var data = [
      { label: 'Маркетплейс', value: Math.round(62 * m), color: 'var(--terra)' },
      { label: 'WhatsApp', value: Math.round(24 * m), color: 'var(--sage)' },
      { label: 'Telegram', value: Math.round(9 * m), color: 'var(--plum)' },
      { label: 'MAX', value: Math.round(5 * m), color: 'var(--amber)' }
    ];
    // normalize to % for share chart
    var sum = data.reduce(function (a, d) { return a + d.value; }, 0) || 1;
    var max = 100;
    el.innerHTML = data.map(function (d) {
      var pct = Math.round(d.value / sum * 100);
      return '<div style="display:flex;align-items:center;gap:14px">' +
        '<div style="width:110px;font-size:0.84rem;font-weight:600;color:var(--ink-mute)">' + d.label + '</div>' +
        '<div style="flex:1;height:24px;background:var(--bg-3);border-radius:999px;overflow:hidden">' +
        '<div style="width:' + pct + '%;height:100%;background:' + d.color + ';border-radius:999px"></div></div>' +
        '<div style="width:52px;text-align:right;font-size:0.9rem;font-weight:800;color:var(--ink)">' + pct + '%</div></div>';
    }).join('');
  }

  function renderReports() {
    var m = periodMult();
    var live = liveOrdersAgg();
    var revDays = [42, 55, 48, 61, 70, 88, 76].map(function (v) { return Math.round(v * m * 10) / 10; });
    var ordDays = [11, 14, 12, 16, 18, 22, 19].map(function (v) { return Math.max(1, Math.round(v * m)); });
    var weekSum = Math.round(revDays.reduce(function (a, b) { return a + b; }, 0) * 1000);
    var weekOrd = ordDays.reduce(function (a, b) { return a + b; }, 0);
    var aov = weekOrd ? Math.round(weekSum / weekOrd) : 0;
    var pl = periodLabel();

    // period buttons
    $$('#repPeriod button').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-period') === repPeriod);
    });
    var ovLab = $('#ovRevLabel');
    if (ovLab) ovLab.textContent = pl;

    // ── Overview KPIs
    var ov = $('#ovKpis');
    if (ov) {
      ov.innerHTML =
        kpi('Выручка', fmtPrice(weekSum), '▲ 9% к прошлому', 'up') +
        kpi('Заказы', String(weekOrd), '▲ 12%', 'up') +
        kpi('Средний чек', fmtPrice(aov), '▲ 4%', 'up') +
        kpi('Повторные', '28%', '▲ 3 п.п.', 'up') +
        kpi('Открытые чаты', String(chats.filter(function (c) { return (c.status || 'open') !== 'resolved'; }).length), unreadHint(), unreadHint().indexOf('ответ') >= 0 ? 'warn' : 'up') +
        kpi('Жалобы открыты', String(cases.filter(function (c) { return c.status !== 'closed'; }).length), 'нужен разбор', 'warn');
    }
    function kpi(l, v, d, cls) {
      return '<div class="rep-kpi"><div class="l">' + l + '</div><div class="v">' + v + '</div><div class="d ' + (cls || '') + '">' + d + '</div></div>';
    }
    function unreadHint() {
      var u = chats.reduce(function (s, c) { return s + (c.unread || 0); }, 0);
      return u ? u + ' ждут ответа' : 'всё прочитано';
    }

    var osr = $('#ovSparkRev');
    if (osr) osr.innerHTML = sparkHtml(revDays, 100 * m);
    var osd = $('#ovSparkDays');
    if (osd) osd.innerHTML = DAYS7.map(function (d) { return '<span>' + d + '</span>'; }).join('');

    var leg = $('#ovChannelLegend');
    if (leg) {
      leg.innerHTML =
        lg('#E06B4A', 'Маркетплейс', '62%') +
        lg('#6F8F72', 'WhatsApp', '24%') +
        lg('#7A5A74', 'Telegram', '9%') +
        lg('#D9A441', 'MAX', '5%');
    }
    function lg(c, n, v) {
      return '<div class="lg"><span><span class="dotc" style="background:' + c + '"></span>' + n + '</span><b>' + v + '</b></div>';
    }
    var don = $('#ovDonut');
    if (don) {
      don.style.background = 'conic-gradient(var(--terra) 0 62%, var(--sage) 62% 86%, var(--plum) 86% 95%, var(--amber) 95% 100%)';
    }

    var ovShop = $('#ovShopRank');
    if (ovShop) {
      ovShop.innerHTML = rankHtml([
        { n: 'Мира 14', m: '94 заказа', v: fmtPrice(Math.round(318400 * m)), w: 94 },
        { n: 'Ленина 92', m: '61 заказ', v: fmtPrice(Math.round(204100 * m)), w: 61 },
        { n: 'Рижская 8', m: '31 заказ', v: fmtPrice(Math.round(98700 * m)), w: 31 }
      ]);
    }
    var ovProd = $('#ovProdRank');
    if (ovProd) {
      ovProd.innerHTML = rankHtml([
        { n: 'Букет пионов, 15 шт.', m: '42 шт.', v: fmtPrice(Math.round(134400 * m)), w: 42 },
        { n: 'Сборный · роза + эустома', m: '31 шт.', v: fmtPrice(Math.round(75950 * m)), w: 31 },
        { n: 'Композиция «Нежность»', m: '18 шт.', v: fmtPrice(Math.round(73800 * m)), w: 18 }
      ]);
    }
    var ovAl = $('#ovAlerts');
    if (ovAl) {
      var openCases = cases.filter(function (c) { return c.status !== 'closed'; }).length;
      var lowStock = products.filter(function (p) { return p.stock > 0 && p.stock <= 3; }).length;
      var unread = chats.reduce(function (s, c) { return s + (c.unread || 0); }, 0);
      ovAl.innerHTML =
        al(openCases ? 'bad' : 'ok', openCases ? 'Жалобы' : 'Ок', openCases ? '<b>' + openCases + '</b> открытых обращений' : 'Нет открытых жалоб') +
        al(lowStock ? 'warn' : 'ok', lowStock ? 'Склад' : 'Ок', lowStock ? '<b>' + lowStock + '</b> позиции с низким остатком' : 'Остатки в норме') +
        al(unread ? 'warn' : 'ok', unread ? 'Чаты' : 'Ок', unread ? '<b>' + unread + '</b> непрочитанных' : 'Чаты разобраны') +
        al('ok', 'Пик', 'Суббота 12–15 — держать смену');
    }
    function al(tag, t, html) {
      return '<div class="alert-item"><span class="tag ' + tag + '">' + t + '</span><div>' + html + '</div></div>';
    }

    // ── Sales
    var sk = $('#salesKpis');
    if (sk) {
      sk.innerHTML =
        kpi('Выручка', fmtPrice(weekSum), '▲ 9%', 'up') +
        kpi('Заказы', String(weekOrd), '▲ 12%', 'up') +
        kpi('Средний чек', fmtPrice(aov), '▲ 4%', 'up') +
        kpi('Оплачено', fmtPrice(Math.round(weekSum * 0.71)), '71% выручки', '') +
        kpi('Ожидает оплаты', fmtPrice(Math.round(weekSum * 0.18)), 'в работе', 'warn') +
        kpi('Отмены', '2.1%', 'без всплеска', '');
    }
    var sr = $('#sparkRev');
    var so = $('#sparkOrd');
    if (sr) sr.innerHTML = sparkHtml(revDays, 100 * Math.max(m, 1));
    if (so) so.innerHTML = sparkHtml(ordDays, 24 * Math.max(m, 1));
    var srd = $('#sparkRevDays');
    var sod = $('#sparkOrdDays');
    if (srd) srd.innerHTML = DAYS7.map(function (d) { return '<span>' + d + '</span>'; }).join('');
    if (sod) sod.innerHTML = DAYS7.map(function (d) { return '<span>' + d + '</span>'; }).join('');

    var plan = $('#salesPlan');
    if (plan) {
      var planV = Math.round(480000 * m);
      var fact = weekSum;
      var pct = Math.min(100, Math.round(fact / planV * 100));
      plan.innerHTML =
        '<div class="box"><div class="k">План</div><div class="vv">' + fmtPrice(planV) + '</div></div>' +
        '<div class="box"><div class="k">Факт</div><div class="vv">' + fmtPrice(fact) + '</div></div>' +
        '<div class="box" style="grid-column:1/-1"><div class="k">Выполнение</div>' +
        '<div class="rank-bar" style="height:12px;margin-top:8px"><i style="width:' + pct + '%"></i></div>' +
        '<div class="vv" style="margin-top:8px">' + pct + '%</div></div>';
    }
    var pills = $('#salesPills');
    if (pills) {
      pills.innerHTML =
        '<span>Пик: <b>сб 12–15</b></span>' +
        '<span>Лучший день: <b>суббота</b></span>' +
        '<span>Новые клиенты: <b>' + Math.round(17 * m) + '</b></span>' +
        '<span>Период: <b>' + pl + '</b></span>';
    }
    var cmp = $('#salesCmp');
    if (cmp) {
      cmp.innerHTML =
        '<tr><th>Метрика</th><th class="num">Сейчас</th><th class="num">Прошлая</th><th class="num">Δ</th></tr>' +
        rowCmp('Выручка', fmtPrice(weekSum), fmtPrice(Math.round(weekSum / 1.09)), '+9%', true) +
        rowCmp('Заказы', String(weekOrd), String(Math.round(weekOrd / 1.12)), '+12%', true) +
        rowCmp('Средний чек', fmtPrice(aov), fmtPrice(Math.round(aov / 1.04)), '+4%', true) +
        rowCmp('Отмены', '2.1%', '2.4%', '−0.3 п.п.', true);
    }
    function rowCmp(m, a, b, d, pos) {
      return '<tr><td><b>' + m + '</b></td><td class="num">' + a + '</td><td class="num">' + b + '</td><td class="num ' + (pos ? 'pos' : 'neg') + '">' + d + '</td></tr>';
    }
    var payB = $('#payBars');
    if (payB) {
      var maxP = Math.max(live.byPay.paid || 1, live.byPay.pending || 1, live.byPay.cod || 1, weekSum * 0.5);
      // blend live + demo
      var paid = Math.round(weekSum * 0.71);
      var pend = Math.round(weekSum * 0.18);
      var cod = Math.round(weekSum * 0.11);
      payB.innerHTML =
        barRow('Оплачено', paid, weekSum, 'var(--sage)') +
        barRow('Ожидает', pend, weekSum, 'var(--amber)') +
        barRow('При получении', cod, weekSum, 'var(--plum)');
      // show as money labels
      payB.innerHTML =
        moneyBar('Оплачено', paid, weekSum, 'var(--sage)') +
        moneyBar('Ожидает', pend, weekSum, '#D9A441') +
        moneyBar('При получении', cod, weekSum, 'var(--plum)');
    }
    function moneyBar(label, val, max, color) {
      var pct = Math.max(2, Math.round(val / (max || 1) * 100));
      return '<div style="display:flex;align-items:center;gap:12px">' +
        '<div style="width:130px;font-size:0.84rem;font-weight:700;color:var(--ink-mute)">' + label + '</div>' +
        '<div style="flex:1;height:22px;background:var(--bg-3);border-radius:999px;overflow:hidden">' +
        '<div style="width:' + pct + '%;height:100%;background:' + color + ';border-radius:999px"></div></div>' +
        '<div style="width:100px;text-align:right;font-weight:800">' + fmtPrice(val) + '</div></div>';
    }

    // ── Channels
    var chK = $('#chKpis');
    if (chK) {
      chK.innerHTML =
        kpi('Из чата в заказ', '34%', '▲ чуть выше', 'up') +
        kpi('Ответ < 3 мин', '81%', 'SLA ок', 'up') +
        kpi('Непрочитанные', String(chats.reduce(function (s, c) { return s + (c.unread || 0); }, 0)), 'нужен ответ', 'warn') +
        kpi('Возвраты', '1.2%', 'спокойно', '');
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
    var chT = $('#channelTable');
    if (chT) {
      var rows = [
        ['Маркетплейс', Math.round(62 * m), fmtPrice(Math.round(weekSum * 0.58)), '3 100 ₽', '2.4%'],
        ['WhatsApp', Math.round(24 * m), fmtPrice(Math.round(weekSum * 0.24)), '2 800 ₽', '1.1%'],
        ['Telegram', Math.round(9 * m), fmtPrice(Math.round(weekSum * 0.11)), '2 600 ₽', '0.8%'],
        ['MAX', Math.round(5 * m), fmtPrice(Math.round(weekSum * 0.07)), '2 400 ₽', '0.5%']
      ];
      chT.innerHTML = '<tr><th>Канал</th><th class="num">Заказы</th><th class="num">Выручка</th><th class="num">Ср. чек</th><th class="num">Отмены</th></tr>' +
        rows.map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="num">' + r[3] + '</td><td class="num">' + r[4] + '</td></tr>';
        }).join('');
    }

    // ── Shops
    var shopTable = $('#shopTable');
    if (shopTable) {
      var shops = [
        ['Мира 14', String(Math.round(94 * m)), fmtPrice(Math.round(318400 * m)), '38 м', '96%', '▲'],
        ['Ленина 92', String(Math.round(61 * m)), fmtPrice(Math.round(204100 * m)), '41 м', '92%', '▲'],
        ['Рижская 8', String(Math.round(31 * m)), fmtPrice(Math.round(98700 * m)), '45 м', '88%', '—']
      ];
      shopTable.innerHTML = '<tr><th>Точка</th><th class="num">Заказы</th><th class="num">Выручка</th><th class="num">Сборка</th><th class="num">В слот</th><th class="num">Тренд</th></tr>' +
        shops.map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="num">' + r[3] + '</td><td class="num">' + r[4] + '</td><td class="num pos">' + r[5] + '</td></tr>';
        }).join('');
    }
    var heat = $('#heat');
    if (heat) {
      var days = DAYS7;
      var hours = ['10', '12', '14', '16', '18', '20'];
      var levels = [
        [1, 1, 2, 2, 3, 4, 2],
        [1, 2, 2, 3, 3, 4, 3],
        [2, 2, 3, 3, 4, 4, 3],
        [1, 2, 2, 3, 3, 4, 2],
        [1, 1, 2, 2, 3, 3, 2],
        [1, 1, 1, 2, 2, 3, 2]
      ];
      var html = '<div class="h"></div>' + days.map(function (d) { return '<div class="h">' + d + '</div>'; }).join('');
      hours.forEach(function (h, hi) {
        html += '<div class="h">' + h + '</div>';
        levels[hi].forEach(function (lv) {
          html += '<div class="c l' + lv + '" title="' + h + ':00"></div>';
        });
      });
      heat.innerHTML = html;
      heat.style.gridTemplateColumns = '48px repeat(7, 1fr)';
    }
    var scmp = $('#shopCompare');
    if (scmp) {
      scmp.innerHTML = rankHtml([
        { n: 'Мира 14', m: 'выручка доля', v: '51%', w: 51 },
        { n: 'Ленина 92', m: 'выручка доля', v: '33%', w: 33 },
        { n: 'Рижская 8', m: 'выручка доля', v: '16%', w: 16 }
      ]);
    }
    var fl = $('#floristTable');
    if (fl) {
      fl.innerHTML = '<tr><th>Флорист</th><th>Точка</th><th class="num">В сборке</th><th class="num">Сдано</th><th>Нагрузка</th></tr>' +
        [
          ['Света П.', 'Ленина 92', '3', '7', 'высокая'],
          ['Анна К.', 'Мира 14', '2', '9', 'норма'],
          ['Игорь М.', 'Мира 14', '1', '5', 'свободно']
        ].map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td>' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="num">' + r[3] + '</td><td>' + r[4] + '</td></tr>';
        }).join('');
    }

    // ── Products
    var prodTable = $('#prodTable');
    if (prodTable) {
      var prods = [
        ['Букет пионов, 15 шт.', String(Math.round(42 * m)), fmtPrice(Math.round(134400 * m)), '12'],
        ['Сборный · роза + эустома', String(Math.round(31 * m)), fmtPrice(Math.round(75950 * m)), '4'],
        ['Композиция «Нежность»', String(Math.round(18 * m)), fmtPrice(Math.round(73800 * m)), '2'],
        ['Корзина «Счастье»', String(Math.round(9 * m)), fmtPrice(Math.round(68400 * m)), '1'],
        ['Тюльпаны, 21 шт.', String(Math.round(27 * m)), fmtPrice(Math.round(53730 * m)), '28']
      ];
      prodTable.innerHTML = '<tr><th>Товар</th><th class="num">Продано</th><th class="num">Выручка</th><th class="num">Остаток</th></tr>' +
        prods.map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="num">' + r[3] + '</td></tr>';
        }).join('');
    }
    var sc = $('#sparkCat');
    if (sc) sc.innerHTML = sparkHtml([34, 22, 18, 14, 12], 40);
    var catPills = $('#catPills');
    if (catPills) {
      catPills.innerHTML =
        '<span>Пионы <b>34%</b></span><span>Розы <b>22%</b></span><span>Сборные <b>18%</b></span><span>Корзины <b>14%</b></span><span>Прочее <b>12%</b></span>';
    }
    var srt = $('#stockRiskTable');
    if (srt) {
      var risks = products.filter(function (p) { return p.stock <= 3; }).slice(0, 6);
      srt.innerHTML = '<tr><th>SKU</th><th>Товар</th><th class="num">Остаток</th><th>Статус</th></tr>' +
        (risks.length ? risks.map(function (p) {
          var st = p.stock <= 0 ? 'нет' : 'мало';
          return '<tr><td class="num" style="text-align:left;font-family:var(--mono);font-size:0.78rem">' + esc(p.code) + '</td><td><b>' + esc(p.name) + '</b></td><td class="num">' + p.stock + '</td><td>' + st + '</td></tr>';
        }).join('') : '<tr><td colspan="4" style="color:var(--ink-faint)">Рисков нет</td></tr>');
    }
    var sa = $('#stockAlerts');
    if (sa) {
      var lows = products.filter(function (p) { return p.stock > 0 && p.stock <= 3; });
      var outs = products.filter(function (p) { return p.stock <= 0; });
      sa.innerHTML =
        al(outs.length ? 'bad' : 'ok', 'Нет', outs.length ? '<b>' + outs.length + '</b>: ' + outs.map(function (p) { return p.name; }).slice(0, 2).join(', ') : 'Нулевых позиций нет') +
        al(lows.length ? 'warn' : 'ok', 'Мало', lows.length ? '<b>' + lows.length + '</b> SKU ≤ 3 шт.' : 'Всё с запасом') +
        al('ok', 'Хаб', 'Утренние перемещения в норме');
    }

    // ── Ops
    var ok = $('#opsKpis');
    if (ok) {
      ok.innerHTML =
        kpi('Собрано вовремя', '94%', 'норма', 'up') +
        kpi('Ср. сборка', '38 м', '−4 мин', 'up') +
        kpi('Доставка в слот', '91%', '▲ 2 п.п.', 'up') +
        kpi('Отмены', '2.1%', 'без всплеска', '');
    }
    var courierTable = $('#courierTable');
    if (courierTable) {
      var crs = [
        ['Игорь', 'Мира 14', '7', '5', 'в слоте'],
        ['Аня', 'Ленина 92', '6', '4', 'в пути'],
        ['Сергей', 'Рижская 8', '5', '5', 'свободен']
      ];
      courierTable.innerHTML = '<tr><th>Курьер</th><th>Зона</th><th class="num">Рейсы</th><th class="num">Сдано</th><th>Статус</th></tr>' +
        crs.map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td>' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="num">' + r[3] + '</td><td>' + r[4] + '</td></tr>';
        }).join('');
    }
    var opsPills = $('#opsPills');
    if (opsPills) {
      var n = function (st) { return live.bySt[st] || 0; };
      opsPills.innerHTML =
        '<span>Новые <b>' + n('new') + '</b></span>' +
        '<span>Приняты <b>' + n('accepted') + '</b></span>' +
        '<span>Сборка <b>' + n('assembled') + '</b></span>' +
        '<span>В доставке <b>' + n('delivering') + '</b></span>' +
        '<span>Готово <b>' + n('done') + '</b></span>';
    }
    var osb = $('#opsStatusBars');
    if (osb) {
      var total = Math.max(1, live.n);
      osb.innerHTML =
        moneyBar('Новые', (live.bySt.new || 0), total, 'var(--terra)') +
        moneyBar('В работе', (live.bySt.accepted || 0) + (live.bySt.assembled || 0), total, 'var(--plum)') +
        moneyBar('Доставка', (live.bySt.delivering || 0), total, '#D9A441') +
        moneyBar('Готово', (live.bySt.done || 0), total, 'var(--sage)');
      // fix labels to counts not money - reuse structure with count
      osb.innerHTML =
        countBar('Новые', live.bySt.new || 0, total, 'var(--terra)') +
        countBar('Приняты + сборка', (live.bySt.accepted || 0) + (live.bySt.assembled || 0), total, 'var(--plum)') +
        countBar('В доставке', live.bySt.delivering || 0, total, '#D9A441') +
        countBar('Доставлено', live.bySt.done || 0, total, 'var(--sage)');
    }
    function countBar(label, val, max, color) {
      var pct = Math.max(2, Math.round(val / (max || 1) * 100));
      return '<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">' +
        '<div style="width:140px;font-size:0.82rem;font-weight:700;color:var(--ink-mute)">' + label + '</div>' +
        '<div style="flex:1;height:18px;background:var(--bg-3);border-radius:999px;overflow:hidden">' +
        '<div style="width:' + pct + '%;height:100%;background:' + color + ';border-radius:999px"></div></div>' +
        '<div style="width:36px;text-align:right;font-weight:800">' + val + '</div></div>';
    }
    var sla = $('#slaTable');
    if (sla) {
      sla.innerHTML = '<tr><th>Метрика</th><th class="num">Факт</th><th class="num">Цель</th><th>Статус</th></tr>' +
        [
          ['Ответ в чате', '2.4 мин', '≤ 3 мин', 'ок'],
          ['Сборка', '38 мин', '≤ 45 мин', 'ок'],
          ['Выезд курьера', '12 мин', '≤ 15 мин', 'ок'],
          ['Доставка в слот', '91%', '≥ 90%', 'ок'],
          ['Закрытие жалобы', '6.5 ч', '≤ 8 ч', 'ок']
        ].map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="pos">' + r[3] + '</td></tr>';
        }).join('');
    }

    // ── Clients
    var ck = $('#cliKpis');
    if (ck) {
      ck.innerHTML =
        kpi('Клиентов в базе', String(clients.length * 120 + 840), 'сеть', '') +
        kpi('Новые · период', String(Math.round(17 * m)), '▲', 'up') +
        kpi('Повторные', '28%', '▲ 3 п.п.', 'up') +
        kpi('Средний LTV', '7 400 ₽', 'оценка', '');
    }
    var cs = $('#cliSplit');
    if (cs) {
      cs.innerHTML =
        '<div class="box"><div class="k">Новые</div><div class="vv">72%</div></div>' +
        '<div class="box"><div class="k">Повторные</div><div class="vv">28%</div></div>';
    }
    var cseg = $('#cliSegment');
    if (cseg) {
      cseg.innerHTML = rankHtml([
        { n: 'VIP (3+ заказа)', m: 'доля выручки', v: '41%', w: 41 },
        { n: 'Постоянные (2)', m: 'доля выручки', v: '27%', w: 27 },
        { n: 'Новые (1)', m: 'доля выручки', v: '32%', w: 32 }
      ]);
    }
    var vip = $('#vipTable');
    if (vip) {
      var top = clients.map(function (c) {
        var st = clientStats(c);
        return { c: c, sum: st.sum, n: st.count };
      }).sort(function (a, b) { return b.sum - a.sum; }).slice(0, 5);
      vip.innerHTML = '<tr><th>Клиент</th><th>Точка</th><th class="num">Заказы</th><th class="num">Сумма</th></tr>' +
        top.map(function (x) {
          return '<tr><td><b>' + esc(x.c.name) + '</b></td><td>' + esc(x.c.shop) + '</td><td class="num">' + x.n + '</td><td class="num">' + fmtPrice(x.sum) + '</td></tr>';
        }).join('');
    }
    var wb = $('#winbackTable');
    if (wb) {
      wb.innerHTML = '<tr><th>Клиент</th><th>Канал</th><th>Последний контакт</th><th>Действие</th></tr>' +
        [
          ['Ольга', 'Маркетплейс', '18 дней', 'Написать'],
          ['Алексей', 'Telegram', '12 дней', 'Написать'],
          ['Ирина', 'Маркетплейс', '9 дней', 'Промо']
        ].map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td>' + r[1] + '</td><td>' + r[2] + '</td><td>' + r[3] + '</td></tr>';
        }).join('');
    }

    // ── Quality
    var qk = $('#qKpis');
    if (qk) {
      var openC = cases.filter(function (c) { return c.status !== 'closed'; }).length;
      qk.innerHTML =
        kpi('Открытые', String(openC), 'в работе', openC ? 'warn' : 'up') +
        kpi('Жалобы / 100 зак.', '1.8', 'норма', 'up') +
        kpi('Ср. закрытие', '6.5 ч', 'цель ≤ 8 ч', 'up') +
        kpi('Повторные жалобы', '0.4%', 'низко', 'up');
    }
    var qtr = $('#qTypeRank');
    if (qtr) {
      var types = { complaint: 0, feedback: 0, claim: 0, question: 0 };
      cases.forEach(function (c) { types[c.type] = (types[c.type] || 0) + 1; });
      qtr.innerHTML = rankHtml([
        { n: 'Жалоба', v: String(types.complaint || 0), w: types.complaint || 0 },
        { n: 'Претензия', v: String(types.claim || 0), w: types.claim || 0 },
        { n: 'Вопрос', v: String(types.question || 0), w: types.question || 0 },
        { n: 'Отзыв', v: String(types.feedback || 0), w: types.feedback || 0 }
      ]);
    }
    var qr = $('#qReasonTable');
    if (qr) {
      qr.innerHTML = '<tr><th>Причина</th><th class="num">Шт.</th><th class="num">Доля</th></tr>' +
        [
          ['Качество / увядшие', '4', '36%'],
          ['Опоздание курьера', '3', '27%'],
          ['Не тот состав', '2', '18%'],
          ['Адрес / слот', '1', '9%'],
          ['Прочее', '1', '9%']
        ].map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td></tr>';
        }).join('');
    }
    var qo = $('#qOpenTable');
    if (qo) {
      var openList = cases.filter(function (c) { return c.status !== 'closed'; });
      qo.innerHTML = '<tr><th>№</th><th>Тема</th><th>Точка</th><th>Статус</th></tr>' +
        (openList.length ? openList.map(function (c) {
          return '<tr><td><b>' + esc(c.number) + '</b></td><td>' + esc(c.title) + '</td><td>' + esc(c.shop) + '</td><td>' + esc(CASE_ST[c.status] || c.status) + '</td></tr>';
        }).join('') : '<tr><td colspan="4" style="color:var(--ink-faint)">Нет открытых</td></tr>');
    }
    var qs = $('#qShopTable');
    if (qs) {
      qs.innerHTML = '<tr><th>Точка</th><th class="num">Жалобы</th><th class="num">На 100 зак.</th><th class="num">Закрыто вовремя</th></tr>' +
        [
          ['Мира 14', '3', '1.4', '92%'],
          ['Ленина 92', '5', '2.2', '88%'],
          ['Рижская 8', '2', '1.9', '90%']
        ].map(function (r) {
          return '<tr><td><b>' + r[0] + '</b></td><td class="num">' + r[1] + '</td><td class="num">' + r[2] + '</td><td class="num">' + r[3] + '</td></tr>';
        }).join('');
    }

    setText('#anWeek', weekOrd);
    setText('#anRev', fmtPrice(weekSum));
    setText('#anAov', fmtPrice(aov));
    setText('#anConv', '34%');
    setText('#anRet', '1.2%');
    setText('#anUnreadRep', chats.reduce(function (s, c) { return s + (c.unread || 0); }, 0));

    renderChart();
  }
'''


def main():
    for path in paths:
        if not path.exists():
            print("skip", path)
            continue
        text = path.read_text(encoding="utf-8")

        # inject CSS before reports section end marker - after .pill-row styles
        if ".rep-kpi-row" not in text:
            # insert after pill-row span styles - find REPORTS block end of heat styles
            anchor = "  .pill-row span {\n font-size: 0.78rem; font-weight: 700; padding: 8px 12px; border-radius: 999px;\n background: var(--bg-3); color: var(--ink-dim);"
            # find full pill-row block
            m = re.search(
                r"  \.pill-row span \{[^}]+\}",
                text,
            )
            if m:
                text = text[: m.end()] + "\n" + CSS_EXTRA + text[m.end() :]
                print("css ok", path.name)
            else:
                text = text.replace("</style>", CSS_EXTRA + "\n</style>")
                print("css fallback", path.name)

        # replace analytics section
        m = re.search(
            r" <!-- ═════════════ 04 · REPORTS ═════════════ -->\s*<section data-section=\"analytics\"[\s\S]*?</section>",
            text,
        )
        if not m:
            m = re.search(
                r"<section data-section=\"analytics\"[\s\S]*?</section>",
                text,
            )
        if not m:
            raise SystemExit("analytics section not found in " + str(path))
        text = text[: m.start()] + SECTION + text[m.end() :]
        print("section ok", path.name)

        # replace renderChart + renderReports functions
        m = re.search(
            r"  /\* ────────────────────────── REPORTS ────────────────────────── \*/[\s\S]*?  /\* ────────────────────────── RESET ────────────────────────── \*/",
            text,
        )
        if not m:
            raise SystemExit("REPORTS js not found")
        text = text[: m.start()] + JS + "\n  /* ────────────────────────── RESET ────────────────────────── */" + text[m.end() :]
        print("js ok", path.name)

        # bind period buttons - add after rep-tab binding if not present
        if "repPeriod" not in text or "data-period" not in text[text.find("function bind") : text.find("function bind") + 3000]:
            bind_snip = """
    var rp = $('#repPeriod');
    if (rp) rp.addEventListener('click', function (e) {
      var b = e.target.closest('[data-period]');
      if (!b) return;
      repPeriod = b.getAttribute('data-period');
      renderReports();
    });
"""
            # insert after rep-tab forEach block
            marker = "$$('.rep-tab').forEach(function (tab) {"
            idx = text.find(marker)
            if idx >= 0:
                # find end of this forEach - next }); after a few lines is fragile
                # insert before chSend instead
                pass
            marker2 = "$('#chSend').addEventListener('click', sendMessage);"
            if "data-period" not in text.split("function bind")[1][:5000] if "function bind" in text else True:
                if marker2 in text and "repPeriod" not in text[text.find(marker2) - 400 : text.find(marker2)]:
                    text = text.replace(
                        marker2,
                        bind_snip + "\n    " + marker2,
                        1,
                    )
                    print("bind period ok", path.name)

        path.write_text(text, encoding="utf-8")
        print("wrote", path, path.stat().st_size)


if __name__ == "__main__":
    main()
