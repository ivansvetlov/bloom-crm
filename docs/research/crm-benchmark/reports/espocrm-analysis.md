# EspoCRM — Bloom CRM Benchmark Analysis

| Field | Value |
|-------|--------|
| **id** | `espocrm` |
| **Product** | EspoCRM |
| **License** | GNU AGPLv3 (core) |
| **Stack** | PHP REST API backend + custom SPA frontend (JS/TS) · MySQL 8+ / MariaDB 10.3+ / PostgreSQL 15+ · PHP 8.3–8.5 |
| **Type** | Web (SPA) |
| **Repo** | https://github.com/espocrm/espocrm |
| **Docs** | https://docs.espocrm.com |
| **Demo** | https://www.espocrm.com/demo/ |
| **Stars (approx., 2026-08)** | ~3.2k |
| **Commits (approx.)** | ~23k |
| **Review date** | 2026-08-01 |
| **Bloom fit score** | **6.5 / 10** (strong entity/status blueprint; weak native ops/orders/inbox) |

**Sources used:** official README, Entity Manager, Layout Manager, Pipelines, Workflows, BPM, Case management, Sales management, Roles docs; product site; GitHub `espocrm/espocrm`.

---

## 1. Overview / Positioning

EspoCRM is a **mature, self-hostable CRM platform** positioned less as a fixed sales product and more as a **metadata-driven application framework** for customer-facing business processes. The core ships classic CRM objects (Accounts, Contacts, Leads, Opportunities, Cases, Activities, Campaigns, Emails) plus deep admin tooling: Entity Manager, Layout Manager, Formula, Roles/Teams, Portals, Kanban, and (as of v10) multi-pipeline stages.

**Who it serves**

- SMBs and mid-market teams that want on-prem CRM without Salesforce complexity.
- Developers/integrators building **custom business apps** on CRM primitives.
- Support/ops teams using **Cases + Stream + email-to-case**.

**What it is *not***

- Not a retail/ops ERP: no first-class multi-shop inventory, marketplace order intake, courier routing, or shop-level P&L in free core.
- Not an omnichannel messenger (WhatsApp/Telegram/MAX): email is first-class; social/messengers need integration.
- Full Workflows / BPM / rich Reports live in **commercial Advanced Pack** (not pure OSS for automation depth).

**Bloom relevance in one line**

Best open-source reference for **entity modeling, status-driven Kanban, Cases-as-tickets, team ACL, and formula/workflow automation patterns** — not for marketplace order ops out of the box.

---

## 2. Architecture

### 2.1 High-level

```
┌─────────────────────────────────────────────────────────┐
│  SPA Client (custom framework, nested views, partial TS) │
│  List / Detail / Edit / Kanban / Dashlets / Admin tools  │
└───────────────────────────┬─────────────────────────────┘
                            │ REST JSON API
┌───────────────────────────▼─────────────────────────────┐
│  PHP Application (Espo DI container, services, hooks)    │
│  Metadata (entityDefs, clientDefs, ACL, layouts…)        │
│  Built-in ORM + Select Builder + Jobs / Daemon / WS      │
└───────────────────────────┬─────────────────────────────┘
                            │
              MySQL / MariaDB / PostgreSQL
```

- **Backend:** PHP, SOLID-oriented, static typing, PHPStan level 8; own ORM (not Doctrine/Eloquent); metadata-centric config described with JSON Schema (IDE autocomplete).
- **Frontend:** SPA on a **custom** view framework (not React/Vue/Angular). Nested views + service DI; core partially TypeScript. Field/form views are the main extension surface.
- **API:** Straightforward REST for CRUD, search, relationships — primary integration surface for external systems (marketplace webhooks, couriers, messengers).
- **Customization storage:** Admin customizations land in `custom/Espo/Custom` (copyable between instances; rebuild via `php rebuild.php`; exportable as extension packages).
- **Runtime extras:** Cron/jobs, optional daemon, WebSocket for live updates, Formula engine (before-save scripts, calculated fields).
- **Extensions model:** Core AGPL; Advanced Pack (Workflows, BPM, Reports), Sales Pack (products, inventory, quotes/orders-like commercial modules), VoIP, Google/Outlook, Stripe, etc. are **paid extensions**.

### 2.2 Design principles useful for Bloom

| Principle | Espo pattern | Bloom takeaway |
|-----------|--------------|----------------|
| Metadata over hardcode | Entity/field/layout/ACL as data | Order/Shop/Status definitions should be data-driven |
| Entity types as first-class modules | Each type: list/detail/kanban/search/mass-update | One “Order” entity + related panels beats scattered tables |
| Side panel + bottom panels | Assigned user, teams, stream, relationships | Ops detail: status chips + courier + shop + timeline |
| Team-scoped ACL | Roles merge permissively; record `Teams` field | Map shops/branches → teams (with caveats) |
| Formula + hooks | No-code calc + PHP hooks for hard logic | Dual-status rules, SLA timers, channel defaults |
| REST as product boundary | SPA is just one client | Mobile / marketplace workers / bots share API |

### 2.3 Self-host & ops notes

- Install: manual, script, Docker, Traefik/Caddy docs.
- Requirements: modern PHP + SQL RDBMS only (no heavy Redis dependency for basic CRM).
- AGPL: network use implies source obligations for modified deployments — relevant if Bloom SaaS forks Espo rather than learning from it.

---

## 3. Domain Model

### 3.1 Core stock entities

| Entity | Role | Bloom analogy |
|--------|------|----------------|
| **Account** | Company / org hub | Corporate client / B2B buyer; *not* shop |
| **Contact** | Person linked to Account(s) | Recipient / buyer person |
| **Lead** | Pre-customer; convertible | Inbound interest / unconverted marketplace lead |
| **Opportunity** | Deal pipeline + amount + stage + probability | Sales pipeline only — **not** operational flower order |
| **Case** | Support ticket / issue; stream; email-to-case | Closest stock object to **ops ticket / exception order** |
| **Email** | Threaded mail, group accounts | Channel thread (email only) |
| **Meeting / Call / Task** | Activities / calendar | Ops tasks, callbacks |
| **Campaign / Target List** | Marketing | Weak for Bloom day-1 |
| **Document / Knowledge Base** | Files, KB articles on cases | Shop SOPs / product notes |
| **User / Team / Role / Portal** | Access model | Staff, shop teams, customer portal |
| **User Task** (BPM) | Human step in process | Florist / courier manual checkpoints |

**Commercial (Sales Pack, not free core):** Products, Quotes, Sales Orders, Invoices, Inventory — closer to commerce but still not multi-shop flower marketplace ops.

### 3.2 Entity Manager — the real product

Entity Manager (Administration) lets admins:

- Create **custom entity types** with templates:
  - **Base** — Name, Assigned User, Teams, Description
  - **Base Plus** — + Activities, History, Tasks panels
  - **Person** / **Company** — contact-like field sets
  - **Event** — calendar-capable
- Configure **fields** (enum, multi-enum, link, link-multiple, currency, datetime, formula-driven, etc.)
- Configure **relationships**: 1:N, N:1, N:N, 1:1, children-to-parent (polymorphic parent)
- Set **Status Field** (enum) → enables **Kanban**
- Optional: Stream, Stars, Collaborators, Multiple Assigned Users, Categories, Lockable, Transactional Save, **Pipelines** (v10+)
- **Formula** before-save + API before-save scripts
- Custom names get `c` prefix by default (conflict avoidance)

**Implication for Bloom:** model `Order`, `Shop`, `CourierAssignment`, `MarketplaceListing`, `ChatThread` as custom entities rather than abusing Opportunity.

### 3.3 Status & pipeline model

**Default pattern (single dimension):**

1. One **enum Status field** per entity type.
2. That field is designated as **Status Field** on the entity.
3. **Kanban** columns = enum options (orderable / styled).
4. Drag-and-drop updates status.

**Opportunities (stock):** stages Prospecting → Qualification → Proposal → Negotiation → Closed Won / Closed Lost, each with **probability** for forecast dashlets.

**Pipelines (v10+):** multiple pipelines per entity type (Leads, Opportunities, custom Base/Base Plus/Person/Company). Each record has `Pipeline` + `Pipeline Stage`; Status becomes read-only mirror of stage. Kanban shows **one pipeline at a time** (dropdown switch). Pipelines can be restricted to **teams**.

**Critical for Bloom dual status:**

- Espo’s first-class UX optimizes **one status dimension** (or pipeline-scoped stages of that same enum family).
- **Parallel statuses** (e.g. fulfillment vs payment, shop vs network) require **two+ enum fields** + custom UI (list badges, detail chips) + Formula/Workflow guards — not native dual-kanban.
- Pipelines solve “different process variants per channel/shop,” **not** “two independent life-cycles on one order.”

### 3.4 Cases as ops skeleton

Cases are the strongest **ops-adjacent** stock entity:

- Create paths: manual, portal, API, **email-to-case**, workflow.
- Linked to Account and/or Contacts (and optionally Lead).
- **Stream** for internal + customer dialogue (internal posts lockable from portal).
- Knowledge base links, collaborators (v9+), group email parent for reply routing.
- Assignment via Round-Robin / Least-Busy (Workflows / Advanced Pack).
- Explicit note in docs: Cases need not be limited to support — reusable as generic tracked work items.

**Bloom mapping idea:** reserve Case for **exceptions/claims/complaints**; use custom **Order** entity for primary fulfillment lifecycle.

### 3.5 Multi-shop / multi-tenant patterns

| Mechanism | What it does | Fit for multi-shop |
|-----------|--------------|--------------------|
| **Teams** on records + role level `team` | Isolate read/edit by team membership | Good proxy for **shop-scoped staff** |
| **Roles** merge (most permissive wins) | Flexible ACL stacking | Shop manager vs network operator |
| **Baseline role** (v9.2+) | Default floor for all users | Network-wide minimum rights |
| **Field-level security** | Hide sensitive fields | Hide network margin from shop |
| **Layout Sets** per team/portal/user | Different UI per team | Shop vs HQ layouts |
| **Pipelines per team** | Different stages visibility | Channel-specific order flows |
| **Portals** | External customer users | End-customer order tracking (limited) |
| **Collaborators** | Cross-team read/stream share | Shared order without full team ACL |

**Gaps:** No true multi-company / multi-database tenancy in core. No first-class **Shop** entity, inventory by warehouse-per-shop, or marketplace vs direct order channel objects. Teams are a **security and layout boundary**, not a full org hierarchy (parent teams exist in config for some inheritance cases but are not a retail org model).

### 3.6 Communication / inbox

- **Emails:** personal + group accounts; email-to-case; parent link to Case/Opportunity/etc.; Stream integration.
- **Stream:** activity + comments + audit-ish notes; follow/auto-follow.
- **Portal:** customer-facing case create/view.
- **SMS:** admin-configurable sending (not full SMS inbox product).
- **No native** WhatsApp / Telegram / MAX / Instagram DM unified inbox (contrast Chatwoot).

For Bloom messenger ops, Espo is a **CRM record hub** you integrate *into*, not the inbox itself.

### 3.7 Analytics

- **Core:** dashlets (Sales by Month, Opportunities by Stage, Sales Pipeline, etc.), list filters, export.
- **Advanced Pack Reports:** grid reports, charts on dashboard, scheduled workflow-from-report — **commercial**.
- No built-in multi-shop ops KPI suite (SLA, on-time delivery %, cancellation by shop, marketplace share).

---

## 4. UI / Information Architecture

### 4.1 Shell

Typical admin/user shell:

- **Top / side navigation** — entity modules (customizable tabs), global search, notifications, quick create.
- **Dashboard** — personal/home dashlets (charts, list widgets).
- **List view** — columns from Layout Manager; filters; mass actions; switch to Kanban when enabled.
- **Detail view** — main panels (fields in 1–4 columns, optional **tabs**), **side panel** (Assigned User, Teams, status-ish fields), **bottom panels** (Stream, relationships, activities).
- **Quick create / quick view** — small layouts for speed.
- **Admin** — Entity Manager, Layout Manager, Roles, Teams, Workflows/BPM (if licensed), Email accounts, Portals, Pipelines, Currency, Jobs.

UX character: **minimalist, dense, form-centric**, short learning curve for CRM users; not a modern React “notion-like” UI (Twenty is closer to that aesthetic).

### 4.2 Layout Manager (IA control plane)

Layouts per entity:

- List, Detail, List Small, Detail Small  
- Bottom Panels, Side Panels, Side Panel Fields  
- Search Filters, Mass Update  
- **Kanban** layout  
- Extra (Convert Lead, etc.)  
- Custom list layouts (v8+) for relationship panels  

**Dynamic logic:** show/hide panels (and fields via dynamic handler patterns) by conditions — important for status-dependent ops forms (e.g. show courier block only after `ready_for_delivery`).

**Layout Sets:** different layouts for teams / portals / users — HQ sees network fields; shop sees local fulfillment fields.

### 4.3 Kanban IA

- Enabled only if Status Field set.
- Columns = status options (or pipeline stages when Pipelines on).
- Card fields configurable; column min width / order limits via config.
- One primary status axis per board; multi-pipeline = switcher, not dual boards on one screen.

### 4.4 Suggested Espo-like module map (stock + custom for Bloom)

```
CRM
  Accounts · Contacts · Leads · Opportunities
Service
  Cases · Knowledge Base
Activities
  Calendar · Tasks · Meetings · Calls
Communication
  Emails
Marketing
  Campaigns · Target Lists
[Custom Bloom]
  Orders · Shops · Couriers · Channels · Claims
Analytics
  Dashboard · Reports*
Admin
  Users · Teams · Roles · Entity Manager · Layouts · Workflows* · BPM*
```

\* Advanced Pack / commercial.

---

## 5. Workflows / BPM

> **License note:** Workflows and BPM are part of **Advanced Pack** (paid). Patterns below are still high-value design references even if Bloom builds its own engine.

### 5.1 Workflows (rule engine)

**Structure of a rule**

1. Target entity type  
2. Trigger type  
3. Conditions (UI builder or Formula)  
4. Actions  

**Triggers**

| Trigger | Use |
|---------|-----|
| After record created | New order → assign shop team |
| After record updated | Status changed → notify / side effects |
| Created or updated | Common; pair with “field changed” |
| Manual | Detail-view button / menu (teams, dynamic-logic visibility, access level) |
| Scheduled | Cron + List Report result set |
| Sequential | Chained from another workflow (delays, branching) |
| Signal | System/object signals (shared with BPM) |

**Conditions**

- UI: equals / was equal / empty / **changed** / not changed / …  
- Formula: e.g. `status == 'New' && assignedUserId == null`

**Actions (selected)**

- Send Email, Create/Update record, Link/Unlink  
- Apply Assignment Rule (Round-Robin, Least-Busy)  
- Create Notification, Make Followed  
- Trigger another Workflow, Start BPM Process  
- Send HTTP Request (integration glue)  
- Execute Formula Script, Run Service Action  

**Manual workflows** ≈ no-code “actions” on order detail (e.g. “Mark paid”, “Request florist photo”) with role gating — highly relevant UX for Bloom ops cabinet.

### 5.2 BPM (BPMN 2.0)

- Flowcharts per **target entity type**; Processes are instances bound to **one target record**.
- Start: automatic (condition/signal/schedule), manual, or from Workflow.
- Elements: **Events**, **Gateways** (exclusive/inclusive/parallel diverge-converge), **Activities** (service tasks, user tasks, sub-processes), Sequence flows.
- Visualization of node status (processed / pending / in process / failed).
- Manual intervene: stop process, reject nodes, start flow from node, reactivate.
- Only **one active process** per (target record, flowchart) at a time.
- Shares condition model and many task actions with Workflows; Workflow recommended for simple rules, BPM for multi-step human+system paths.

**Bloom process examples BPM-shaped**

1. Marketplace order intake → validate shop capacity → assign florist → ready → courier → delivered → review.  
2. Exception: delayed delivery → user task to shop → compensation (refund/remake) → close claim.  
3. Dual-channel: diverge by `channel ∈ {marketplace, direct}` early in flowchart.

### 5.3 Formula (core, free)

- Before-save scripts on entity types; recalculate mass action.
- Sets derived fields, enforces invariants, can create related records (careful with loops).
- Complements Workflows when Advanced Pack absent — still limited vs full BPM.

---

## 6. STEAL — Entity / Status Design for Bloom

Patterns Bloom should **copy** (ideas, not code fork):

### 6.1 Entity design

1. **Entity templates** — Base Plus-style package (name, assignee, teams, stream, activities) as default for ops objects.  
2. **Status Field as explicit entity parameter** — one designated enum drives Kanban; other enums stay secondary.  
3. **Relationship catalog** — 1:N, N:N, polymorphic parent (email/activity → parent Order/Case).  
4. **Side panel convention** — assignee + teams/shops + primary status always visible; main canvas for domain fields.  
5. **Bottom relationship panels** — line items, chat thread, courier runs, payments as panels not separate apps.  
6. **Collaborators** — cross-shop visibility without dumping record into every team.  
7. **Layout Sets by role/team** — shop UI ≠ network dispatcher UI.  
8. **Custom entity over abusing Opportunity** — Opportunity stage/probability is sales math; Order fulfillment is ops.  
9. **Metadata + rebuild** — exportable customizations, env promotion (`custom/` copy + rebuild).  
10. **REST-first** — every entity equally available to SPA, bots, marketplace workers.

### 6.2 Status design

1. **Kanban = visualization of one enum life-cycle** — perfect for fulfillment board.  
2. **Status options as ordered, colored stages** with probability *only if* forecasting needed (orders usually skip probability).  
3. **Pipelines-as-variants** — separate stage sets for marketplace vs direct vs corporate, switched by pipeline (or Bloom “flow template”), restricted by team/shop.  
4. **“Field changed” workflow conditions** — reliable hooks for status transitions (notify, SLA, side effects).  
5. **Manual action buttons** — controlled transitions (guarded status changes) instead of free-form enum edits for critical steps.  
6. **Internal vs external stream posts** — shop notes vs customer-visible updates.  
7. **Assignment rules** — Least-Busy / Round-Robin for dispatcher → shop or courier pools.  
8. **Audit / stream on relationship changes** — who linked courier, who reassigned shop.

### 6.3 Dual-status recommendation (Bloom-specific, inspired by Espo gaps)

Espo does **not** ship dual Kanban axes. For Bloom, steal the **clarity of a primary Status Field**, then extend:

| Dimension | Example values | UI |
|-----------|----------------|-----|
| **Fulfillment** (primary Kanban) | new → confirmed → assembling → ready → delivering → delivered / cancelled | Main board |
| **Payment** (secondary chip) | unpaid → authorized → paid → refunded | List column + detail badge |
| **Network control** (optional third) | shop_owned → network_watched → network_taken | Filter + badge |

Rules:

- Only **fulfillment** drives drag-and-drop board.  
- Payment/network change via actions + validations (Formula/Workflow analogues).  
- Never collapse payment into fulfillment enums (classic Espo footgun if you overload one Stage field).

### 6.4 Cases pattern to steal

- Email/channel → ticket creation  
- Stream as shared timeline  
- Portal for customer-visible slice  
- Separate **Claim/Case** entity from **Order** so support noise does not distort fulfillment KPIs  

### 6.5 ACL pattern to steal

- Record-level **Teams** (shops) + role levels `own | team | all`  
- Field-level security for network-only economics  
- Permissive merge of multiple roles for hybrid staff (florist who also dispatches)

---

## 7. AVOID

1. **Using Opportunity as Order** — stages/probability/forecast dashlets will fight ops semantics; reporting will lie.  
2. **Single enum overloaded with payment + delivery + claim states** — unmaintainable Kanban, impossible analytics.  
3. **Assuming Teams = multi-shop ERP** — no stock, no company chart of accounts, no marketplace settlement; only ACL/layout isolation.  
4. **Building Bloom inbox inside Espo email model** — email-to-case is fine; WA/TG/MAX need a Chatwoot-class component.  
5. **Depending on Advanced Pack for core product truth** — if Bloom is OSS/SaaS, do not design so that BPMN is required for basic status transitions; keep transition rules in open core.  
6. **AGPL fork as default product strategy** without legal/product review — learning Espo ≠ shipping a modified Espo under AGPL network copyleft casually.  
7. **Portal as full B2C order cabinet** — Case portal is service-oriented, not cart/checkout/delivery tracking product.  
8. **Custom SPA framework lock-in** — Espo’s frontend is proprietary-to-Espo patterns; for Bloom greenfield, prefer React/Vue ecosystem while **copying IA**, not the view engine.  
9. **Pipelines as dual-status** — pipelines are alternative stage sets, not parallel dimensions.  
10. **Ignoring child-record ACL** — Espo documents that email/meeting access ≠ case access; Bloom must define whether chat messages inherit order shop scope.  
11. **Workflow update loops** — status automation that re-triggers itself; Espo warns explicitly — design idempotent transitions.  
12. **Sales-pack inventory as flower multi-shop stock** — commercial modules still won’t match marketplace + dark-store + florist bench realities without heavy customization.

---

## 8. Web MVP Notes

### 8.1 Structure MVP (`mvp/espocrm/index.html`) — intent

Standalone HTML shell that **mirrors Espo IA**, not Bloom branding:

- Left/top nav: Home, Accounts, Contacts, Leads, Opportunities, **Cases**, Emails, Activities, (Custom) Orders demo tab optional as “how we’d extend”, Admin  
- Dashboard with dashlet placeholders  
- List ↔ Kanban toggle on Opportunities and Cases  
- Case detail: side panel (Assigned, Teams, Status), Stream, Emails panel  
- Admin stub: Entity Manager list, Layout concepts, Roles/Teams  
- Label header: **EspoCRM · id `espocrm`**

### 8.2 If prototyping *on* Espo (spike, not product)

1. Docker install from official docs.  
2. Entity Manager → create `Order` (Base Plus), enums `fulfillmentStatus`, `paymentStatus`.  
3. Set **Status Field** = `fulfillmentStatus`, enable Kanban.  
4. Link Order → Account/Contact, custom Shop (Company or Base), Teams = shops.  
5. Layout: side panel statuses; detail tabs Delivery / Payment / Customer.  
6. Formula: deny illegal transitions; default channel.  
7. Group email → Case for claims only.  
8. REST webhooks from marketplace → create Order.  
9. Accept that WA inbox and true multi-shop stock stay out of scope for the spike.

### 8.3 Bloom greenfield MVP (recommended path)

- Do **not** ship Espo as Bloom.  
- Steal: entity metadata mindset, status field + kanban, case/stream split, team ACL, manual actions, layout sets.  
- Implement dual-status and messenger as first-class Bloom modules.  
- Stack suggestion aligned with modern shortlist peers: TS API + React SPA + Postgres (Twenty-like DX) or PHP only if team is PHP-native — Espo proves PHP REST CRM is viable, not mandatory.

### 8.4 Acceptance checks for Espo structure MVP

- [ ] Offline open, no backend  
- [ ] Clickable nav across main modules  
- [ ] Kanban and list both represented  
- [ ] Case detail shows stream + assignment pattern  
- [ ] Notes call out Advanced Pack vs core  

---

## 9. Mapping: Espo concept → Bloom concept

| Espo concept | Bloom concept | Notes |
|--------------|---------------|-------|
| Account | B2B client / partner org | Not flower shop |
| Contact | Buyer / recipient person | Split buyer vs recipient fields on Order |
| Lead | Unqualified inbound | Optional |
| Opportunity | B2B deal only | Do not use as order |
| Case | Claim / support ticket / incident | Keep separate from Order |
| Email + Group Account | One channel adapter | Parallel adapters for WA/TG/MAX |
| Stream | Order timeline / internal notes | Internal vs customer-visible |
| Team | Shop or ops cell | Plus explicit Shop entity for attributes |
| Role + field-level ACL | Network vs shop permissions | Baseline role pattern useful |
| Status Field + Kanban | Fulfillment board | Primary axis only |
| Pipeline (v10) | Channel/flow template | Marketplace vs direct stage sets |
| Second enum + badges | Payment / network status | Custom dual-status |
| Workflow manual button | Ops action on order | “Confirm”, “Hand to courier” |
| BPM process | Long-running order/claim orchestration | Optional; keep simple transitions in core |
| Formula before-save | Domain invariants | SLA clocks, status guards |
| Portal | Customer tracking lite | Not full B2C app |
| Dashlets / Reports* | Ops KPI dashboard | Build Bloom metrics explicitly |
| REST API | Integration bus | Marketplace, payments, geo, chat |
| Entity Manager | Admin data model | Bloom needs controlled schema migrations, not only runtime EM |
| Layout Sets | Role-based UI | Dispatcher vs florist vs network |

---

## 10. Fit Score (1–10)

### 10.1 Scorecard

| Dimension (Bloom-weighted) | Score | Comment |
|----------------------------|------:|---------|
| Entity / metadata modeling | 9 | Best-in-class admin Entity Manager among shortlist CRMs |
| Status / Kanban / pipeline | 8 | Excellent single-axis; pipelines for variants; weak dual-axis |
| Cases / ops tickets | 8 | Stream, email-to-case, portal — strong ticket pattern |
| Workflows / BPM | 8* | *Powerful but commercial Advanced Pack |
| Multi-shop / org isolation | 5 | Teams/roles/layout sets only; no shop ops model |
| Orders / marketplace / direct | 3 | No native dual-channel order; Sales Pack still not marketplace |
| Messenger / omnichannel inbox | 3 | Email-first; no WA/TG/MAX product |
| Analytics / ops KPIs | 5 | Basic dashlets free; serious reports paid; not ops-native |
| UX cleanliness / IA | 7 | Fast, consistent, admin-powerful; dated vs Twenty |
| Self-host / API / extensibility | 8 | Docker, REST, hooks, metadata, extensions |
| License / commercial clarity | 6 | Core AGPL solid; critical automation/reports behind paid packs |
| **Overall Bloom fit** | **6.5** | **Design blueprint strong; product substitute weak** |

### 10.2 Verdict

**EspoCRM is a Tier-1 reference for Bloom’s entity + status + case + ACL design language**, and a Tier-3 candidate as an actual flower multi-shop ops system.

- **Use it to steal:** Entity Manager mental model, Status Field → Kanban contract, Case/Stream, Teams ACL, Layout Sets, manual workflow actions, pipeline-as-flow-variant.  
- **Do not use it to steal:** opportunity-as-revenue-core for fulfillment, email-as-only-inbox, teams-as-full-multi-shop ERP.  
- **Build Bloom as** a purpose-built ops cabinet with dual status and messenger-native IA; keep Espo on the research shelf next to Twenty (UX) and Chatwoot (inbox) and ERPNext (orders/multi-company).

### 10.3 Рекомендации (RU)

1. **Не форкать Espo как основу Bloom** без отдельного legal/product решения по AGPL и кастомному SPA-фреймворку.  
2. **Украсть контракт «Status Field → Kanban»** и явно назвать primary status = fulfillment.  
3. **Payment и network control** — отдельные поля/чипы + action API, не колонки того же канбана.  
4. **Order ≠ Opportunity ≠ Case**: три разных объекта с разными KPI.  
5. **Shop** — сущность с атрибутами (адрес, слоты, рейтинг), а Teams — только контур доступа.  
6. **Автоматизацию статусов** закладывать в open core (rules engine), не зависеть от платного BPM.  
7. **Inbox** интегрировать (Chatwoot-класс), а в CRM хранить link на thread + таймлайн.  
8. **Layout Sets / роли** — обязательный паттерн: флорист / диспетчер / сеть видят разные панели одного заказа.  
9. **MVP структуры** (`mvp/espocrm`) — показать Cases Kanban + Detail/Stream + Admin Entity concepts как референс IA.  
10. **Итоговый приоритет для синтеза:** Espo → status/entity chapter; ERPNext/Dolibarr → orders/multi-entity; Chatwoot → inbox; Twenty → modern UX shell.

---

## 11. Extensibility / API / Self-host (summary)

| Topic | Detail |
|-------|--------|
| API | REST CRUD, search, link; API keys / auth per docs |
| Hooks / Services | PHP hooks, custom API actions, scheduled jobs |
| Frontend extension | Custom views, buttons, dashlets, panels, CSS |
| Packaging | Extensions; Entity Manager export |
| Realtime | WebSocket optional |
| Hosting | Docker-friendly; PHP+SQL stack |
| Commercial gravity | Advanced Pack (Workflows, BPM, Reports), Sales Pack, VoIP, etc. |

---

## 12. Citations / links

- https://github.com/espocrm/espocrm  
- https://www.espocrm.com · https://www.espocrm.com/demo/  
- https://docs.espocrm.com  
- https://docs.espocrm.com/administration/entity-manager/  
- https://docs.espocrm.com/administration/layout-manager/  
- https://docs.espocrm.com/administration/workflows/  
- https://docs.espocrm.com/administration/bpm/  
- https://docs.espocrm.com/general/pipelines/  
- https://docs.espocrm.com/user-guide/case-management/  
- https://docs.espocrm.com/user-guide/sales-management/  
- https://docs.espocrm.com/administration/roles-management/  
- https://docs.espocrm.com/development/  

---

*Analyzer artifact for Bloom CRM benchmark · `{id}` = `espocrm` · path: `docs/research/crm-benchmark/reports/espocrm-analysis.md`*
