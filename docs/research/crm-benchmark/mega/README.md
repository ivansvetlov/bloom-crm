# Bloom Mega CRM · research MVP

**Program:** Bloom CRM open-source CRM research  
**Path:** `docs/research/crm-benchmark/mega/`  
**Entry:** open `index.html` in a browser (offline, no backend)  
**Badge:** **Bloom Mega CRM · research MVP**

Interactive structure MVP of a **flower-network ops cabinet**, assembled by synergizing IA/UX patterns from the shortlisted OSS CRMs. Not a product clone of any single system.

---

## How to open

1. Open this file in any modern browser (Chrome / Edge / Firefox / Safari):

   `docs/research/crm-benchmark/mega/index.html`

2. Or from a terminal:

   ```bash
   # Windows
   start docs/research/crm-benchmark/mega/index.html

   # macOS
   open docs/research/crm-benchmark/mega/index.html
   ```

3. No server, install, or API required. All state is in-memory mock data (reload resets).

---

## Module map

| Sidebar | Screen | What you can poke |
|---------|--------|-------------------|
| **Сегодня** | Ops dashboard | KPI cards, live event feed, quick actions, per-shop summary |
| **Заказы** | Kanban + list | Dual badges (fulfillment status × channel marketplace\|direct), click card → detail drawer + stream, **advance status**, filters by channel/shop, **new-order simulation** (~7s while on this screen) |
| **Чаты** | 3-pane omni-inbox | WA / TG / MAX list → thread → contact pane; send reply / private note; assign; resolve; **create order from chat** |
| **Витрина** | Product catalog | Price, stock ±, hide/show on storefront, low-stock filter |
| **Отчёты** | Analytics tabs | Sales (funnel + weekly bars), Channels (MP vs direct + messengers), Shops (multi-point rollup) |
| **Настройки** | Stubs | Shops (switch active point), users, channels, roles ACL stub |

### Status workflow (fulfillment axis)

```
Новый → Принят → Собран → В пути → Доставлен
```

Advance via:

- button on kanban card  
- list row action  
- drawer footer **«Продвинуть статус →»**

Payment axis is shown as a secondary badge (`Оплачен` / `Ожидает` / `При получении`) — dual-status model, ERPNext-inspired.

---

## Which OSS pattern each screen steals

| Bloom screen | Primary OSS pattern | Secondary borrows |
|--------------|---------------------|-------------------|
| **Shell / sidebar** | **Krayin** — modular ops menu + settings ACL shape | **Twenty** — calm density, soft surfaces |
| **Сегодня** | **ERPNext** Desk home / workspace KPIs | **EspoCRM** activity stream; **Twenty** card grid |
| **Заказы kanban** | **EspoCRM** entity kanban + **Krayin** pipeline columns | **ERPNext** multi-axis status (fulfillment + payment/channel badges) |
| **Заказы list + drawer** | **EspoCRM** list → detail + **stream** history | **Dolibarr** document chain strip (Заказ → Оплата → Сборка → Доставка) |
| **Чаты** | **Chatwoot** 3-pane omni-inbox (list / thread / contact) | WA·TG·MAX channels; create order from conversation |
| **Витрина** | **Dolibarr** stock/product + **ERPNext** Item list | hide/show + qty controls as shop floor ops |
| **Отчёты** | **ERPNext** / ops rollups by shop & channel | tabbed analytics (sales · channels · shops) |
| **Настройки** | **Krayin** settings/ACL menu skeleton | multi-shop switcher (ERPNext company/branch idea) |
| **Global search ⌘K** | **ERPNext** Awesome Bar jump | order / chat / SKU quick find |

Footer in the UI repeats this lineage:

> Assembled from OSS CRM patterns (ERPNext, Dolibarr, Chatwoot, Twenty, Krayin, EspoCRM) — structure study

---

## Bloom mapping (why these patterns)

| Bloom need | Pattern used in mega |
|------------|----------------------|
| Marketplace + direct orders | Dual channel badges on every order card/row |
| Multi-shop network | Shop switcher, filters, reports by point |
| Messenger inbox | Chatwoot-style 3-pane, order-linked contact pane |
| Dual status | Fulfillment workflow + payment badge |
| Stock / vitrina | Product cards with stock and visibility |
| Ops KPIs | Today dashboard + report tabs |

---

## Suggested 10-minute click path

1. **Сегодня** — read KPIs and feed; click «К заказам».  
2. **Заказы** — switch Канбан / Список; filter «Маркетплейс»; open a card; advance status twice.  
3. Leave sim running — wait for a **new order** flash on kanban.  
4. **Чаты** — open WA dialog, send a reply, toggle note, **＋ Заказ** from chat.  
5. **Витрина** — hide a product, drop stock to low, filter «Мало».  
6. **Отчёты** — walk tabs Продажи → Каналы → Точки.  
7. **Настройки** — switch shop; browse users / channels stubs.  
8. Use top search: type `BL-` or a client name, Enter.

---

## Files

| File | Role |
|------|------|
| `index.html` | Self-contained HTML + CSS + JS (mock data, routing, workflows) |
| `README.md` | This note |

Related research:

- Per-CRM analysis: `../reports/{id}-analysis.md`
- Per-CRM structure shells: `../mvp/{id}/index.html`
- Orchestrator rules: `../ORCHESTRATOR.md`

---

## Out of scope (by design)

- Real backend, auth, persistence  
- Real WhatsApp / Telegram / MAX APIs  
- Production ACL enforcement  
- Full accounting / stock ledger  
- Pixel-perfect clones of third-party UIs  

This is a **structure study** for Bloom product design, not shippable software.
