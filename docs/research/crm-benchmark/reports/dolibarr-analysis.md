# Dolibarr ERP/CRM — Bloom CRM Benchmark Analysis

| Field | Value |
|-------|--------|
| **id** | `dolibarr` |
| **Product** | Dolibarr ERP & CRM |
| **License** | GPL-3.0-or-later |
| **Stack** | PHP (no heavy framework) + JS enhancements · MariaDB / MySQL / PostgreSQL |
| **Type** | Modular web ERP/CRM (self-host + Docker + SaaS partners) |
| **Repo** | https://github.com/Dolibarr/dolibarr |
| **Docs** | https://wiki.dolibarr.org · https://www.dolibarr.org |
| **Marketplace** | https://www.dolistore.com (~1000+ addons) |
| **Review date** | 2026-08-01 |
| **Sources** | GitHub README/develop, `Commande` / `Expedition` / `Ticket` / `CommonObject` class sources, Wiki MultiCompany & REST API |

---

## 1. Overview

Dolibarr is a **modular ERP+CRM suite** aimed at SMEs, freelancers, and foundations. Positioning is deliberately broad: enable only the modules you need (≈100 built-in modules; thousands on DoliStore). It is **not** a modern “ops inbox CRM” and **not** marketplace-native; it is a classic European ERP spine with CRM sales documents, stock, accounting, tickets, and a light collaboration layer.

**Relevance to Bloom (flower multi-shop ops):**

| Bloom need | Dolibarr affinity |
|------------|-------------------|
| Marketplace + direct orders | Partial — sales orders exist; channel is a weak metadata field (`source`, `module_source`/`pos_source`, not dual-intake model) |
| Multi-shop isolation | Partial — multi-entity via paid **MultiCompany**; warehouses can approximate shops |
| Dual status sync | Strong pattern — **lifecycle status** + independent **billed** flag (and separate shipment object status) |
| WA/TG/MAX inbox | Weak — **Ticket** + **EmailCollector** only; no messenger channels |
| Catalog | Strong — **Products/Services**, variants, stock, barcodes, categories |
| Analytics | Medium — margins, reports, dashboards; not network/shop rollups |
| Roles | Strong — groups + fine-grained module rights (+ advanced perms) |

**Fit score (Bloom): 5.5 / 10** — excellent **document-chain and dual-dimension status** reference; weak as product shell for messenger-first multi-shop flower ops. Steal patterns, do not fork.

---

## 2. Architecture

### 2.1 Runtime shape

```
Browser → Apache/Nginx
        → htdocs/ (PHP entrypoints per module)
        → conf/conf.php
        → MariaDB/MySQL/PostgreSQL
        → documents/ (generated PDFs, attachments, install.lock)
```

- **No Symfony/Laravel/Doctrine stack** — intentional: “PHP with no heavy framework.”
- Module activation is feature-flag style (`isModEnabled('order')`, etc.).
- Web root is `htdocs/`; business classes live under `htdocs/{module}/class/`.
- External modules deploy to `htdocs/custom/` (Module Builder + DoliStore install UI).

### 2.2 Core extension model (concrete)

| Mechanism | Role | Concrete examples |
|-----------|------|-------------------|
| **Triggers** | Domain events on object lifecycle | `ORDER_CREATE`, `ORDER_VALIDATE`, `ORDER_CLOSE`, `ORDER_CANCEL`, `SHIPPING_VALIDATE`, `TICKET_CREATE` |
| **Hooks** | UI/DAO interception points | `$hookmanager->executeHooks('createFrom', ...)`, `getTooltipContent`, `LibStatut` |
| **Extrafields** | Per-table custom columns | `isextrafieldmanaged = 1` on Commande, Expedition, Ticket… |
| **Element links** | Polymorphic object graph | `element_element` — Propal→Commande→Expedition→Facture |
| **Contacts on element** | Roles on documents | `element_contact` + dictionary `c_type_contact` (SHIPPING, BILLING, SUPPORTTEC…) |
| **REST API** | External integration | `/api/index.php/{resource}` + header `DOLAPIKEY`; multi-entity via `DOLAPIENTITY` |
| **SOAP** | Legacy web services | Still present; REST is preferred path |
| **Numbering addons** | Ref strategies | e.g. `COMMANDE_ADDON`, `EXPEDITION_ADDON_NUMBER` |
| **PDF/ODT models** | Document generation | Per object `model_pdf` |
| **Dictionaries** | Configurable enums | Ticket types/categories/severities, payment terms, shipment modes |

### 2.3 Object inheritance spine

```
CommonObject (+ CommonTrigger)
  ├── CommonOrder → Commande (sales order)
  ├── Expedition (shipment)
  ├── Facture (invoice)
  ├── Propal (proposal/quote)
  ├── Ticket
  ├── Societe (third party)
  ├── Product
  └── …
```

CommonObject owns: `entity`, `status`/`statut`, notes, linked objects, contacts, extrafields, multicurrency totals, PDF refs, bank/payment FK helpers.

### 2.4 Multi-entity primitives (core, even without MultiCompany UI)

Almost every business table has:

- `entity` integer (default `1`)
- `ismultientitymanaged = 1` on classes
- Query scoping via `getEntity('commande')` / `getEntity('expedition')` / `setEntity($this)` on create

This is the **kernel multi-tenant hook**. Full multi-company UX is an external module (see §7).

### 2.5 Module map (Bloom-relevant, concrete names)

| Area | Module / path keys | Objects / tables |
|------|--------------------|------------------|
| Parties | **Third Parties** (`societe`) | `Societe`, contacts `socpeople` |
| CRM pipeline | **Opportunities / Leads**, **Proposals** (`propal`) | leads, `Propal` |
| Sales | **Orders** (`commande`) | `Commande`, `OrderLine` / `commandedet` |
| Fulfillment | **Shipments** (`expedition`) | `Expedition`, `ExpeditionLigne` |
| Delivery receipt | **Delivery** submodule | `Delivery` from shipment |
| Billing | **Invoices** (`facture`) | customer invoices, credit notes |
| Catalog | **Products/Services** (`product`) | products, variants, BOM |
| Stock | **Stock / Warehouse** (`stock`) | `Entrepot`, stock movements |
| POS | **TakePOS** / CashDesk | `module_source`, `pos_source` on orders |
| Support | **Ticket** (+ knowledge) | `Ticket`, ticket messages cache |
| Mail intake | **EmailCollector** | rules → create tickets/objects from mailbox |
| Projects | **Projects / Tasks** | `Project` |
| Calendar | **Agenda** | events, iCal |
| ECM | **EDM** | attachments / `ecm_files` |
| Payments | **Bank**, Stripe/PayPal modules | payment modes, online payment URL |
| HR | Leaves, expenses, recruitment, timesheets | out of Bloom scope mostly |
| Manufacturing | BOM, MO, Workstations | limited Bloom relevance |

---

## 3. Domain model

### 3.1 Canonical commercial chain

```
Societe (customer/prospect/supplier)
  └── Contact (socpeople)
        └── Propal (quote) ──linked──► Commande (order)
                                         ├── OrderLine (product/service lines)
                                         ├── Expedition (1..n partial shipments)
                                         │     └── ExpeditionLigne (+ batch/lot optional)
                                         └── Facture (invoice)  [billed flag on order]
```

**Key design property:** documents are **separate first-class objects** with their own refs, statuses, PDFs, and triggers — not one “order row” with nested stages only.

### 3.2 Core objects (Bloom mapping preview)

| Dolibarr object | Table / element | Bloom analogue |
|-----------------|-----------------|----------------|
| `Societe` | third party | Customer / shop counterparty / supplier florist partner |
| Contact (`socpeople`) | people | Recipient, buyer, shop manager contact |
| `Product` | catalog SKU | Bouquet / product SKU (+ variants) |
| `Commande` | sales order | **Order** (ops unit of work) |
| `OrderLine` | line items | Composition lines / SKU qty |
| `Expedition` | shipment | Courier dispatch / delivery leg |
| `Facture` | invoice | Payment/settlement document |
| `Ticket` | support thread | Partial stand-in for inbox thread (email-centric) |
| `Project` | project | Campaign / event order grouping (optional) |
| `Entrepot` | warehouse | Physical shop stock location (not full shop tenant) |
| Category (`categorie`) | tags | Product/order taxonomy |

### 3.3 Commande (sales order) — important fields

From `htdocs/commande/class/commande.class.php`:

| Field | Meaning for Bloom |
|-------|-------------------|
| `ref`, `ref_client` / `ref_customer`, `ref_ext` | Internal ref, customer ref, **external marketplace ref** |
| `fk_soc` | Customer third party |
| `fk_statut` / `status` | **Fulfillment lifecycle** (see §5) |
| `billed` / `facture` | **Independent billing dimension** (0/1) |
| `date_livraison` / `delivery_date` | Planned delivery |
| `fk_shipping_method`, `fk_warehouse` | Delivery method, default warehouse |
| `source` | How order entered (phone, email…) — coarse |
| `module_source`, `pos_source` | POS / channel module key |
| `signed_status` | Signature workflow on document |
| `entity` | Company/tenant partition |
| `fk_projet` | Optional project link |
| Multicurrency totals | Cross-border pricing |
| Extrafields | Custom marketplace metadata |

### 3.4 Catalog & stock

- Products and services share product module; type flag product vs service.
- **Variants**, **barcodes**, **batches/lots/serials**, **BOM**, multi-warehouse stock.
- Stock movement timing is **configurable** (e.g. decrement on order validate vs on shipment validate via `STOCK_CALCULATE_ON_VALIDATE_ORDER` / `STOCK_CALCULATE_ON_SHIPMENT`).
- Relevance for floristry: variants + warehouse per shop is usable; “composition/recipe” can map to BOM or free text lines, but no native flower-window UX.

### 3.5 Parties model nuance

One **Societe** can be customer, prospect, and/or supplier flags — useful for B2B flower partners who both sell and supply. Not the same as multi-shop network membership.

---

## 4. UI / Information architecture

### 4.1 Shell

Classic **ERP left menu / top menu managers** (multiple menu managers; internal vs external user menus). Modules appear only when enabled. Home has **customizable dashboards** (boxes/widgets).

Typical top-level IA (when modules on):

```
Home (dashboard)
Third Parties
  Customers / Prospects / Suppliers / Contacts
Commercial / Sales
  Opportunities · Proposals · Orders · Contracts · Interventions
Products / Services
  Catalog · Stock · Warehouses · Inventory
Shipments / Logistics
Billing / Invoices · Payments · Bank
Tickets
Projects · Agenda
HR (optional)
Accounting (optional)
Tools (ECM, import/export, emailing)
Setup (modules, dictionaries, users/groups, extrafields)
```

### 4.2 Object card pattern (steal-worthy)

Nearly every business object uses the same card IA:

1. **Header** — ref, status badge(s), third party, totals  
2. **Action bar** — Validate / Create shipment / Create invoice / Send email / Generate PDF  
3. **Tabs** — Card · Contacts · Notes · Linked files · Linked objects · Agenda · Extrafields  
4. **Lines table** — editable in draft; rank reorder  
5. **Linked documents chain** — visual/list of origin and targets  

This **document-centric card** is the UX unit of Dolibarr.

### 4.3 List pattern

- Filterable lists with saved search tendencies, status filters, totals for money columns.
- Export / mass actions depending on module.
- UI is functional but **dated** vs Twenty/Espo modern SPA shells — dense tables, server-rendered PHP pages, progressive JS.

### 4.4 External / portal faces

- External users can get a reduced menu (customer portal–like).
- Public ticket track via `track_id`.
- Online signing for proposals; online payment URLs on commercial docs.
- TakePOS is a separate touch UI for retail, not ops board.

### 4.5 What is missing for Bloom IA

- No **unified messenger inbox** (threads across WA/TG/MAX).
- No **shop switcher** as first-class nav (entity switch only with MultiCompany).
- No **dual-lane board** (marketplace vs direct) as primary IA.
- No courier map / delivery slot board native to flowers.
- Analytics are report lists, not live multi-shop ops KPIs.

---

## 5. Workflows & statuses

### 5.1 Dual (actually multi) status dimensions — the main Bloom steal

Dolibarr does **not** collapse billing into order status. That is the critical pattern.

#### A) Order lifecycle (`Commande::STATUS_*` → `fk_statut`)

| Const | Value | Meaning |
|-------|------:|---------|
| `STATUS_CANCELED` | -1 | Canceled |
| `STATUS_DRAFT` | 0 | Draft `(PROV…)` ref |
| `STATUS_VALIDATED` | 1 | Validated / open |
| `STATUS_SHIPMENTONPROCESS` | 2 | Shipment in process (set when shipment validated) |
| `STATUS_CLOSED` | 3 | Closed (sent, billed or not) |

Methods: `create` → `valid` → shipment drives status 2 → `cloture` / `cancel` / `set_reopen` / `setDraft`.

Triggers: `ORDER_CREATE`, `ORDER_VALIDATE`, `ORDER_UNVALIDATE`, `ORDER_CLOSE`, `ORDER_CANCEL`, `ORDER_REOPEN`.

#### B) Billing flag (parallel dimension)

- Field: **`billed`** (also historically `facture` on reopen SQL).
- Independent of `fk_statut`: an order can be **Closed + not billed**, or validated and already linked to invoices.
- Reopen explicitly sets `facture=0`.

→ Bloom dual status analogue: **ops/fulfillment status ∥ payment/settlement status** (and potentially shop-network status as a third).

#### C) Signature dimension (tertiary, document legal)

`signed_status`: 0 none · 1 sender · 2 receiver · 9 all.

#### D) Shipment lifecycle (`Expedition::STATUS_*`)

| Const | Value | Meaning |
|-------|------:|---------|
| `STATUS_CANCELED` | -1 | Canceled |
| `STATUS_DRAFT` | 0 | Draft parcel |
| `STATUS_VALIDATED` | 1 | Ready to send |
| `STATUS_CLOSED` | 2 | Received / processed end |
| `STATUS_SHIPMENT_IN_PROGRESS` | 3 | Left warehouse / with courier |

Shipment validate updates origin order toward `STATUS_SHIPMENTONPROCESS` and may fire `SHIPPING_ORDER_SHIPMENTONPROCESS`.

Also: `billed` exists on shipment too; tracking_number + shipping_method_id; optional Delivery receipt submodule.

#### E) Ticket workflow (inbox-ish)

| Const | Value | Label |
|-------|------:|-------|
| `STATUS_NOT_READ` | 0 | Unread |
| `STATUS_READ` | 1 | Read |
| `STATUS_ASSIGNED` | 2 | Assigned |
| `STATUS_IN_PROGRESS` | 3 | In progress |
| `STATUS_NEED_MORE_INFO` | 5 | Need more info |
| `STATUS_WAITING` | 7 | On hold (optional dict flag) |
| `STATUS_CLOSED` | 8 | Solved/closed |
| `STATUS_CANCELED` | 9 | Canceled |

Assignment: `fk_user_assign`; public `track_id`; email threading via `email_msgid` / EmailCollector.

### 5.2 Commercial conversion workflows

| Flow | Mechanism |
|------|-----------|
| Quote → Order | `Commande::createFromProposal(Propal)` + `element_element` link; optional auto-validate `ORDER_VALID_AFTER_CLOSE_PROPAL` |
| Order → Shipment | Create Expedition from order lines (partial qty, multi-warehouse, batches) |
| Order → Invoice | Invoice from order; sets billed dimension |
| Clone | `createFromClone` |
| POS → Order | TakePOS writes `module_source` / `pos_source` |

### 5.3 Permissions on transitions

Advanced permissions pattern (example orders):

- Basic: `commande.creer`
- Advanced: `commande.order_advance.validate`, `order_advance.close`

Bloom should similarly gate **validate / close / refund / reassign shop** separately from “edit draft”.

### 5.4 Gaps vs Bloom dual-status sync

- No native **marketplace status ↔ internal status** mapping engine.
- Statuses are **hardcoded integer enums** in PHP classes (dictionaries only for some satellite enums like ticket type). Not a free-form status designer like some CRMs.
- Multi-party sync (network HQ vs shop) would require MultiCompany + custom modules/triggers — not out of box.

---

## 6. Integrations

### 6.1 First-party / built-in

| Integration | Notes |
|-------------|-------|
| **REST API** | Module Web Services API REST; explorer embedded; resources e.g. `thirdparties`, `products`, `orders`/`commandes`, `invoices`, `shipments`, `tickets` |
| Auth | Per-user **API key** header `DOLAPIKEY` |
| Multi-entity API | Header `DOLAPIENTITY: {id}` |
| **SOAP** | Legacy |
| **EmailCollector** | Mailbox rules → tickets / records |
| **Mass emailing** | Campaign-ish, not conversational inbox |
| **LDAP** | Directory auth/sync |
| **Click-to-Dial** | Telephony hooks |
| **Payments** | PayPal, Stripe, Paybox modules |
| **Agenda iCal/vCal** | Calendar sync surface |
| **Import/Export** | Data tools |
| **AI via API** | Mentioned in feature list (API-level assist) |
| **Social linking** | Light, not inbox |

### 6.2 Ecosystem (DoliStore)

- E-commerce bridges (WooCommerce, PrestaShop import modules, marketplace-ish addons like UltimateMarketPlace on wiki category).
- MultiCompany (paid, iNodbox).
- Accounting/country packs, carriers, etc.

### 6.3 What Bloom cannot get natively

- WhatsApp / Telegram / MAX channel connectors  
- Real-time websocket inbox  
- Flowwow/marketplace dual-write adapters (must build on REST + triggers)  
- Native event bus beyond triggers/hooks (no Kafka-style)  

### 6.4 Integration recommendation for Bloom if ever embedding Dolibarr

Prefer **Dolibarr as back-office ledger** (invoices, stock, accounting) behind Bloom ops UI via REST — not as primary agent desktop.

---

## 7. Multi-company / multi-shop

### 7.1 Stock vs paid module

| Layer | Capability |
|-------|------------|
| **Core `entity` column** | Data partition field on objects; `getEntity()` filters; ready for multi-tenant |
| **MultiCompany module** (DoliStore, editor Régis Houssin / iNodbox, product id 1619) | Manage **several companies in one installation / one DB**; entity switcher; shared or isolated directories depending on setup |
| **Warehouses (`Entrepot`)** | Multi-location stock — weak multi-shop if shops only need inventory isolation |
| **Users & groups** | Rights per module; sales rep restriction on third parties (`restrictiononfksoc`, commerciaux) |
| **External users** | Portal-limited visibility to own socid |

### 7.2 MultiCompany characteristics (from wiki + API docs)

- One unzip, one database, multiple legal entities/instances.
- Install into `/custom`, activate under Setup → Modules.
- API can pin entity with `DOLAPIENTITY`.
- Objects call `setEntity($this)` so create lands in correct entity under multicompany.
- **Not free core** — important product/licensing note for Bloom comparisons.

### 7.3 Fit to Bloom multi-shop

| Bloom multi-shop need | Dolibarr |
|-----------------------|----------|
| Shop as org unit with own orders | Entity ≈ company; heavier than “shop branch” |
| Shared network catalog | Possible via shared entities/config in MultiCompany — non-trivial |
| HQ sees all shops | Super-admin / multi-entity visibility patterns |
| Shop sees only own | Entity isolation + rights |
| Cross-shop transfer | Stock movements between warehouses more natural than entity-to-entity |
| Franchise vs marketplace seller | No first-class marketplace seller model |

**Verdict:** entity model is a solid **reference for tenant keys**, but MultiCompany is **legal multi-company ERP**, not flower **network multi-shop**. Bloom should implement lighter `shop_id` / org tree rather than full entity cloning.

---

## 8. STEAL for Bloom

Patterns worth taking (concrete):

1. **Parallel status dimensions**  
   Keep fulfillment status separate from payment/billed (and optionally from marketplace external status). Never encode “Paid” as a stage of “Assembling”.

2. **Document chain with links**  
   Order → Shipment(s) → Invoice as linked objects with independent refs and PDFs/`ref_ext` for marketplace IDs.

3. **Trigger/hook extension surface**  
   Domain events (`ORDER_VALIDATE` style) + UI hooks for modules — better than hardcoding integrations inside core screens.

4. **Partial shipment model**  
   Multiple expeditions per order with line qty, warehouse pick, tracking — maps to multi-courier / split delivery.

5. **Extrafields as first-class customization**  
   Avoid schema forks for every marketplace attribute; typed extra data on order/product.

6. **Fine-grained transition permissions**  
   Separate create vs validate vs close (advanced rights).

7. **Contact roles on documents**  
   Typed contacts (billing vs shipping vs assignee) via dictionary codes — useful for recipient vs payer vs shop florist.

8. **External ref fields**  
   `ref_ext` / `ref_client` dual identity for marketplace sync.

9. **Stock movement policy configuration**  
   When inventory decrements (accept vs ship) as a setting — floristry perishable rules may want different policies.

10. **Module on/off IA**  
    Enable only surfaces needed; Bloom MVP should hide unused cabinets.

11. **Ticket assignment + unread states**  
    Even if Bloom uses messengers, status set Unread → Assigned → In progress → Waiting customer is a proven ops inbox skeleton.

12. **API key + entity header pattern**  
    Simple integration auth; multi-tenant header for shop/network context.

---

## 9. AVOID

1. **Forking Dolibarr as Bloom core** — PHP monolith + ERP breadth fights messenger-first SPA ops UX.  
2. **Hardcoded integer status enums only** — fine for stable ERP docs; Bloom needs configurable dual maps (marketplace codes ↔ internal).  
3. **Treating MultiCompany as multi-shop** — wrong abstraction weight and paid dependency.  
4. **Ticket module as primary WA/TG inbox** — email/ticket semantics, not realtime chat, no channel adapters.  
5. **Server-rendered dense ERP chrome for shop floor** — florists need fast board/inbox; Dolibarr UI is accountant-friendly.  
6. **Collapsing shipment into order status only** — Dolibarr itself avoids this; don’t regress.  
7. **POS as marketplace intake model** — `module_source` is a string tag, not dual-channel ops design.  
8. **Assuming free multi-tenant SaaS** — multi-company is external; core is single-entity friendly.  
9. **Over-adopting accounting surface in MVP** — Dolibarr’s gravity pulls toward full ERP; Bloom MVP should stay ops-thin.  
10. **SOAP / legacy dual APIs** — prefer one clean REST/Graph style in Bloom.

---

## 10. Web MVP notes (structure MVP for `mvp/dolibarr/`)

When building the clickable structure MVP (`mvp/dolibarr/index.html`), mirror Dolibarr IA — **not** Bloom skin:

### Screens to prototype

| Screen | Key widgets |
|--------|-------------|
| Home dashboard | Module boxes: orders draft/validated, tickets unread, shipments to validate |
| Third parties list + card | Customer flags, contacts tab |
| Products list + card | Stock by warehouse, variants badge |
| Orders list | Filters: status, billed yes/no, ref_ext |
| **Order card** | Status badge + **Billed** badge side-by-side; lines; actions Validate / Ship / Invoice; tabs Contacts, Links, Files |
| Create shipment from order | Partial qty, warehouse, tracking |
| Shipment card | Own status lifecycle |
| Invoice stub | Linked from order |
| Tickets list + card | Unread → assign → thread messages (email style) |
| Setup strip | Modules toggles, users/groups (read-only mock) |
| Entity switcher mock | Label “MultiCompany (external)” disabled or demo |

### Interaction notes for MVP fidelity

- Show **two badges** on order: `Validated` + `Not billed`.  
- Linked objects strip: Propal → Order → Shipment → Invoice.  
- No WhatsApp panel — optionally a greyed “not in product” for honest benchmark.  
- Menu: Third Parties · Commercial · Products · Shipments · Tickets · Tools.

### Offline constraints

Standalone HTML/CSS/JS; labels in English module names (`Commande` can be shown as “Orders (commande)”).

---

## 11. Mapping: Dolibarr → Bloom

| Dolibarr concept | Bloom concept | Notes |
|------------------|---------------|-------|
| `Commande` | Order | Primary ops object |
| `fk_statut` order status | Fulfillment / shop ops status | Draft→Validate→In delivery→Done |
| `billed` | Payment / settlement status | Parallel dimension |
| Future: marketplace state | Network / channel status | **Third** dimension Bloom needs; Dolibarr lacks |
| `ref_ext` | Marketplace order id | Sync key |
| `Expedition` | Delivery / courier job | 1 order : n jobs |
| `Product` + warehouse | Catalog SKU + shop stock | Warehouse ≈ shop stock node |
| `Societe` | Customer (and/or partner shop as third party) | Not network shop tenant |
| `entity` / MultiCompany | Legal company / heavy tenant | Prefer Bloom `shop_id` + network org |
| `Ticket` + EmailCollector | Inbox thread (email only) | Replace with WA/TG/MAX unified inbox |
| `fk_user_assign` | Thread/order assignee | Keep |
| Extrafields | Custom order fields | Marketplace metadata |
| Triggers | Integration automations | Status sync webhooks |
| Groups/rights | Roles (dispatcher, florist, accountant) | Map carefully |
| TakePOS | Offline counter sales | Optional later |
| Agenda | Delivery calendar | Partial |
| Margins / reports | Analytics | Rebuild for multi-shop KPIs |

---

## 12. Fit score (Bloom) — 5.5 / 10

| Criterion (weight) | Score 1–10 | Rationale |
|--------------------|------------|-----------|
| Orders model | 8 | Mature sales order + lines + links |
| Dual status | 8 | Lifecycle ∥ billed (+ shipment status) |
| Multi-shop | 4 | Entity/MultiCompany ≠ shop network |
| Messenger inbox | 2 | Tickets/email only |
| Catalog & stock | 7 | Strong product/stock; not floristry UX |
| Analytics | 5 | Classic reports; no network rollups |
| Roles & auditability | 7 | Fine rights, triggers, document trail |
| Extensibility / API | 7 | REST + hooks + DoliStore |
| UX modernity for ops | 3 | ERP-dense, not agent realtime |
| Build-from vs learn-from | 4 | Learn-from only |

**Weighted qualitative total: ~5.5/10.**

### Recommendation

| Option | Verdict |
|--------|---------|
| Use Dolibarr as Bloom base | **No** |
| Steal domain patterns | **Yes** — dual status, document chain, partial ship, extrafields, triggers, ref_ext |
| Use as accounting sidecar | **Maybe** later via REST for invoices/stock |
| Benchmark ranking | Strong **ERP reference**; mid pack for Bloom-specific ops CRM |

---

## 13. Russian summary / рекомендации

**Dolibarr** — зрелый модульный ERP/CRM (PHP, GPL-3). Для Bloom это **не кандидат на ядро продукта**, а **референс доменной модели документов**.

### Что взять (STEAL)

- Двухмерный статус заказа: **жизненный цикл отдельно от оплаты (`billed`)**.  
- Цепочка **Заказ → Отгрузка(и) → Счёт** со связями и внешним `ref_ext`.  
- Частичные отгрузки, склады, трекинг.  
- Триггеры/хуки и extrafields вместо форка схемы.  
- Роли контактов на документе и раздельные права на validate/close.

### Чего избегать (AVOID)

- Форк монолита Dolibarr.  
- MultiCompany как модель «сети цветочных магазинов».  
- Ticket как замена WA/TG/MAX inbox.  
- ERP-перегруженный UI для флористов и диспетчеров.

### Для web MVP benchmark

Сверстать shell с **двумя бейджами статуса на карточке заказа** и linked-objects цепочкой — это главный didactic takeaway для Bloom dual-status UX.

---

## 14. Citations & further reading

- Repo: https://github.com/Dolibarr/dolibarr  
- REST API wiki: https://wiki.dolibarr.org/index.php/Module_Web_Services_API_REST_(developer)  
- MultiCompany wiki: https://wiki.dolibarr.org/index.php/Module_MultiCompany  
- DoliStore MultiCompany: https://www.dolistore.com/product.php?id=1619  
- Source anchors (develop):  
  - `htdocs/commande/class/commande.class.php` — order statuses, billed, triggers  
  - `htdocs/expedition/class/expedition.class.php` — shipment statuses  
  - `htdocs/ticket/class/ticket.class.php` — ticket workflow  
  - `htdocs/core/class/commonobject.class.php` — entity, links, contacts, extrafields  

---

*Analyzer artifact for Bloom CRM benchmark · id=`dolibarr` · path=`reports/dolibarr-analysis.md`*
