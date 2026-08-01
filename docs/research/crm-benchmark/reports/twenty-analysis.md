# Twenty CRM — Bloom Benchmark Analysis

| Field | Value |
|-------|--------|
| **id** | `twenty` |
| **Product** | Twenty |
| **Tagline** | Open alternative to Salesforce, designed for AI / #1 open-source CRM |
| **Repo** | https://github.com/twentyhq/twenty |
| **Website** | https://twenty.com |
| **Docs** | https://docs.twenty.com |
| **Demo / cloud** | https://app.twenty.com |
| **Figma** | https://www.figma.com/file/xt8O9mFeLl46C5InWwoMrN/Twenty |
| **License** | AGPL-3.0 |
| **Type** | Web SPA (self-host + managed cloud) |
| **Stack** | TypeScript monorepo (Nx) · NestJS · React · PostgreSQL · Redis · BullMQ · GraphQL/REST · ClickHouse (analytics/events) |
| **Stars (approx.)** | ~54k (GitHub, research date 2026-08-01) |
| **Activity** | Very active (14k+ commits; continuous main-branch pushes) |
| **Review date** | 2026-08-01 |
| **Sources** | Official docs (user guide + developers), README, package monorepo layout, marketing site, public API docs |

**Bloom lens:** Flower multi-shop ops CRM — marketplace + direct orders, multi-shop isolation, messenger inbox, dual status, ops analytics. Twenty is primarily a **modern GTM / Salesforce-class CRM**, not a shop-ops system; its value for Bloom is **UX bar, custom objects, views, workflows, and multi-workspace patterns**.

---

## 1. Overview / Positioning

### What Twenty is

Twenty positions itself as a **developer-owned, customizable CRM platform**: “the CRM you build, ship, and version like the rest of your stack.” It targets technical GTM teams who outgrow rigid SaaS CRMs and want:

- Standard CRM objects (People, Companies, Opportunities, Tasks, Notes)
- Unlimited custom objects/fields without pricing penalties
- No-code **workflows** + code-as-config **Apps** (TypeScript SDK)
- Notion-like modern UI with kanban/table/calendar views
- Email/calendar sync (Google/Microsoft) on core objects
- AI chat + AI agents (workspace-scoped, role-bound)
- Schema-driven REST + GraphQL APIs per workspace

### Target user

- RevOps / sales ops / founders building internal GTM systems
- Engineering teams that want CRM as **infrastructure** (versioned apps, MCP, CLI)
- Mid-market orgs replacing Salesforce/HubSpot for customization speed, not for ERP/inventory

### What it is *not*

- Not an ERP: no native stock, POS, multi-warehouse, purchase orders, or shop fulfillment
- Not an omnichannel support desk: no first-class WhatsApp/Telegram/MAX unified inbox
- Not multi-company accounting/ops (shops are not a first-class entity; isolation is **workspace**-level)

### Bloom relevance (summary)

| Bloom need | Twenty strength |
|------------|-----------------|
| Modern UX benchmark | ★★★★★ — clean tables, kanban, Cmd+K, record page widgets |
| Custom objects (Order, Shop, Courier…) | ★★★★★ — first-class custom objects + code-defined apps |
| Workflows / status automation | ★★★★ — visual workflows; stage = Select field + kanban |
| Multi-workspace / tenant model | ★★★★ — workspace isolation; schema-per-tenant APIs |
| Orders / fulfillment ops | ★★ — only via custom objects; no ops primitives |
| Messenger inbox | ★★ — email/calendar, not WA/TG threads |
| Multi-shop hierarchy *inside* one org | ★★ — model as custom object + row-level (premium) or views |

**Overall fit for Bloom as product base:** low–medium.  
**Overall fit as UX / platform benchmark:** very high.

---

## 2. Architecture

### 2.1 Monorepo shape (Nx + Yarn 4)

Key packages under `packages/`:

| Package | Role |
|---------|------|
| `twenty-server` | NestJS API, workers, TypeORM, GraphQL Yoga, queue worker, migrations |
| `twenty-front` | React SPA (Jotai, Linaria, Lingui i18n) |
| `twenty-ui` | Shared design system / UI primitives |
| `twenty-shared` | Shared types/utilities |
| `twenty-sdk` / `twenty-client-sdk` / `twenty-cli` / `create-twenty-app` | Apps framework: define objects/views/logic as code, publish to workspaces |
| `twenty-emails` | Transactional email templates |
| `twenty-docker` | Self-host packaging |
| `twenty-docs` / `twenty-website` | Product docs & marketing |
| `twenty-zapier` | Zapier integration package |
| `twenty-front-component-renderer` | Renders app-provided React components inside host UI |

Runtime stack (from README + `twenty-server` deps):

- **API:** NestJS 11, GraphQL (Yoga + nestjs-query), REST
- **DB:** PostgreSQL (`pg` + TypeORM)
- **Cache/queues:** Redis, BullMQ workers (`worker:prod`)
- **Analytics store:** ClickHouse client + migrations (events/metrics path)
- **Auth:** JWT, Google/Microsoft OAuth, SAML/SSO (plan-gated), sessions
- **Storage/email:** S3-compatible, SES, IMAP (imapflow), Google/Microsoft Graph
- **AI:** Vercel AI SDK multi-provider (`@ai-sdk/*`), agents in workflows
- **Observability:** Sentry, OpenTelemetry metrics
- **Node:** ^24.5; package manager Yarn 4

### 2.2 Runtime topology (self-host mental model)

```
Browser (twenty-front)
        │
        ▼
   NestJS API (twenty-server)
   ├── GraphQL / REST  (schema generated from workspace metadata)
   ├── Metadata API    (objects, fields, relations)
   └── Auth / files / webhooks
        │
        ├── PostgreSQL  (core + per-workspace data/schema)
        ├── Redis       (cache, sessions, pub/sub, BullMQ)
        ├── Worker      (async jobs, workflows, sync)
        └── ClickHouse  (optional analytics path)
```

Production scripts imply multi-process: `start:prod` (API) + `worker:prod` (queues) + DB migrate commands.

### 2.3 Schema-driven platform core

The architectural centerpiece for Bloom benchmarking:

1. **Metadata layer** — objects, fields, relations, views, layouts stored as workspace metadata  
2. **Generated APIs** — adding object `Invoice` immediately yields REST/GraphQL endpoints using *your* names (no opaque static OpenAPI for all tenants)  
3. **Core vs Metadata APIs**
   - **Core:** `/rest/`, `/graphql/` — CRUD on records  
   - **Metadata:** `/rest/metadata/`, `/metadata/` — schema mutations  
4. **Apps as code** — TypeScript packages (`defineObject`, `defineView`, logic functions, front components, agents) synced via CLI (`yarn twenty dev` / `apply` / `publish`)

This is closer to **Salesforce metadata + Lightning + Apex**, but open-source TypeScript-native.

### 2.4 Implications for Bloom engineering

| Pattern in Twenty | Bloom takeaway |
|-------------------|----------------|
| Metadata-driven objects + generated GraphQL | Prefer “object registry + views” over hardcoding every entity screen |
| Separate API process + queue worker | Workflows/notifications must be async; don’t block request path |
| Schema-per-workspace customization | Multi-tenant customization needs careful migration story |
| Design system package (`twenty-ui`) | Invest in shared UI kit early (tables, filters, record shell) |
| Apps SDK | Domain packs (e.g. “flower ops”) could be versioned modules |

---

## 3. Domain Model

### 3.1 Standard objects

| Object | Role | Notes |
|--------|------|-------|
| **People** | Contacts / individuals | Email/calendar sync eligible |
| **Companies** | Accounts / orgs | Email/calendar sync eligible |
| **Opportunities** | Deals / pipeline | Stage via Select; kanban native |
| **Tasks** | To-dos linked to records | Activity surface |
| **Notes** | Notes on records | Activity surface |
| **Workflows** | Automation definitions | First-class product object in nav |
| **Dashboards** | Analytics boards | KPI widgets |

**Important product constraint (docs):** email and calendar sync only work with **People, Companies, Opportunities**. Custom objects do not get mailbox/calendar attachment the same way. Design guidance: prefer fields/views on People rather than inventing alternate contact objects if you need sync.

### 3.2 Customization primitives

| Primitive | Behavior |
|-----------|----------|
| **Custom objects** | Unlimited; appear in sidebar; deactivate (soft) or delete |
| **Fields** | Text, number, date/datetime, currency, select, multi-select, relation, and more (SDK `FieldType.*`) |
| **Relations** | Bidirectional; one-to-many / many-to-one via relation fields |
| **Views** | Saved filters, sort, field visibility, grouping; shared or private |
| **Record page layouts** | Tabs + grid widgets (fields, related lists, emails, timeline, tasks, notes, files, charts, iframe) |
| **Roles** | Object / field / settings / action permissions; API keys & AI agents assignable to roles |
| **Row-level permissions** | Premium (Organization plan): filter conditions per role per object |

### 3.3 Sales pipeline model (not orders)

- **Opportunity** ≈ deal  
- **Stage** ≈ values of a **Select** field (not a separate Status entity)  
- Kanban columns = select options; drag-and-drop updates stage  
- Aggregations on columns: count, sum, avg, min, max (e.g. pipeline value per stage)

There is **no native Order, OrderLine, Shipment, Payment, Shop, Inventory** object. Those must be modeled as custom objects + workflows.

### 3.4 Bloom mapping table

| Twenty concept | Bloom concept | Fit |
|----------------|---------------|-----|
| Workspace | Network / tenant (or single Bloom deployment) | Good for isolation; not for shop-inside-network |
| Company | Shop partner / B2B account / marketplace merchant | Partial |
| Person | Customer, florist contact, courier contact | Partial (no channel identity model) |
| Opportunity | **Not** flower order — sales deal only | Poor as-is; remap as custom **Order** |
| Opportunity.stage (Select) | Single pipeline status | Partial — Bloom needs **dual** statuses |
| Task / Note | Internal ops notes / follow-ups | Useful |
| Custom object | Order, Shop, Courier, Bouquet SKU, Complaint… | **Primary path** for Bloom domain |
| Relation fields | Order→Shop, Order→Customer, Order→Courier | Steal |
| Workflow | Status transitions, SLA pings, webhook to Flowwow | Steal pattern |
| Dashboard | Ops KPIs (orders/day, late, conversion) | Steal pattern |
| Email sync | B2B sales email; not WA/TG | Avoid expecting inbox parity |
| Apps (code) | Versioned “Bloom ops pack” | Conceptual steal |

### 3.5 Recommended Bloom custom model *if* cloning Twenty style

```
Shop (custom)
  ├── fields: name, city, timezone, active, channelFlags…
  └── relations: Orders, Staff (People), …

Order (custom)  ← primary ops entity (not Opportunity)
  ├── fulfillmentStatus: SELECT  (new → confirmed → assembling → delivery → done / cancel)
  ├── paymentStatus: SELECT     (unpaid → paid → refund…)
  ├── channel: SELECT           (marketplace | direct | phone…)
  ├── amount: CURRENCY
  ├── deliveryAt: DATE_TIME
  └── relations: Shop, Customer(Person), Courier(Person?), items…

OrderItem (custom) if multi-line needed
Thread / Message — prefer dedicated inbox product (Chatwoot-class), not Twenty Notes
```

**Dual status:** model as **two Select fields** on Order (not one stage), with **two kanban/table views** (or one table grouped by fulfillment + filter chips for payment). Twenty does not enforce cross-field status machines natively — workflows must keep them consistent.

---

## 4. UI / Information Architecture

### 4.1 Shell & navigation

Observed / documented IA:

```
Left sidebar (customizable)
├── Favorites (pinned views / records / searches)
├── Workspace objects
│   ├── Companies
│   ├── People
│   ├── Opportunities
│   ├── Tasks
│   ├── Notes
│   ├── Dashboards
│   └── Workflows (+ custom objects)
├── Folders / reorder / hide unused objects
├── External links
└── Settings
```

Capabilities:

- Drag-reorder nav items  
- Folders for grouping objects/views  
- Hide unused standard objects  
- Pin favorites  
- Command palette **Cmd/Ctrl+K** (navigate, create, bulk actions, theme)

### 4.2 View types (list surfaces)

| View | Use |
|------|-----|
| **Table** | Default; spreadsheet columns; inline-friendly; group-by Select |
| **Kanban** | Pipeline by Select stages; compact mode; column aggregations |
| **Calendar** | Records plotted by date field |

Views store: filters, sort, field visibility, grouping; **workspace-shared or private**.

### 4.3 Record detail pages

Configurable via layout mode (`Cmd+K` → edit layout):

- Tabs  
- Widgets on a **grid**: fields, related records, emails, timeline, calendar, tasks, notes, files, charts, iframes  
- Drag/resize widgets; per-widget field visibility  

This is the strongest UX pattern for Bloom **order detail**: one shell, many widgets (status chips, customer, shop, chat iframe, timeline).

### 4.4 Interaction polish (UX bar)

Patterns Bloom should treat as the **modern CRM floor**:

1. Dense but airy **table** with logos/avatars, filters, sort, “Calculate”/aggregations  
2. **Kanban** with stage colors and money aggregates  
3. **Command menu** for power users  
4. **Inline** create and bulk actions (export, delete, send email)  
5. Soft delete vs destroy  
6. Record timeline + related activity without leaving the page  
7. Dark mode / experience settings  
8. i18n (Lingui + Crowdin community)  

Marketing claim: “feels like Notion” — fair for navigation and table density; less so for true collaborative docs.

### 4.5 Communication UI (limited)

- **Email & calendar** centralized for connected Google/Microsoft accounts  
- Threading and meetings surface on People/Companies/Opportunities  
- **No** multi-channel agent inbox UI (WA/TG assignment, SLA queues, CSAT)

For Bloom, treat Twenty’s communication surface as **sales activity**, not **ops messenger**.

### 4.6 Settings IA (admin)

- General (workspace name/logo)  
- Experience (timezone, date format)  
- Members + Roles  
- Accounts (email/calendar connect)  
- Data Model  
- API & Webhooks  
- Applications (installed apps)  
- Billing (cloud)  
- Security / SSO (plan-dependent)

---

## 5. Workflows

### 5.1 Product model

Workflows are a first-class nav object: create → trigger → actions → test → activate.

**Triggers:**

| Trigger | Meaning |
|---------|---------|
| Record events | Create / update / delete on any object |
| Schedule | Cron-like (daily, weekly, …) |
| Manual | User-initiated (often needs workflow management permission) |
| Webhook | Inbound HTTP trigger |

**Actions (documented):**

- Create / Update / Delete / Search / Upsert records  
- Iterator, Filter, Delay  
- Send Email (connected account)  
- Code (custom JavaScript)  
- HTTP Request (external APIs)  
- Form (runtime user input inside Twenty UI)  
- AI Agent (intelligent steps; expanding)

### 5.2 Engineering characteristics

- Execution is asynchronous (BullMQ workers)  
- Steps can reference prior step outputs  
- Test mode with sample data before activation  
- Best practice: rename steps; start simple; plan logic before building  

### 5.3 Bloom-oriented workflow examples (on custom Order)

| Automation | Trigger | Actions |
|------------|---------|---------|
| Marketplace intake | Webhook from Flowwow | Upsert Order + Person; set channel=marketplace |
| Payment confirmed | Order.paymentStatus → paid | Notify shop; allow assembly |
| Stuck assembling > 2h | Schedule + Search | Filter stale; update flag; HTTP to alert channel |
| Delivery done | fulfillmentStatus → done | Create Task “request review”; HTTP NPS |
| Cancel + refund path | Manual form | Update both statuses; HTTP refund service |

### 5.4 Gaps vs Bloom dual-status ops

- No built-in **state machine** with legal transitions matrix  
- No parallel-lane visualizer (fulfillment × payment)  
- No courier geo / dispatch actions  
- Code/HTTP steps exist, but ops reliability (idempotency, retries UX) is product-dependent — validate in self-host before relying  

---

## 6. Multi-Workspace / Multi-Tenant

### 6.1 Workspace as tenant boundary

Twenty’s primary isolation unit is the **Workspace**:

- Own data model (objects/fields can diverge)  
- Own members, roles, settings, apps installs  
- Own generated API surface (schema-per-tenant APIs)  
- Users can belong to **multiple workspaces** and switch after login  

Apps can be **registered once at server level** and **installed into multiple workspaces** (docs: application registration vs installed app).

### 6.2 What “multi-shop” is *not* by default

| Desired Bloom model | Twenty default |
|---------------------|----------------|
| One network, many shops, shared customers, cross-shop analytics | Single workspace with custom **Shop** object + relations |
| Hard isolation per franchise legal entity | Multiple workspaces (heavy: split customers, no easy join) |
| Shop staff only see own shop’s orders | Row-level permissions (Organization/premium) or careful role filters |

**Practical recommendation for Bloom:**

1. **One workspace per network/product** (not one workspace per shop)  
2. Model **Shop** as custom object + `Order.shop` relation  
3. Use **views** (“My shop’s orders”) + roles; upgrade to **row-level** when needed  
4. Reserve multi-workspace for true multi-tenant SaaS (different flower brands / white-label clients on one Bloom cloud)

### 6.3 Permissions depth (relevant to multi-shop)

- Default object CRUD (see / edit / delete / destroy)  
- Object-level exceptions  
- Field-level (see / edit / no access)  
- Settings and action permissions (import/export CSV, send email, API, data model)  
- Roles on **members, API keys, AI agents**  
- Row-level filters (premium) for “own records / own region / assigned only”

### 6.4 Self-host multi-tenant note

Self-host via Docker Compose is supported officially. One deployment can host many workspaces (SaaS mode). Schema customization per workspace increases ops cost (migrations, metadata versioning). Apps CLI (`plan`/`apply`) is the intended way to keep schemas consistent across workspaces.

---

## 7. Analytics

- **Dashboards** object: real-time-ish performance tracking (product docs section)  
- Kanban/table **aggregations** for pipeline-style metrics  
- ClickHouse present in server stack → event/analytics pipeline for scale  
- AI chat can answer metric-style questions over workspace data  

**Bloom gap:** no native “orders by shop / late delivery rate / channel mix” until custom objects + dashboards are built. Do not expect ERPNext-grade ops analytics out of the box.

---

## 8. Extensibility / API / Self-host

| Capability | Detail |
|------------|--------|
| REST + GraphQL | Dynamic from workspace schema; playground in Settings → API & Webhooks |
| Auth | Bearer API keys; OAuth for apps; keys scoped via Roles |
| Batch | Up to 60 records per call; GraphQL batch upsert |
| Rate limit (cloud docs) | 100 req/min |
| Webhooks | Outbound + workflow webhook triggers |
| Zapier | Official package |
| Apps framework | Objects, views, layouts, logic functions (HTTP/cron/DB events), front components, AI skills/agents |
| MCP | Cloud workspaces expose MCP for AI assistants |
| Self-host | Docker Compose; AGPL-3.0 obligations apply |
| Cloud pricing (site) | Pro ~$9/user/mo; Org ~$19/user/mo (SSO, row-level) — verify current pricing |

**License risk for Bloom product:** AGPL-3.0 is strong copyleft. Using Twenty as a **hosted dependency of a commercial SaaS** may force source disclosure of modifications/network use depending on architecture and legal interpretation. Prefer **pattern theft** over **fork-as-product** unless legal green-lights AGPL.

---

## 9. STEAL for Bloom UX (брать)

### UX / IA

1. **Sidebar = object list + folders + favorites** — ops users pin “Today’s deliveries”, “Marketplace queue”.  
2. **Three view types on every core entity:** Table / Kanban / Calendar (delivery calendar for Order.deliveryAt).  
3. **Saved views** private vs shared — shop managers vs network admins.  
4. **Record page as widget grid** — status widgets, customer, shop, timeline, embed chat.  
5. **Cmd+K command palette** — jump to order, change status, assign courier.  
6. **Column aggregations** on boards — “sum of order amount in Delivery”.  
7. **Group-by Select** in tables — group orders by shop or channel.  
8. **Soft delete + destroy** distinction for ops safety.  
9. **Notion-like density** without ERPNext form heaviness — Bloom should feel this modern.

### Domain / platform

10. **Custom objects as equal citizens** to standard ones (sidebar, API, views, workflows).  
11. **Stage = Select field**, kanban = projection of that field (simple mental model).  
12. **Dual status via two Selects** + dedicated views (fulfillment vs payment).  
13. **Workflows: record event + webhook + HTTP** for marketplace intake and status side-effects.  
14. **Metadata API + generated GraphQL** pattern for Bloom if multi-tenant SaaS later.  
15. **Roles on API keys and automation actors** — least privilege for integrations.  
16. **Apps-as-code** idea: versioned domain pack (`bloom-ops`) with objects/views — even if stack differs.  
17. **AI chat with page context** (“summarize this order”) — high leverage for shop staff later.

### Multi-entity

18. **Workspace = tenant**, **Shop = data object** (don’t explode tenants per shop).  
19. **Row-level permission trajectory** as network grows (even if MVP is view-based).

---

## 10. AVOID (не брать / осторожно)

1. **Using Opportunity as Order** — wrong lifecycle, wrong sales semantics, email-sync bias.  
2. **One workspace per flower shop** — fragments customers, analytics, support; ops nightmare.  
3. **Expecting WA/TG/MAX inbox** — Twenty is email/calendar CRM; use Chatwoot-class for messenger.  
4. **Single stage field for Bloom** — flower ops need at least fulfillment × payment (and often channel).  
5. **Over-customizing People into shop/courier types without views** — docs warn against object explosion; use fields + views, but don’t force courier geo into Person.  
6. **Assuming free row-level security** — shop isolation may be paid/premium or custom-built.  
7. **Forking AGPL into closed SaaS without counsel** — legal and upgrade cost.  
8. **Porting Twenty’s full monorepo stack “because stars”** — Nest+Nx monorepo is heavy; steal UX, not necessarily the entire engine.  
9. **Believing custom objects get full email/calendar parity** — product limitation on core three objects.  
10. **Kanban-only ops** — high-volume flower orders need dense tables + filters first; kanban is secondary for stage queues.  
11. **Workflow-only enforcement of status legality** — users can still set illegal combinations unless UI/API validate transitions.  
12. **Ignoring offline / peak delivery UX** — Twenty is cloud-office UX, not courier/mobile-first.

---

## 11. Web MVP notes (structure prototype)

**Purpose of `mvp/twenty/index.html` (Analyzer companion):** offline clickable **Twenty IA shell**, not Bloom skin.

### Screens to prototype

| Screen | Elements |
|--------|----------|
| App shell | Left nav: Companies, People, Opportunities, Tasks, Notes, Dashboards, Workflows, Settings; favorites; Cmd+K hint |
| Companies table | Columns: name, domain, owner, industry, ARR; filters; count |
| Opportunities kanban | Stages: New → Screening → Meeting → Proposal → Customer; card amount + company |
| Opportunity record | Tabs: Fields, Timeline, Tasks, Notes, Emails; related company/person |
| People table | Name, email, company, job title |
| Workflows list | Name, active toggle, trigger type |
| Dashboard placeholder | KPI cards (pipeline value, open opps) |
| Settings | Members, Roles, Data Model stub, API keys stub |

### Interaction budget (MVP)

- Client-side tab/panel switch only  
- Sample static JSON for 5–8 fake companies/opportunities  
- Kanban columns as CSS columns (drag optional)  
- Label header: `Twenty · structure MVP · id: twenty`  

### Bloom delta callouts (optional footnotes in MVP)

- “Order would be custom object”  
- “No messenger inbox module”  
- “Dual status not native”

---

## 12. Fit score (1–10)

Scored for **Bloom flower multi-shop ops CRM** (not “best open-source CRM in general”).

| Dimension | Score | Comment |
|-----------|------:|---------|
| Modern UX / IA benchmark | 9.5 | Best-in-class among OSS CRM shortlist for UI polish |
| Custom objects & extensibility | 9.0 | Metadata + Apps SDK + dynamic API |
| Workflows / automation | 8.0 | Solid triggers/actions; not full process engine |
| Multi-workspace / tenancy | 7.5 | Strong workspace isolation; shop-in-network needs modeling |
| Orders / ops domain | 3.0 | No native fulfillment/inventory/POS |
| Multi-shop ops | 4.0 | Possible via custom model + RLS; not productized |
| Messenger / inbox | 2.5 | Email/calendar only |
| Analytics for ops | 5.0 | Dashboards exist; ops metrics DIY |
| Self-host & stack quality | 8.0 | Modern TS stack; non-trivial ops |
| License / productization risk | 4.0 | AGPL + SaaS implications |
| **Weighted Bloom fit** | **6.0 / 10** | **Excellent UX/platform reference; weak as ops CRM base** |

### Scoring narrative

- **As benchmark to steal from:** 9/10 — primary shortlist pick for UI, views, record layouts, command palette, custom objects story.  
- **As fork/foundation for Bloom:** 4/10 — wrong domain core, AGPL, missing inbox and shop ops.  
- **Blended “how much should Bloom study Twenty?”:** **6/10** overall fit (rank #4 in shortlist by ops depth, #1 by UX richness).

### Recommendation (RU)

**Twenty — эталон современного CRM UX, а не готовая операционная система цветочной сети.**

Брать: табличные/канбан-виды, избранные вьюхи, карточку записи как сетку виджетов, Cmd+K, кастомные объекты наравне со стандартными, вебхуки/workflow для intake с маркетплейса, workspace как tenant.

Не брать: Opportunity как заказ; workspace-на-каждый-магазин; надежду на WA/TG inbox; AGPL-форк без юридической оценки; один Select-статус вместо dual status.

**Практика для Bloom:** рядом с ERPNext/Dolibarr (ops) и Chatwoot (inbox) держать Twenty как **UI/IA/custom-object benchmark** при проектировании web MVP и design system.

---

## 13. Mapping checklist (CRM → Bloom) — quick ref

| Twenty | Bloom |
|--------|-------|
| Workspace | Tenant / network instance |
| Company | Shop org / partner account |
| Person | Customer / staff contact |
| Opportunity | ❌ → custom **Order** |
| Stage (Select) | One of **fulfillmentStatus** or pipeline only |
| Second Select | **paymentStatus** / **channel** |
| Task | Internal ops task |
| Note | Internal comment (not chat) |
| Workflow | Automations & integrations |
| Dashboard | Ops analytics |
| Role + row-level | Shop staff scoping |
| App package | Versioned Bloom domain module |
| Email timeline | Sales activity only |
| GraphQL Core API | Backend for record CRUD |
| Metadata API | Admin schema tooling |

---

## 14. Sources

1. https://github.com/twentyhq/twenty — README, license AGPL-3.0, monorepo packages  
2. https://docs.twenty.com/user-guide/introduction — product modules  
3. https://docs.twenty.com/user-guide/data-model/overview — objects, fields, design rules  
4. https://docs.twenty.com/user-guide/workflows/overview — triggers & actions  
5. https://docs.twenty.com/user-guide/layout/overview — nav, views, record pages  
6. https://docs.twenty.com/user-guide/views-pipelines/capabilities/kanban-views — stages, aggregations  
7. https://docs.twenty.com/user-guide/views-pipelines/capabilities/table-views — group-by, tables  
8. https://docs.twenty.com/user-guide/permissions-access/capabilities/permissions — RBAC, field, row-level  
9. https://docs.twenty.com/user-guide/ai/overview — AI chat & agents  
10. https://docs.twenty.com/developers/extend/api — schema-per-tenant REST/GraphQL  
11. https://docs.twenty.com/developers/extend/apps/getting-started/quick-start — Apps CLI & entities  
12. https://twenty.com — positioning, pricing signals, product screens  
13. https://twenty.com/resources/why-twenty — product philosophy  
14. Shortlist context: `docs/research/crm-benchmark/00-candidates.md`

---

*End of report — id: `twenty`*
