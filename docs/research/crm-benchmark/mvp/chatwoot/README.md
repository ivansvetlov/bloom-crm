# Chatwoot · Omni-inbox MVP

**Program:** Bloom CRM open-source CRM research  
**Artifact:** Structure MVP for `{id}` = `chatwoot`  
**Path:** `docs/research/crm-benchmark/mvp/chatwoot/`  
**Entry:** open `index.html` in a browser (offline, no backend)

---

## What this is

Clickable **web shell** inspired by [Chatwoot](https://github.com/chatwoot/chatwoot) omni-channel inbox. Built for Bloom research: flower-shop ops context (orders, multi-shop labels, WA / TG / MAX channels).

Badge in UI: **MVP · Chatwoot inbox → web**

Not a production Chatwoot install — a self-contained HTML/CSS/JS prototype of inbox **information architecture** and agent flows.

---

## Layout (Chatwoot-like)

| Pane | Role |
|------|------|
| **Left** | Inbox tabs (Mine / Unassigned / All), channel chips, conversation list |
| **Center** | Thread header, message stream, composer (reply + private note) |
| **Right** | Contact card, attributes, tags, linked mock orders, actions |

---

## Channels (mock)

- **WhatsApp**
- **Telegram**
- **MAX**

Filter chips filter the conversation list client-side.

---

## Interactive flows (local only)

1. **Switch chats** — click a row; unread clears; thread + contact update  
2. **Filter** — tabs + channel + search  
3. **Send message** — Enter or «Отправить»; stays in memory (mock)  
4. **Private note** — toggle «Приват»; dashed yellow bubble, not a real channel send  
5. **Resolve / reopen** — status pill + list labels  
6. **Assign to me** — sets assignee to demo agent «Анна К.»  
7. **Create order** — button in header or contact pane → mini form → mock order on contact + system line in thread  

No API, no persistence after reload.

---

## UI language

Russian labels (OK for Bloom research demos). Product chrome keeps Chatwoot naming where useful (`Open` / `Pending` / `Resolved`).

---

## How to open

```text
# file://
docs/research/crm-benchmark/mvp/chatwoot/index.html
```

Or any static server from the folder, e.g.:

```bash
npx --yes serve .
```

---

## Bloom mapping (why Chatwoot is in the shortlist)

| Chatwoot concept | Bloom relevance |
|------------------|-----------------|
| Omni-inbox + channels | Unified WA / TG / MAX threads for shop ops |
| Conversation status | Agent workflow parallel to order fulfillment status |
| Assignee / unassigned | Multi-shop staffing / queue |
| Contact sidebar + custom attrs | Client card next to chat |
| Private notes | Internal florist/courier coordination |
| Labels / tags | VIP, Flowwow vs direct, corporate |
| Order link (mocked here) | Chat ↔ order as source of truth in Bloom |

Steal for Bloom: **3-pane inbox IA**, channel badges, private notes, contact+order sidebar.  
Do not treat Chatwoot alone as full CRM/orders/stock — it is the best open **inbox** reference, not full flower-ops ERP.

---

## Files

```text
mvp/chatwoot/
├── index.html   # single-file shell (CSS + JS inlined)
└── README.md    # this file
```

---

## Meta

| Field | Value |
|-------|--------|
| Product | Chatwoot |
| License (upstream) | MIT (community core); enterprise path proprietary |
| Stack (upstream) | Ruby on Rails / Vue / PostgreSQL / Redis |
| MVP date | 2026-08-01 |
| Related | `reports/chatwoot-analysis.md` (when Analyzer ships) |
