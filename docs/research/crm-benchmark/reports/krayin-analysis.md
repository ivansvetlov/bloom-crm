# Krayin CRM — Bloom Benchmark Analysis

| Field | Value |
|-------|--------|
| **id** | `krayin` |
| **Product** | Krayin CRM |
| **Vendor** | Webkul |
| **Repo** | https://github.com/krayin/laravel-crm |
| **License** | MIT (core OSS forever free) |
| **Stack** | Laravel 12 / PHP 8.3+ / Vue 3 / Vite / Tailwind / MySQL 8+ |
| **Type** | Web admin CRM (self-host + commercial cloud/extensions) |
| **Branch reviewed** | `2.2` (default; latest release family **v2.2.4**, 2026-07-20) |
| **GitHub signal** | ~23.5k stars, ~1.5k forks, active maintenance |
| **Demo** | https://demo.krayincrm.com |
| **User docs** | https://docs.krayincrm.com |
| **Dev docs** | https://devdocs.krayincrm.com |
| **Product site** | https://krayincrm.com |
| **Review date** | 2026-08-01 |
| **Bloom context** | Flower multi-shop ops CRM; multi-tenant patterns; messaging extensions |

---

## 1. Overview / Positioning

Krayin is a **classic B2B sales CRM** built as a modular Laravel application (Webkul package architecture, same family as Bagisto e‑commerce). Target users are **SMEs and enterprise sales teams** who need:

- Lead → opportunity lifecycle with **Kanban pipelines**
- Persons / organizations
- Quotes (proposals)
- Email-centric interaction (IMAP/SMTP + templates)
- Activities (calls, meetings, notes) + calendar
- Products / light warehouses
- Role-based ACL, groups, custom attributes, workflows, webhooks, web forms

It is **not** an order-ops / fulfillment / multi-shop network cabinet. There is no first-class **Order** entity, no marketplace dual-intake, no dual parallel status dimensions (e.g. fulfillment vs payment), and no built-in messenger inbox (WhatsApp is a **paid** commercial extension).

**Positioning for Bloom research:** high value as a **reference implementation** of Laravel modular CRM packages, pipeline/stage modeling, ACL/groups, and (separately, commercial) multi-tenant SaaS domain isolation — not as a drop-in product base for Bloom.

### Key product claims (official)

- Free & open-source under MIT
- Modular package approach (`packages/Webkul/*`)
- Custom attributes, ACL, Kanban leads, dashboard
- Email parsing (Sendgrid mentioned; IMAP via `webklex/laravel-imap`)
- Commercial add-ons: Multi-Tenant SaaS, WhatsApp, VoIP, Cloud Hosting

### Requirements (self-host)

| Resource | Minimum |
|----------|---------|
| Server | Apache 2 or NGINX |
| RAM | 3 GB+ |
| PHP | 8.3+ |
| Composer | 2.5+ |
| DB | MySQL 8.0.32+ |
| Install | `composer create-project` + `php artisan krayin-crm:install` |
| Admin URL | `/admin/login` (demo defaults: admin@example.com / admin123) |

---

## 2. Architecture

### 2.1 High-level shape

```
laravel-crm (app shell)
├── app/ bootstrap/ config/ routes/ public/   # thin Laravel host
└── packages/Webkul/
    ├── Core, Admin, Installer, User
    ├── Lead, Contact, Quote, Product, Warehouse
    ├── Activity, Email, EmailTemplate
    ├── Attribute, Tag, Automation, Marketing
    ├── DataGrid, DataTransfer, WebForm
    └── GoogleContact
```

- **Concord-style module loading** (`konekt/concord`) + Webkul service providers.
- **Repository pattern** (`prettus/l5-repository`): models behind contracts/proxies (`LeadProxy`, `PersonProxy`, …).
- **Custom attributes** via shared `CustomAttribute` trait on leads, persons, organizations, products, quotes, warehouses.
- **Admin UI**: Laravel Blade + **Vue 3** islands (Vite, Tailwind, vee-validate, vuedraggable, vue-cal, Chart.js funnel).
- **API tokens**: Laravel Sanctum on `User`.
- **Exports/PDF**: maatwebsite/excel, dompdf/mpdf.
- **Testing**: Pest 3; formatting: Laravel Pint.

Agent/contributor guidance (`AGENTS.md`) is explicit: **extend via new packages under `packages/Webkul/`, do not edit core**; migrations only for schema; follow existing module layout (Providers, Models, Contracts, Repositories, Http, Routes, Migrations, Resources/views, Config).

### 2.2 Module map (domain ownership)

| Package | Responsibility |
|---------|----------------|
| **Lead** | Leads, pipelines, stages, sources, types, lead↔product lines, lead tags, lead quotes |
| **Contact** | Persons, organizations |
| **Quote** | Quotes, quote items, billing/shipping, totals |
| **Product** | Catalog SKUs used on leads/quotes |
| **Warehouse** | Inventory locations (settings-level) |
| **Activity** | Calls/meetings/notes; polymorphic links to lead/person/product/warehouse |
| **Email** | Mailboxes: inbox/draft/outbox/sent/trash; link to leads |
| **Attribute** | Unlimited custom fields per entity type |
| **Automation** | Workflows, webhooks |
| **Marketing** | Events, campaigns |
| **WebForm** | Public lead capture forms |
| **User** | Users, roles, groups, view_permission |
| **Admin** | Menu, ACL matrix, configuration, DataGrid UI shell |
| **DataTransfer** | Import/export |

### 2.3 Frontend / IA shell

Config-driven sidebar from `packages/Webkul/Admin/src/Config/menu.php` (keys → routes → sort → icons). ACL is a large parallel matrix (`acl.php`). This is a strong **declarative IA** pattern: nav and permissions evolve together.

### 2.4 Extensibility

- New CRM package generator (`krayin/krayin-package-generator` in dev).
- Events/listeners documented for deeper hooks.
- Webhooks + workflows for process automation without code.
- Commercial marketplace of extensions (SaaS tenancy, WhatsApp, VoIP).

**Implication for Bloom:** architecture is **fork-friendly if you stay in Laravel/PHP**, but domain is sales-native. Bloom would re-implement most packages (Order, Shop, Messenger, dual status) rather than “configure Krayin.”

---

## 3. Domain Model

### 3.1 Core objects

```
Organization 1──* Person 1──* Lead *──1 User (owner)
                     │          │
                     │          ├── Source, Type
                     │          ├── Pipeline → Stage(s) [code, name, probability, sort]
                     │          ├── * Product lines (lead_products)
                     │          ├── * Quotes (lead_quotes)
                     │          ├── * Activities, * Emails, * Tags
                     │          └── status / lost_reason / closed_at / expected_close_date
                     │
Quote *──1 Person, *──* Lead
  └── QuoteItem* (products, qty, price, tax, discount)
Product (SKU catalog)
Warehouse (settings inventory)
Activity (type, schedule, is_done) *──* Lead|Person|Product|Warehouse
User *──1 Role, *──* Group; view_permission
```

### 3.2 Lead (primary deal-like object)

From `Webkul\Lead\Models\Lead` + migrations:

| Field | Notes |
|-------|--------|
| `title`, `description` | Deal headline |
| `lead_value` | Monetary opportunity value |
| `status` | Boolean-ish lifecycle flag |
| `lost_reason`, `closed_at` | Terminal state metadata |
| `expected_close_date` | Forecast date |
| `user_id` | Sales owner (nullable in later migrations) |
| `person_id` | Required contact link |
| `lead_source_id` | Channel (web, phone, …) |
| `lead_type_id` | e.g. new vs existing business |
| `lead_pipeline_id` | Which funnel |
| `lead_pipeline_stage_id` | Current stage |
| **computed** `rotten_days` | Days past pipeline `rotten_days` if not won/lost |

**There is no Order, Shipment, Payment, Shop, or Thread entity in core.**

### 3.3 Pipeline / Stage

- **Pipeline** (`lead_pipelines`): `name`, `rotten_days`, `is_default`
- **Stage** (`lead_pipeline_stages`): `code`, `name`, `probability`, `sort_order`, FK to pipeline
- Terminal stage codes treated specially: **`won` / `lost`** (rotten calculation skips them)
- Multiple pipelines supported; dashboard multi-pipeline enhancements in 2.2.x

### 3.4 Person / Organization

- **Person**: name, emails[], contact_numbers[], job_title, user_id (owner), organization_id, unique_id
- **Organization**: B2B company container for persons
- Contact detail surfaces activities, notes, emails, related leads in a unified timeline (product UX)

### 3.5 Quote

- Subject, description, billing/shipping addresses (JSON), discount/tax/adjustment, sub/grand totals, expired_at
- Items collection; linked to person + many leads
- PDF-friendly commercial proposal, not an ops work order

### 3.6 Activity

- Types for sales follow-up (call, meeting, note, etc.)
- Schedule range, done flag, participants, files
- Calendar UI with drag-and-drop (2.2.1+)
- **Not** a multi-channel conversation thread

### 3.7 User / ACL / Group

- **Role**: permission_type all|custom + permission keys from ACL config
- **Group**: team segmentation for visibility
- **User.view_permission**: scopes record visibility (individual / group patterns; 2.2.x improved group selection)
- Groups are **team ACL**, not multi-shop tenancy

### 3.8 Custom attributes

Entity types with EAV-style custom fields: leads, persons, organizations, products, quotes, warehouses.

### 3.9 Mapping: Krayin → Bloom

| Krayin concept | Bloom concept | Fit |
|----------------|---------------|-----|
| Lead | Order / deal card | Weak rename — different lifecycle |
| Pipeline stage | Single status dimension | Partial — Bloom needs **dual** statuses |
| Person | Customer / recipient | Strong |
| Organization | B2B client / network partner | Partial (not flower shop) |
| Source | Marketplace vs direct intake | Steal pattern, not data model |
| Quote | Commercial proposal / estimate | Optional for B2B flower accounts |
| Product | Catalog SKU / bouquet template | Partial |
| Warehouse | Shop stock location | Weak — not multi-shop org unit |
| Group | Team / role segment | Partial — not shop isolation |
| User + Role ACL | Staff permissions | Strong |
| Mail inbox | Messenger inbox | Weak channel (email ≠ chat) |
| Activity | Timeline events | Strong pattern |
| Workflow / webhook | Ops automation | Strong |
| WebForm | Public order/lead form | Partial |
| Tenant (SaaS ext.) | Network / franchise isolation | Strong **as pattern**, paid only |
| WhatsApp ext. | Messenger channel | Strong **as product idea**, paid only |

---

## 4. UI / Information Architecture

### 4.1 Primary nav (from `menu.php`)

| Sort | Module | Children / notes |
|------|--------|------------------|
| 1 | **Dashboard** | Pipeline metrics, activities, KPIs |
| 2 | **Leads** | Kanban + list; stage drag; won/lost |
| 3 | **Quotes** | Proposal list/detail |
| 4 | **Mail** | Inbox, Draft, Outbox, Sent, Trash |
| 5 | **Activities** | List + calendar |
| 6 | **Contacts** | Persons, Organizations |
| 7 | **Products** | Catalog |
| 8 | **Settings** | Nested hub (below) |
| 9 | **Configuration** | System / locale / mail / powered-by |
| 10 | **Help** | Support tab (newer) |

### 4.2 Settings hub (IA depth)

- **User:** Groups, Roles, Users  
- **Lead:** Pipelines, Sources, Types  
- **Inventory:** Warehouses  
- **Automation:** Attributes, Email templates, Events, Campaigns, Webhooks, Workflows, Data transfer  
- **Other:** Tags  

This is a clean **settings taxonomy**: identity → lead taxonomy → inventory → automation → misc. Good reference for Bloom Settings IA (shops, statuses, channels, automations).

### 4.3 UX patterns of note (2.2)

- **Kanban leads** with infinite scroll, stage columns, rotten indicators, multi-pipeline dashboard
- **Quick Add** tabbed modal: Lead / Person / Organization / Product / Email in one entry point
- **Quick Attribute** on lead form
- **Sidebar collapse** remembered (Bagisto-like)
- **Global / mega search** across modules
- Contact + lead detail **timeline** of activities/emails/notes
- Responsive polish ongoing; security fixes in recent releases (IDOR, XSS, SQLi, upload CVE)

### 4.4 What Bloom should notice in IA

- Sales modules dominate top nav; ops surfaces absent  
- Mail is first-class, messenger is not  
- Settings put pipelines next to sources/types — good for configurable status dictionaries  
- No shop switcher / network context in chrome  

---

## 5. Pipelines / Leads / Quotes

### 5.1 Lead lifecycle

1. Capture (manual, web form, email, WhatsApp commercial, import)
2. Assign owner + person + source + type + pipeline + stage
3. Move stages on Kanban (probability per stage)
4. Attach products, quotes, activities, emails, tags
5. Mark **won** or **lost** (lost_reason, closed_at)
6. Rotten lead alerting via pipeline `rotten_days`

**Single primary status dimension** = pipeline stage (+ terminal won/lost + boolean status). No parallel “payment status” or “fulfillment status.”

### 5.2 Pipelines

- Configurable multi-pipeline  
- Stages ordered with probability for forecasting  
- Default pipeline flag  
- Rotten days policy per pipeline  
- Useful for Bloom **order stages**, but Bloom must **not** collapse fulfillment + payment into one board without dual-status design

### 5.3 Quotes

- Separate module linked M:N to leads  
- Line items, tax, discount, addresses, expiry  
- Share/view quote with person  
- Maps better to B2B estimates than same-day flower delivery ops  

### 5.4 Sources & Types

- **Sources** = acquisition channel dictionary (steal for marketplace / direct / walk-in / Telegram)  
- **Types** = lead classification (new vs existing business)  

### 5.5 Products on leads

- `lead_products` lines attach catalog products to opportunity value  
- Catalog is sales-oriented, not production/assembly BOM for florists  

### 5.6 Status & workflow model (summary)

| Mechanism | Behavior |
|-----------|----------|
| Stage | Primary linear/Kanban state |
| Won/Lost | Terminal outcomes |
| Activity.is_done | Task completion |
| Workflows | Rule-based automation steps |
| Webhooks | External system sync |
| Tags | Soft segmentation |

**Dual-status gap:** Bloom needs at least two independent dimensions (e.g. **ops/fulfillment** vs **payment/settlement**, and possibly **shop status** vs **network status**). Krayin models one sales funnel well and nothing dual.

---

## 6. Multi-tenant / Multi-shop

### 6.1 Open-source core

**Single-tenant by default.** One app instance → one company database. Isolation mechanisms inside:

- User roles (ACL keys)
- Groups + `view_permission` (record visibility)
- Lead ownership (`user_id`)

**Not multi-shop:** no Shop entity, no branch hierarchy, no per-shop inventory ops board, no shared network super-admin in OSS core.

GitHub discussion (#851): single-database multi-tenancy was **not on OSS roadmap**; commercial path preferred.

### 6.2 Commercial Multi-Tenant SaaS extension

| Aspect | Detail |
|--------|--------|
| Product | Krayin CRM Multi Tenant SaaS (Webkul paid) |
| Model | Superadmin + tenants with **personal domains / subdomains** |
| Isolation | Domain middleware (`ValidatesDomain`); tenants get full CRM feature set |
| Superadmin | Tenants CRUD, roles, agents, filters, locale/RTL |
| Tenant self-reg | Register company → domain/CNAME → own admin dashboard |
| DNS | Wildcard + CNAME mapping |
| Install note | Fresh setup; existing data wiped on SaaS install path |
| Versioning | Ext docs reference ~2.1.x support line (verify against core 2.2 before production) |

**Tenant panel modules (same sales CRM):** Leads, Quotes, Mail, Activities, Contacts, Products, Settings, Configuration.

### 6.3 Messaging extensions (commercial)

| Extension | Role |
|-----------|------|
| **WhatsApp** | Lead generation via WhatsApp number; not a full omnichannel inbox in OSS |
| **VoIP** | Trunk/inbound telephony |

### 6.4 Bloom multi-tenant takeaways

| Pattern | Krayin | Bloom need |
|---------|--------|------------|
| Hard tenant isolation by domain | SaaS paid ext. | Optional for multi-network franchise; usually **multi-shop inside one network** is enough |
| Soft isolation (groups/owners) | OSS core | Useful for staff scopes |
| Shop as first-class org unit | Missing | **Required** |
| Shared catalog + per-shop stock | Weak warehouse only | Required |
| Superadmin of network vs shop admin | SaaS superadmin ≠ shop ops | Map carefully: network HQ vs florist shop |

**Рекомендация (RU):** не брать OSS Krayin как multi-shop каркас. Брать **идеи**: domain-based isolation (если SaaS), ACL matrix, groups/view_permission. Shop isolation в Bloom проектировать отдельно (shop_id scoping + dual roles network/shop).

---

## 7. Communication / Inbox

| Channel | Support |
|---------|---------|
| Email (IMAP/SMTP, templates, folders) | First-class in core |
| Activities timeline | First-class |
| WhatsApp | Paid extension; lead-oriented |
| VoIP | Paid extension |
| Telegram / multi-thread messenger | Not present |
| Order-linked chat assignment | Not present |

Mail menu mirrors classic MUA: inbox/draft/outbox/sent/trash. Good for B2B email sales; **poor model for Bloom messenger inbox** (threads, quick replies, shop assignment, order deep-link).

---

## 8. Analytics

- Admin **dashboard**: leads, activities, customers/products at a glance  
- Stage **probability** + lead_value for pipeline forecasting  
- **Funnel** charts (chartjs funnel dependency)  
- Kanban **previous month sales** enhancement (2.2.4)  
- Multi-pipeline dashboard support  

**Gap for Bloom:** no ops KPIs (SLA delivery, shop load, courier, GMV marketplace vs direct, dual-status rollups). Analytics are sales CRM, not network ops.

---

## 9. Extensibility / API / Self-host

| Topic | Notes |
|-------|--------|
| Self-host | First-class; Docker docs exist |
| Cloud | Paid Krayin Cloud Hosting |
| API | Sanctum tokens on users; admin is primarily session UI; Fractal for transformers |
| Packages | Concord modules; clear skill docs for package development |
| Workflows/Webhooks | No-code automation surface |
| Import/Export | DataTransfer package |
| License risk | Core MIT; multi-tenant + messaging often commercial |

Recent security attention (IDOR, XSS, upload CVE, SQLi filters) shows active hardening — positive for project health, caution for rushed forks.

---

## 10. STEAL (for Bloom)

Patterns and ideas worth borrowing — not code dump:

1. **Declarative menu + ACL configs**  
   Single source of truth for nav keys and permissions (`menu.php` / `acl.php`). Bloom should keep IA and RBAC in sync the same way.

2. **Modular package boundaries**  
   Lead / Contact / Quote / Activity as isolated packages with contracts + repositories. Bloom can mirror: `Order`, `Shop`, `Messenger`, `Catalog`, `Network`.

3. **Pipeline as configurable dictionary**  
   Stages with `code`, `name`, `probability`, `sort_order`, `rotten_days`. Steal for **one** status dimension; **duplicate the pattern** for a second dimension (fulfillment vs payment).

4. **Sources dictionary**  
   Explicit acquisition channels — map to marketplace / direct / phone / chat.

5. **Kanban + list dual view** on primary work object  
   Ops boards for flower orders benefit from same dual presentation.

6. **Rotten / SLA aging**  
   Pipeline rotten_days → Bloom delivery SLA breach indicators.

7. **Quick Add multi-entity modal**  
   Fast capture across related entities from one chrome control.

8. **Custom attributes EAV**  
   Per entity extensibility without migrations for shop-specific fields (bouquet notes, occasion, delivery window flags).

9. **Activity timeline on detail pages**  
   Unified history: status changes, messages, courier events, payments.

10. **Groups + view_permission**  
    Soft data scopes for call-center vs shop staff (before hard multi-tenant).

11. **Workflows + webhooks**  
    External marketplace webhooks → order create; status change → notify messenger.

12. **Web forms for intake**  
    Public form → lead/order with source tagging.

13. **Commercial tenancy productization**  
    Superadmin / tenant / domain model is a useful **product** reference if Bloom ever sells white-label networks — even if implemented differently (row-level shop_id vs separate DBs).

14. **WhatsApp-as-lead-channel product idea**  
    Messaging as acquisition + conversation surface is critical for flower retail; implement natively in Bloom, not as afterthought.

---

## 11. AVOID (for Bloom)

1. **Using Lead as Order**  
   Lead lifecycle (won/lost, probability) does not model delivery windows, florist assignment, courier, COD, marketplace claims.

2. **Single status funnel only**  
   Collapsing all state into one Kanban will fight dual-status ops (payment vs fulfillment, shop vs network).

3. **Email-first inbox as messenger substitute**  
   Folders (inbox/sent/trash) ≠ threads, assignment queues, multi-channel unified inbox.

4. **Groups as shops**  
   User groups are permission scopes, not operational org units with hours, geo, catalog, balance.

5. **Warehouse as multi-shop**  
   Inventory warehouse ≠ florist shop with ops board and P&L.

6. **Relying on paid multi-tenant for core multi-shop**  
   Bloom’s primary tenancy is **many shops inside one network**, not many unrelated CRM tenants. Domain-per-tenant SaaS is a different problem.

7. **Forking Krayin as the Bloom codebase**  
   You would rewrite domain + UI; better steal patterns and build Bloom domain-first (or choose a closer base). PHP/Laravel is fine stack-wise if team owns it — but Krayin’s sales packages become dead weight.

8. **Quote-centric commercial flow for same-day retail**  
   Quotes/PDF proposals add friction for high-velocity flower orders.

9. **Assuming OSS = full feature parity with marketing site**  
   Multi-tenant, WhatsApp, VoIP are monetized extensions.

10. **Ignoring recent security history**  
    If evaluating any Laravel CRM fork, budget for ACL/IDOR audits early.

---

## 12. Web MVP Notes

Guidance for structure MVP under `mvp/krayin/index.html` (Analyzer/MVP builder track):

### Screens to prototype (Krayin IA, not Bloom skin)

1. **Shell** — collapsible sidebar: Dashboard, Leads, Quotes, Mail, Activities, Contacts, Products, Settings, Configuration  
2. **Dashboard** — KPI cards + pipeline summary + recent activities  
3. **Leads Kanban** — columns = stages; cards with value, owner, rotten badge; toggle list view  
4. **Lead detail** — person, stage, products, quotes, activity timeline, email thread stub  
5. **Quotes list/detail** — line items, totals, status/expiry  
6. **Mail** — folder list + message pane (classic)  
7. **Activities** — calendar + list  
8. **Contacts** — Persons / Organizations tabs  
9. **Settings hub** — tiles for Users, Roles, Groups, Pipelines, Sources, Types, Warehouses, Attributes, Workflows, Webhooks, Tags  
10. **Pipeline settings** — ordered stages editor (code/name/probability)

### Explicit non-goals for Krayin MVP

- No shop switcher  
- No dual status chips  
- No messenger thread UI (optional footnote: “WhatsApp = commercial”)  
- Label header: **Krayin CRM · id: krayin**  

### Bloom contrast callouts (footer or notes panel)

- “Missing: multi-shop, orders, dual status, messenger”  
- “Steal: menu+ACL config, pipeline stages, sources, quick add”

---

## 13. Fit Score (Bloom) — **5 / 10**

| Criterion (weight) | Score 1–10 | Comment |
|--------------------|------------|---------|
| Order / deal model | 4 | Strong lead/pipeline; no order/ops |
| Multi-shop / tenant | 5 | Paid SaaS multi-tenant solid; OSS multi-shop absent |
| Messenger / inbox | 4 | Email strong; chat commercial/weak |
| Status / workflow | 6 | Excellent single pipeline; no dual status |
| Analytics / ops KPIs | 4 | Sales dashboard only |
| Extensibility / self-host | 8 | MIT, packages, workflows, active core |
| UX IA quality | 7 | Clear modular admin; Kanban + Quick Add |
| Bloom domain proximity | 3 | Flower network ops is a different product |

### Weighted qualitative score: **5 / 10**

**Interpretation**

- **5** = solid **pattern library** (architecture, pipeline, ACL, settings IA, optional SaaS tenancy ideas), weak **product fit** for Bloom ops cabinet.  
- Higher than pure marketing CRMs because of modular Laravel quality, quotes, warehouses, workflows, and explicit multi-tenant *product* thinking.  
- Lower than order-centric ERPs (ERPNext/Dolibarr class) for multi-entity ops and inventory-as-business-unit.  
- **Do not adopt as Bloom foundation.** **Do mine** STEAL list into Bloom IA and domain design.

### Score sub-dimension (research matrix helper)

| Bloom surface | Krayin fit |
|---------------|------------|
| Marketplace + direct orders | Low (sources only) |
| Multi-shop | Low OSS / Medium paid SaaS (wrong grain) |
| Messenger inbox | Low–Medium (WhatsApp paid) |
| Dual status | Low |
| Analytics | Medium sales / Low ops |

---

## 14. Bloom Recommendations (EN + RU)

### English

- Treat Krayin as **reference CRM architecture**, not a candidate to white-label into Bloom.  
- Copy **pipeline stage schema + rotten SLA + sources** into Bloom status dictionaries — then **split into dual dimensions**.  
- Design Bloom chrome with **shop context switcher** (absent in Krayin).  
- Build **messenger-native inbox** with order deep links; do not start from email folders.  
- If network SaaS isolation is needed later, study Webkul’s **superadmin / domain tenant** product UX — implement with Bloom’s shop/network model, not lead packages.

### Русский

- **Krayin — хороший учебник по Laravel-CRM-модульности**, но плохой каркас для цветочного multi-shop ops.  
- Украсть: конфиг меню+ACL, стадии воронки, sources, Quick Add, timeline активностей, workflows/webhooks, custom attributes.  
- Не тащить: Lead-как-заказ, один статус на всё, groups-как-магазины, email-inbox-как-мессенджер.  
- Multi-tenant SaaS Webkul — про **разных клиентов CRM на доменах**, а не про **сеть магазинов одного оператора**. Для Bloom важнее `shop_id` + роли network/shop.  
- Оценка **5/10**: держать в shortlist как **паттерн-референс**, не как base fork.

---

## 15. Sources Used

| Source | URL |
|--------|-----|
| GitHub repo (branch 2.2) | https://github.com/krayin/laravel-crm |
| README / composer / packages | raw GitHub 2.2 |
| Lead/Quote/Person/Activity/User models | `packages/Webkul/*/src/Models` |
| Admin menu | `packages/Webkul/Admin/src/Config/menu.php` |
| CHANGELOG 2.2.x | repo root |
| AGENTS.md | repo root |
| Dev docs intro | https://devdocs.krayincrm.com/2.0/introduction/ |
| User docs settings | https://docs.krayincrm.com/2.x/settings/ |
| Multi-tenant SaaS guide | https://webkul.com/blog/krayin-crm-multi-tenant-saas-documentation/ |
| Product site / extensions | https://krayincrm.com |
| Demo | https://demo.krayincrm.com |

---

## 16. One-line verdict

**Krayin is a mature MIT Laravel/Vue sales CRM with excellent modular packaging and pipeline UX; multi-tenant and messaging live mostly in paid extensions — use it as a pattern source for Bloom (score 5/10), not as the Bloom product base.**
