# ERPNext structure MVP (Bloom research)

**Path:** `docs/research/crm-benchmark/mvp/erpnext/`  
**Entry:** open `index.html` offline (no backend).  
**Label:** MVP · ERPNext structure → web  
**Purpose:** clickable shell that mirrors **ERPNext Desk module layout** and core Selling/CRM/Stock document flows — not a product clone.

---

## Screens

| Screen | ERPNext analogue | Interaction |
|--------|------------------|-------------|
| **Dashboard** | Desk home / workspace KPIs | Module tiles, open SO table → form |
| **Клиенты** | CRM → Customer (List) | Search/filter, mock add customer |
| **Лиды** | CRM → Lead (List, light) | Static list for module completeness |
| **Заказы (Sales Order)** | Selling → Sales Order (List) | Filter by status; row opens form |
| **SO Form** | Sales Order (Form + workflow) | Status buttons mutate local state + history |
| **Номенклатура** | Stock → Item (List) | Search/group filter, stock qty badges |
| **Buying / Accounting** | Module stubs | Empty states; show desk adjacency only |

### Status workflow (mock SO)

Simplified ERPNext-style transitions (local JS state only):

- `Draft` → Submit → `To Deliver and Bill` | Cancel  
- `To Deliver and Bill` → Deliver / Invoice / Deliver+Bill / Hold / Cancel  
- `To Deliver` | `To Bill` → terminal paths → `Completed`  
- `On Hold` → Resume / Cancel  
- `Completed` / `Cancelled` — terminal (no actions)

---

## Desk structure (sidebar)

```
Dashboard
CRM        → Клиенты, Лиды
Selling    → Sales Order (+ Form)
Stock      → Item
Buying     → stub
Accounting → stub
```

This is the structural takeaway: **ops CRM sits next to Selling + Stock + Accounting**, not as a standalone “deals only” app.

---

## Mapping to Bloom CRM

| ERPNext idea (this MVP) | Bloom relevance |
|-------------------------|-----------------|
| Multi-module Desk | Bloom ops cabinet should feel modular (orders, shops, inbox, stock) not single-pipeline CRM |
| Customer master + Sales Order | Dual intake (marketplace + direct) still needs **customer + order** documents, not only “deal” |
| SO status workflow | Bloom **dual status** (fulfillment vs payment / shop vs network) can extend this pattern with parallel dimensions |
| Item + stock qty | Flower ops: SKUs, perishable stock, low/out signals before dispatch |
| Company on SO | Multi-shop / multi-company isolation pattern |
| Buying / Accounting stubs | Suppliers, receipts, marketplace settlement — later modules, same desk |
| Awesome Bar (search) | Fast jump across entities (order #, customer, SKU) |

**What this MVP does not cover (by design):** multi-company UI, stock ledger, real invoices, omnichannel inbox (see Chatwoot MVP), permissions, or Frappe meta/DocType builder.

---

## Files

| File | Role |
|------|------|
| `index.html` | Self-contained HTML + CSS + JS (mock data, routing, status changes) |
| `README.md` | This note |

---

## How to review

1. Open `index.html` in a browser.  
2. Walk: Dashboard → Клиенты → Заказы → open SO → click **Submit / Deliver / Hold**.  
3. Confirm status pill, sidebar history, and list filters update without reload.  
4. Use Stock → Item list and Buying/Accounting stubs for full module map.

*Structural study for Bloom CRM · research artifact under `crm-benchmark`.*
