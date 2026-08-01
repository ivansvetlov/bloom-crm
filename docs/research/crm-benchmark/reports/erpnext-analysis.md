# ERPNext — Bloom CRM Benchmark Analysis

| Meta | Value |
|------|--------|
| **id** | `erpnext` |
| **Product** | ERPNext |
| **Vendor** | Frappe Technologies Pvt Ltd |
| **Repo** | https://github.com/frappe/erpnext |
| **Docs** | https://docs.frappe.io/erpnext/ |
| **License** | GNU GPL-3.0 (code); docs CC-BY-SA-3.0 |
| **Stars (approx, 2026-08)** | ~37.5k |
| **Type** | Web ERP (+ bundled CRM module; separate Frappe CRM app) |
| **Stack** | Python · Frappe Framework · Vue (Frappe UI) · MariaDB/MySQL · Redis |
| **Review date** | 2026-08-01 |
| **Primary sources** | Official docs (docs.frappe.io/erpnext), GitHub README, frappe/crm README, module list `erpnext/modules.txt` |

**Bloom lens:** flower multi-shop ops CRM — marketplace + direct orders, dual status sync, WA/TG/MAX inbox, catalog, analytics, roles.

---

## 1. Product overview & positioning

ERPNext is a **full open-source ERP**, not a pure CRM. Positioning: one system for accounting, selling, buying, stock, manufacturing, projects, assets, support, and (legacy) CRM — “run the whole business for free.”

**Who it targets**

- SMBs and mid-market: manufacturing, distribution, retail, services.
- Teams that want **order → delivery → invoice → payment** in one database with stock and GL.
- Implementers who customize heavily via DocTypes, Server Scripts, and custom apps on Frappe.

**CRM story (important split)**

1. **ERPNext CRM module** (inside ERPNext desk, workspace CRM): Lead → Opportunity → Quotation → Customer → Sales Order. Official docs (develop) state this module is **scheduled for deprecation and full removal in version 17**; Frappe recommends **[Frappe CRM](https://github.com/frappe/crm)** for new CRM implementations.
2. **Frappe CRM** (separate app, Vue SPA at `/crm`): modern Lead/Deal UX, Kanban, Twilio/Exotel, WhatsApp via `frappe_whatsapp`, optional ERPNext bridge for invoicing/accounting.
3. **Selling / Stock / Accounts** stay in ERPNext regardless of CRM path — these are the ops-relevant surfaces for Bloom.

**Positioning vs Bloom**

| ERPNext | Bloom need |
|---------|------------|
| Generalist ERP for goods/services | Vertical ops cabinet for flower shops / network |
| Accounting-first document chain | Messenger-first + dual status + marketplace |
| Multi-**Company** legal entities | Multi-**shop** operational nodes (may not be separate legal entities) |
| Strong stock/warehouse | Strong catalog + delivery slots + florist capacity |
| Weak native omnichannel inbox | First-class WA/TG/MAX unified inbox |

**Takeaway:** ERPNext is the strongest **open ops + multi-entity order model** reference in the shortlist; it is a poor “adopt as product” candidate for Bloom without heavy verticalization, and its pre-sales CRM is forking away into Frappe CRM.

---

## 2. Architecture & stack

### Runtime

| Layer | Technology |
|-------|------------|
| Backend | Python 3, **Frappe Framework** |
| DB | **MariaDB** (primary); Postgres supported in newer stacks for some setups |
| Cache/queue | Redis; background workers (RQ) |
| Classic Desk UI | Frappe Desk (`/app`) — JS forms, list views, reports |
| Modern SPA apps | **Frappe UI** (Vue) — used by Frappe CRM and newer Frappe products |
| Hosting | Self-host (bench / Docker) or Frappe Cloud |
| Multi-tenancy | **Sites** on one bench; each site has own DB; multi-company is *inside* a site |

### Core framework concepts (stealable patterns, not necessarily stack)

- **DocType** — schema + form + permissions + API for every business object (`Lead`, `Sales Order`, `Item`, …).
- **Document** — one row/instance of a DocType; versioned, with comments, attachments, assignment.
- **docstatus** — submittable docs: `0` Draft, `1` Submitted, `2` Cancelled (immutable accounting discipline).
- **Child tables** — line items (`Sales Order Item`), taxes, sales team rows.
- **Naming series** — e.g. `SAL-ORD-.YYYY.-` for human-readable IDs.
- **Workspace** — module home with shortcuts, charts, number cards.
- **Role Permission Manager + User Permission** — type-level + record-level access.
- **REST API** — auto-generated CRUD for every DocType; whitelisted methods for custom logic.
- **Hooks / custom apps** — extend without forking core (`hooks.py`, Client/Server Scripts, custom DocTypes).

### Deployment shape

```
bench
 ├── sites/
│   ├── shop-network.localhost/   # one ERPNext site = one deployment tenant
│   └── ...
└── apps/
    ├── frappe
    ├── erpnext
    └── crm   (optional Frappe CRM)
```

Inside one site: many **Companies**, many **Warehouses**, many **Users**.

### UI architecture

- Classic desk: list → form → linked documents timeline; Awesomebar global search.
- Reports: Report Builder, Query Report, Script Report; dashboards.
- Print formats / Print Designer for quotes and invoices.
- Optional e-commerce / shopping cart → Sales Order of type **Shopping Cart**.

---

## 3. Domain model (entities, relationships)

### Real modules (`erpnext/modules.txt`)

```
Accounts
CRM
Buying
Projects
Selling
Setup
Manufacturing
Stock
Support
Utilities
Assets
Portal
Maintenance
Regional
ERPNext Integrations
Quality Management
Communication
Telephony
Bulk Transaction
Subcontracting
EDI
```

*(HR/Payroll often come as separate **Frappe HR** app; Helpdesk as **Frappe Helpdesk**.)*

### Entity map (Bloom-relevant)

```text
Company ──┬── Warehouse (stock locations)
          ├── Cost Center / Accounting Dimension
          └── (default accounts, currency)

Customer ──┬── Contact (person, multi-link)
           ├── Address (billing / shipping)
           ├── Territory, Customer Group, Price List
           └── Sales Order / Quotation / Invoice

Lead ──► Opportunity ──► Quotation ──► Customer
              │                │
              └── items/value  └──► Sales Order

Sales Order ──┬── Delivery Note ──► stock movement
              ├── Sales Invoice ──► GL + AR
              ├── Payment Entry / Payment Request
              ├── Pick List
              ├── Material Request / Purchase Order
              └── Work Order (manufacturing)

Item ──┬── Item Group, UOM, barcode
       ├── Item Price (per Price List)
       ├── Warehouse stock balance
       └── BOM (if manufacturing)

Communication / Email ── links to Lead, Customer, SO, Issue, …
Issue (Support) ── Customer, optional item/serial
```

### Key DocTypes by area

| Area | DocTypes (representative) |
|------|---------------------------|
| **Setup / org** | Company, User, Role, User Permission, Territory, Brand, Currency, Holiday List |
| **CRM (legacy)** | Lead, Opportunity, Prospect, Campaign, Email Campaign, Appointment, Lead Source, Opportunity Type, Sales Stage, CRM Settings |
| **Party** | Customer, Supplier, Contact, Address, Customer Group |
| **Selling** | Quotation, Sales Order, Sales Invoice, POS Invoice, Price List, Item Price, Pricing Rule, Shipping Rule, Sales Person, Sales Partner, Selling Settings |
| **Stock / catalog** | Item, Item Group, Warehouse, Bin, Delivery Note, Pick List, Stock Entry, Stock Reconciliation, Batch, Serial No |
| **Buying** | Supplier, Request for Quotation, Supplier Quotation, Purchase Order, Purchase Receipt, Purchase Invoice |
| **Accounts** | Payment Entry, Journal Entry, Payment Terms, Tax Category, Sales Taxes and Charges Template, Chart of Accounts, Cost Center |
| **Support** | Issue, Warranty Claim, Maintenance Schedule (service) |
| **Projects** | Project, Task, Timesheet |
| **Manufacturing** | BOM, Work Order, Job Card, Production Plan, Workstation, Routing |

### Relationships that matter for Bloom modeling

| ERPNext concept | Bloom analog (conceptually) |
|-----------------|-----------------------------|
| Company | Network legal entity or “accounting node” (not always = shop) |
| Warehouse / Cost Center | Shop / fulfillment point / stock room |
| Customer | End buyer (B2C) or corporate client |
| Contact | Recipient / buyer contact phones |
| Item + Item Group | Bouquet SKU / category / constructor base items |
| Sales Order | Order (marketplace or direct) |
| Sales Order Item | Order lines (SKU, qty, rate, warehouse) |
| Delivery Note | Fulfillment / courier handoff event |
| Sales Invoice + Payment Entry | Billing / payment dimension |
| Lead / Opportunity | Weak for marketplace ops; better as B2B florist acquisition only |
| Communication | Message timeline (email-centric in core) |
| Issue | Support ticket (not chat thread) |
| Inter Company Order Reference | Cross-entity order link (rare for flowers; interesting for franchise) |

### Catalog model (Item)

- **Item** is the product master: stock/non-stock, UOMs, barcodes, images, tax templates, default warehouses.
- **Item Price** lives on **Price Lists** (selling/buying, multi-currency).
- **Pricing Rule** for discounts, volume, customer group, campaign.
- No first-class “marketplace offer vs shop catalog” split — one Item master, multiple price lists / websites if configured.

### Order model (Sales Order)

Core commercial commitment document:

- Header: Company, Customer, Order Type (`Sales` | `Maintenance` | `Shopping Cart`), dates, currency, price list, addresses, contact, taxes, payment terms, project, inter-company ref.
- Lines: Item Code, qty, rate, warehouse, delivery date (per line), discounts, taxes.
- Does **not** itself post stock or full revenue; those come from Delivery Note / Sales Invoice.

---

## 4. UI / IA (navigation, key screens)

### Global shell

- URL pattern: `/app` (Desk).
- **Awesomebar** (search DocTypes, docs, reports).
- Left/side **module switcher** and per-user **Workspaces**.
- Document UX pattern: **List** → **Form** (sections, tabs, child tables) → **Timeline** (comments, email, versions, linked docs) → **Create** menu for next docs in chain.
- Status as colored badges on list and form; percentages (e.g. % delivered, % billed) on Sales Order list.

### Workspaces (ops IA skeleton)

Typical visible workspaces (role-filtered):

| Workspace | Primary objects |
|-----------|-----------------|
| **Home** | Shortcuts, dashboards |
| **CRM** | Lead, Opportunity, Campaign, pipeline reports *(legacy; deprecating)* |
| **Selling** | Customer, Quotation, Sales Order, Sales Invoice, pricing, POS |
| **Stock** | Item, Warehouse, Delivery Note, Stock Entry, stock reports |
| **Buying** | Supplier, Purchase Order, receipts |
| **Accounts** | Payment Entry, journals, financial reports |
| **Support** | Issue |
| **Projects** | Project, Task |
| **Manufacturing** | BOM, Work Order |
| **Setup / Users** | Company, permissions, email, integrations |

Users can **show/hide** module cards; service orgs often hide Manufacturing/Stock.

### Key screens (for MVP shell mapping)

1. **Sales Order List** — filters by status, company, customer, delivery date; columns: status, grand total, % delivered, % billed.
2. **Sales Order Form** — header commercial data + Items table + taxes + addresses + status actions (Hold, Close, Update Items, Create → DN/SI/…).
3. **Item List / Form** — catalog master.
4. **Customer Form** — party + linked contacts/addresses + dashboard of open orders/invoices.
5. **Lead / Opportunity** — pre-sales (less relevant to flower daily ops).
6. **Delivery Note** — fulfillment document.
7. **Stock summary / warehouse stock** — availability.
8. **POS** — retail counter sales (multi-outlet via POS Profile / company/warehouse).
9. **Reports** — Sales Analytics, pipeline (CRM), stock balance, P&L by company/cost center.
10. **Frappe CRM SPA** (if installed) — `/crm` Lead list, Lead detail (all-in-one page), Kanban, call UI — closer to modern CRM UX than Desk forms.

### IA strengths

- Module workspaces map cleanly to **roles** (seller vs stock vs accountant).
- Document **linked chain** is always visible (references, Create menu).
- List filters + saved views + assignments scale multi-user ops.

### IA weaknesses for Bloom

- No **inbox-first** navigation.
- No native “shop switcher” for ops (company switcher is legal/accounting-oriented).
- Dense form UX; florist floor staff will struggle without a simplified role UI.
- Marketplace vs direct channel not first-class in navigation.

---

## 5. Workflows & statuses

### Framework document lifecycle (submittable DocTypes)

| docstatus | UI label | Meaning |
|-----------|----------|---------|
| 0 | Draft | Editable; not committed |
| 1 | Submitted | Locked for normal edit; drives next docs |
| 2 | Cancelled | Reversed; amend creates new draft |

Optional **Workflow** DocType: multi-step approvals (e.g. Quotation: Draft → Pending Sales Manager → Approved) with role transitions and colors. Can override display status if configured.

### Sales Order operational statuses

From official Sales Order docs:

| Status | Meaning |
|--------|---------|
| **Draft** | Saved, not confirmed |
| **To Deliver and Bill** | Submitted; delivery and billing pending |
| **To Deliver** | Billed, delivery remaining |
| **To Bill** | Delivered, billing remaining |
| **Completed** | Delivery and billing complete |
| **On Hold** | Processing paused (`Status > Hold`) |
| **Closed** | Remaining qty intentionally not fulfilled |
| **Cancelled** | Submitted order reversed |

**Additional orthogonal dimensions** (filters on list):

- **Delivery Status**
- **Billing Status**
- **Advance Payment Status**

This is a true **multi-axis status model**: commercial submission × fulfillment × billing × payment. Partial delivery/billing updates **% delivered** and **% billed**.

### Order-to-cash chain

```text
Lead → Opportunity → Quotation → Customer
                         ↓
                   Sales Order (Submit)
                      ↙    ↓    ↘
              Pick List  Delivery Note  Sales Invoice
                              ↓              ↓
                         stock out      Payment Entry
```

Shortcuts allowed: SI from SO without DN (service/skip delivery); Shopping Cart origin; Maintenance order type with **Skip Delivery Note**.

### CRM pipeline statuses (legacy)

- **Lead**: capture → assign → qualify → convert to Opportunity / Customer; activity timeline (call/email/meeting).
- **Opportunity**: Sales Stage (configurable), probability %, expected closing date, next contact date, Lost Reason; from Lead / Customer / Prospect.
- Not Kanban-first in classic Desk (list-centric); **Frappe CRM** adds drag-drop Kanban for Lead/Deal.

### Support

- **Issue** lifecycle for tickets (Open / Replied / On Hold / Resolved / Closed — classic helpdesk pattern; exact labels version-dependent).
- Separate product trajectory: **Frappe Helpdesk** for modern ticketing.

### Custom workflow notes for Bloom

ERPNext shows that **one “status” string is not enough** for ops:

1. Immutable commit status (draft/submitted).
2. Fulfillment progress.
3. Money progress.
4. Optional hold/close for exception paths.

Bloom dual status (e.g. shop ops vs network/marketplace, or fulfillment vs payment) maps better to **orthogonal fields + derived badge** than to a single linear enum.

---

## 6. Integrations / inbox

### Built-in / first-party-ish

| Channel | Capability |
|---------|------------|
| **Email** | Email accounts, threading via **Communication**, Email Dropbox attach to Lead/Customer/Supplier, Email Campaign, Newsletter, templates |
| **Web forms** | Lead capture, automate lead creation |
| **Telephony** | ERPNext **Telephony** module; Frappe CRM: **Twilio**, **Exotel** (call + record) |
| **WhatsApp** | Not core ERPNext; **Frappe WhatsApp** (community, used by Frappe CRM) for send/receive |
| **ERPNext ↔ Frappe CRM** | Stated integration path for invoicing/accounting extension |
| **REST / webhooks** | Full DocType API; integrations marketplace apps |
| **eCommerce** | Website shopping cart → SO type Shopping Cart |
| **Payment gateways** | Via integrations / payment request flows |
| **EDI** | Module present for B2B electronic docs |

### What is **not** there (Bloom-critical gap)

- No **unified multi-messenger inbox** (WhatsApp + Telegram + MAX) as product surface comparable to Chatwoot.
- No first-class **conversation thread** entity bound to order with agent assignment queues, SLAs, canned replies across messengers.
- Email is the “timeline of record”; chat is bolt-on.
- Marketplace channel adapters (Flowwow-like) not native — would be custom Integration DocTypes + webhooks.

### Communication model to steal carefully

- **Timeline on the document** (order/customer) with typed events: comment, email, assignment, status change, linked docs.
- Assignment + due date on records.
- Separate **Campaign / Lead Source** for attribution — useful for marketing, less for same-day delivery ops.

---

## 7. Multi-company / multi-shop patterns

### Multi-company (first-class)

- Multiple **Company** records in one site.
- Each transactional DocType carries **Company** (currency, warehouses, accounts defaults).
- **User Permission** on Company (and Territory, Warehouse, Cost Center, Customer, …) restricts which rows a user sees — e.g. Sales User only sees Sales Orders for Company X.
- Parent/child company trees for group reporting.
- **Inter-company** flows: Customer/Supplier with **Represents Company**; linked SI/PI and SO/PO references for internal trade between legal entities.

### Multi-shop analogs

| Shop need | ERPNext pattern | Fit |
|-----------|-----------------|-----|
| Separate stock per store | **Warehouse** hierarchy under Company | Strong |
| Separate P&amp;L per store | **Cost Center** / Accounting Dimensions | Strong for finance |
| Staff only sees own shop | User Permission on Warehouse/Company + roles | Strong if shops ≈ companies or warehouses |
| Shared catalog | Global **Item** master | Strong |
| Shop-specific prices | Price List / Pricing Rule | Medium–strong |
| Franchise multi-legal | Multi-Company + inter-company | Strong |
| Same legal, many shops | One Company, many Warehouses + Cost Centers | Strong ops; weaker “shop as product object” |
| Network HQ vs shop roles | Roles + User Permission + workspace hide | Strong |
| Marketplace as virtual shop | Custom channel field / separate Company / custom DocType | DIY |

### Pattern summary for Bloom

ERPNext does **not** ship a “Shop” DocType. Operational multi-location is modeled as:

```text
Company (legal/accounting boundary)
  └── Warehouse (stock/fulfillment location)
  └── Cost Center (P&L slice)
  └── POS Profile (retail terminal config)
```

For a flower **network** where shops are often one legal entity, map Bloom **Shop** → Warehouse + Cost Center (+ optional custom Shop DocType for ops metadata: address, delivery zones, working hours, WA numbers). Use **Company** only when legal/accounting isolation is real.

---

## 8. What to STEAL for Bloom (concrete)

Prefer Russian product language for recommendations.

### 8.1 Dual (multi-axis) order status — must steal

Не один enum «статус заказа», а **независимые оси** + производный summary-бейдж:

| Ось ERPNext | Bloom-предложение |
|-------------|-------------------|
| docstatus Draft/Submitted | Черновик / Подтверждён (операционно) |
| Delivery Status + % delivered | **Фулфилмент:** новый → в сборке → курьер → доставлен / отменён |
| Billing/Payment Status | **Оплата:** не оплачен → предоплата → оплачен → возврат |
| On Hold / Closed | Пауза / закрыт без доставки остатка |
| (нет в ERPNext) | **Канал/сеть:** маркетплейс-статус ↔ статус магазина (dual sync) |

UI: на карточке заказа **2–3 бейджа**, в списке — колонки/фильтры по каждой оси (как Delivery vs Billing filters).

### 8.2 Document chain, not “god order”

Разделить:

1. **Order** (обязательство: что, кому, когда, цена).
2. **Fulfillment event** (сборка/выдача/курьер) ≈ Delivery Note.
3. **Payment event** ≈ Payment Entry / invoice state.

Частичное исполнение (% delivered / % billed) — копировать для multi-item букетов и частичных отмен.

### 8.3 Multi-shop isolation model

- **Role** = функция (флорист, менеджер, курьер, сеть-админ, аналитик).
- **User Permission / scope** = магазин(ы), к которым привязан пользователь.
- Глобальный каталог Item + локальный остаток Warehouse.
- HQ видит rollup; shop user — только свой scope.

### 8.4 Workspace IA by role

Боковое меню не «все модули ERP», а **ролевые кабинеты**:

- Магазин: Заказы · Каталог · Остатки · Чаты.
- Сеть: Магазины · Аналитика · Каталог-сеть · Пользователи.
- Поддержка/инбокс: единый inbox (у ERPNext взять только идею assignment, не email-only UX).

### 8.5 Party model

- **Customer** (плательщик) ≠ **Contact** (получатель/телефон) ≠ **Address** (адрес доставки).
- Для цветов: Buyer / Recipient / DeliveryAddress как явные связи на Order.

### 8.6 Extensibility pattern (product, not GPL fork)

- Стабильные core entities + **custom fields** / extension modules.
- Auto REST на сущностях для marketplace connectors.
- Naming series для человекочитаемых `ORD-2026-…`.
- Timeline событий на заказе (кто сменил статус, сообщение, назначение).

### 8.7 Pricing / catalog structure

- Item master + Price List + rules — хорошая база для «базовый SKU + наценка магазина / канал».
- Shipping Rule ≈ зона/слот доставки (адаптировать под time slots, не Incoterms).

### 8.8 Inter-company link field

Поле **Inter Company Order Reference** — идея для связи «заказ сети ↔ заказ магазина» или «маркетплейс order id ↔ internal order» без смешивания документов.

### 8.9 Hold / Close / Cancel semantics

- **Cancel** = отмена обязательства (с правилами по связанным документам).
- **Close** = остаток не выполнять, история сохраняется.
- **Hold** = пауза (нет цветов / клиент недоступен).

Bloom должен различать эти три действия в UX и API.

---

## 9. What to AVOID

1. **Тянуть весь ERPNext как продукт Bloom** — избыточный GL, manufacturing, assets; долгое внедрение; UX не для курьера/флориста.
2. **Один линейный CRM pipeline (Lead→Opportunity) как ядро ops** — для daily flower orders pipeline B2B-продаж вторичен; marketplace order ≠ sales opportunity.
3. **Строить inbox на email Communication** — не закрывает WA/TG/MAX; для inbox-бенчмарка смотреть Chatwoot, не ERPNext.
4. **Приравнивать Shop = Company всегда** — сломает мультимагазин в одном юрлице; раздувает chart of accounts.
5. **Жёсткий docstatus accounting-lock без ops-режима** — submitted immutability хороша для бухгалтерии; для thrashing same-day order edits нужна controlled “Update Items” / state machine без боли Cancel+Amend.
6. **Desk form density as default UI** — 50+ полей на SO form убьёт speed-to-action; Bloom MVP — узкие экраны задач.
7. **Legacy ERPNext CRM как long-term dependency** — deprecation к v17; не копировать Lead/Opportunity как foundation без осознанного Frappe CRM split.
8. **GPL-fork path** — если Bloom закрытый/отдельный продукт, **идеи и IA** воровать, не кодовую базу ERPNext (GPL-3.0 constraints на derivative distribution).
9. **Скрытая магия статусов без явных осей** — «Completed» как единственный success без % delivered/% paid маскирует operational debt.
10. **POS-only мышление для сети** — POS полезен для walk-in, не заменяет marketplace dual intake.

---

## 10. Implementation notes for a web MVP shell

Goal of `mvp/erpnext/index.html`: offline structure prototype of **ERPNext IA**, not Bloom skin (per ORCHESTRATOR). Below: what to show and how it informs Bloom mega later.

### MVP shell map (ERPNext-faithful)

```text
App shell
├── Awesomebar (fake search)
├── Workspace switcher
│   ├── Home (number cards: Open SO, To Deliver, To Bill)
│   ├── CRM → Leads | Opportunities | Campaigns
│   ├── Selling → Customers | Quotations | Sales Orders | Invoices | Price Lists
│   ├── Stock → Items | Warehouses | Delivery Notes | Stock Summary
│   ├── Accounts → Payment Entry (stub)
│   ├── Support → Issues
│   └── Setup → Companies | Users (stub)
└── Patterns
    ├── List view (filters, status badges, % delivered/billed)
    ├── Form view (header + child table Items + timeline)
    └── Linked Create menu (Delivery Note, Sales Invoice)
```

### Minimum interactive stories

1. Open **Sales Order list** → filter by status “To Deliver and Bill”.
2. Open one SO → see dual badges Delivery/Billing + item table + timeline.
3. Switch **Company** (or show company column) to illustrate multi-entity.
4. Navigate **Item** master and **Warehouse** stock stub.
5. Show **Lead → Opportunity** path as secondary CRM workspace (label “legacy CRM”).
6. Optional note banner: “CRM module deprecating → Frappe CRM”.

### Tech notes for static HTML MVP

- Single `index.html` + minimal CSS; hash routes or `data-view` tabs.
- Labels must use real names: **Sales Order**, **Delivery Note**, **Customer**, **Item**, **Warehouse**, **Company**.
- Status chips exact strings from §5.
- No backend; placeholder tables OK.

### If prototyping Bloom *inspired by* ERPNext (mega later)

| Screen | ERPNext source | Bloom twist |
|--------|----------------|-------------|
| Orders list | SO list | Channel filter marketplace/direct; dual status chips |
| Order detail | SO form | Compact ops actions; chat panel side |
| Catalog | Item | Photo-first bouquet cards |
| Shops | Warehouse/Company | Shop switcher + hours/zones |
| Inbox | — (gap) | Borrow from Chatwoot, link thread → Order |
| Analytics | Sales Analytics | Shop/network KPIs, not only GL |

### Stack recommendation for real Bloom (not ERPNext)

- Do **not** require Frappe for MVP.
- Steal **domain shapes** (Order, Line, Party, Location/Shop, multi-axis status, RBAC+scope).
- Prefer stack already chosen by Bloom team; expose REST/events for marketplace sync like Frappe auto-API philosophy.

### Extensibility / self-host (reference)

- Self-host: Docker (`frappe_docker`) or bench; Frappe Cloud managed.
- API: `/api/resource/{DocType}` CRUD; API keys / OAuth-style token patterns.
- Custom app: `bench get-app` + install on site.
- License: ERPNext **GPL-3.0**; Frappe Framework historically **MIT**; Frappe CRM **AGPL-3.0** — license mix matters if embedding.

---

## 11. Fit score 1–10 for Bloom

### Scorecard

| Dimension | Score | Notes |
|-----------|------:|-------|
| Order / fulfillment model | **9** | SO → DN → SI, partial %, hold/close — gold reference |
| Multi-shop / multi-entity | **8** | Company + Warehouse + User Permission; no native Shop |
| Dual / multi-axis status | **8** | Delivery × Billing × Payment; missing marketplace sync axis |
| Catalog / stock | **8** | Item, warehouses, price lists mature |
| Roles & permissions | **8** | Roles + record rules industry-standard |
| Analytics | **7** | Strong ERP reports; not florist-ops KPI pack |
| CRM pre-sales | **5** | Fine for B2B; wrong core for same-day flower ops; module deprecating |
| Messenger inbox WA/TG/MAX | **2** | Email/telephony + bolt-on WA; not omnichannel inbox product |
| Marketplace + direct dual intake | **3** | Possible via custom fields/integrations only |
| UX for shop-floor speed | **4** | Powerful but heavy Desk forms |
| Adopt-as-is product | **3** | Wrong shape/license/vertical; huge surface area |
| **Pattern source / benchmark value** | **9** | Best OSS ops-order blueprint in shortlist |

### Overall fit for Bloom: **7 / 10**

**Interpretation**

- **7** as *research and domain-pattern benchmark* (shortlist rank #1 for ops model is justified).
- **~3–4** as *system to deploy for Bloom* without rebuilding half the product.
- Steal ruthlessly from **Selling + Stock + multi-company permissions + multi-axis status**.
- Pair with a **Chatwoot-class inbox** reference for messengers; do not expect ERPNext to carry Bloom’s communication spine.
- Treat **Frappe CRM** as a separate modern CRM UX sample (Kanban, all-in-one Lead page, WhatsApp integration), not as flower ops core.

---

## Appendix A — Mapping: ERPNext concept → Bloom concept

| ERPNext | Bloom |
|---------|--------|
| Company | Legal entity / network accounting node |
| Warehouse / Cost Center | Shop / fulfillment point |
| Customer | Buyer (client) |
| Contact | Recipient / contact person |
| Address | Delivery address |
| Item / Item Group | Product / category (bouquet SKU) |
| Price List / Pricing Rule | Channel or shop pricing |
| Lead / Opportunity | Optional B2B florist/partner sales only |
| Quotation | Rare (corporate orders); optional |
| Sales Order | Order |
| Sales Order Item | Order line |
| Delivery Note | Fulfillment / delivery act |
| Sales Invoice / Payment Entry | Payment & fiscal dimension |
| docstatus | Commit state |
| Delivery Status | Fulfillment status axis |
| Billing / Payment Status | Money status axis |
| On Hold / Closed / Cancelled | Exception paths |
| User + Role | Staff roles |
| User Permission | Shop/network data scope |
| Communication timeline | Order activity feed (extend to messengers) |
| Issue | Support ticket (≠ chat) |
| Campaign / Lead Source | Marketing attribution |
| Inter Company Reference | External marketplace id ↔ internal order link |
| POS Profile | Walk-in counter (secondary) |
| Workspace | Role cabinet IA |

---

## Appendix B — Source anchors

- Repo: https://github.com/frappe/erpnext  
- Modules list: `erpnext/modules.txt` in develop  
- CRM intro + v17 deprecation: https://docs.frappe.io/erpnext/CRM  
- Sales Order statuses & chain: https://docs.frappe.io/erpnext/sales-order  
- Selling cycle overview: https://docs.erpnext.com / docs.frappe.io Selling docs  
- User Permissions: https://docs.frappe.io/erpnext/user-permissions  
- Inter-company: https://docs.frappe.io/erpnext/inter-company-invoices  
- Frappe CRM: https://github.com/frappe/crm  
- License: GPL-3.0 (erpnext.com license page)

---

## Appendix C — Bloom steal checklist (actionable)

- [ ] Order entity with **fulfillment_status**, **payment_status**, **channel_status** (marketplace sync), **hold/close**
- [ ] Order lines with partial cancel/fulfill quantities
- [ ] Shop scope on users; global catalog; per-shop stock
- [ ] Buyer ≠ recipient ≠ address
- [ ] Timeline on order (status, assign, messages, external ids)
- [ ] Role workspaces (shop / network / finance light)
- [ ] External_id + source_channel on order (inter-company ref idea)
- [ ] Do **not** implement full GL/manufacturing for MVP
- [ ] Inbox as separate subsystem linked by `order_id` / `customer_id`
- [ ] MVP HTML for erpnext: workspaces Selling/Stock/CRM + SO dual badges

---

*End of report — id: `erpnext` — 2026-08-01*
