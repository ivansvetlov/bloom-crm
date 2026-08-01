# Bloom CRM — Mega Synthesis

| | |
|---|---|
| **Продукт** | Bloom CRM — операционный кабинет сети цветочных салонов |
| **Дата** | 2026-08-01 |
| **Источники** | 6 анализаторов shortlist + `00-candidates.md` + пакеты ТЗ (`tz-decomposition.md`) + `ARCHITECTURE_PLAN.md` |
| **Решение** | **Greenfield web**, не fork. Кража паттернов, не GPL/AGPL-кодовой базы |

**Брендинг:** в публичных текстах — **Bloom CRM**, канал = **маркетплейс** (не имя площадки).

---

## 1. Executive summary (RU)

Шесть open-source продуктов разобраны под линзу Bloom: multi-shop ops, заказы маркетплейс + прямые, dual status, inbox WA/TG/MAX, каталог, роли, аналитика.

**Вывод однозначный:**

1. **Ни один кандидат не годится как база продукта.** ERPNext/Dolibarr — ERP-тяжесть и email-эпоха. Chatwoot — inbox без заказов. Twenty/Krayin/Espo — sales CRM / metadata-платформы без fulfillment-spine.
2. **Bloom = greenfield modular monolith** с кражей лучших *контрактов*: multi-axis статусы (ERPNext/Dolibarr), shop scope (ERPNext User Permission), omni-inbox (Chatwoot), modern shell (Twenty), entity/ACL (Espo), menu+pipeline config (Krayin).
3. **Ядро домена — Order**, не Lead/Opportunity. **Inbox — peer-модуль**, связанный с Order, не «CRM на письмах».
4. **Dual status обязателен:** fulfillment × payment (+ channel sync для маркетплейса). Один Kanban-enum = антипаттерн.
5. **Shop — first-class entity**, не Company, не Workspace, не Team, не Warehouse.
6. **MVP = пакеты 1–2–4–5 ТЗ** (каркас + заказы + прямые + алерты); маркетплейс (п.3) и чаты (п.6) — следующие волны.

**Fit-лидеры shortlist:** Chatwoot (inbox), ERPNext (ops/order), Espo (entity/status design), Twenty (UX bar). **Аутсайдеры как product base:** все шесть. **Как pattern library:** все шесть полезны.

---

## 2. Scoreboard — fit scores (Bloom lens)

Оценки из analyzer-отчётов (overall Bloom fit, 1–10). «Adopt» = готовность развернуть as-is; «Steal» = ценность как эталон паттернов.

| # | Product | Overall | Orders / ops | Multi-shop | Dual status | Inbox WA/TG/MAX | Catalog / stock | UX modernity | Adopt-as-is | Steal value | Role for Bloom |
|--:|---------|--------:|-------------:|-----------:|------------:|----------------:|----------------:|-------------:|------------:|------------:|----------------|
| 1 | **ERPNext** | **7.0** | 9 | 8 | 8 | 2 | 8 | 4 | 3 | **9** | Ops/order/status bible |
| 2 | **Chatwoot** | **7.5*** | 2 | 5 | 2† | **9** | 1 | 9 | 4 | **9** | Inbox + assignment bible |
| 3 | **EspoCRM** | **6.5** | 3 | 5 | 5‡ | 3 | 3 | 7 | 3 | **8** | Entity/Kanban/ACL design |
| 4 | **Twenty** | **6.0** | 3 | 4 | 4‡ | 2.5 | 2 | **9.5** | 4 | **9** | UX / views / Cmd+K bar |
| 5 | **Dolibarr** | **5.5** | 8 | 4 | 8 | 2 | 7 | 3 | 2 | **8** | Document chain + billed∥status |
| 6 | **Krayin** | **5.0** | 4 | 5 | 3 | 4 | 4 | 7 | 3 | **6** | Menu+ACL, pipeline schema |

\* Chatwoot: ~8/10 как **inbox-модуль**, ~4/10 как full CRM; overall ~7.5 отражает критичность inbox для Bloom.  
† Dual status на *orders* отсутствует; conversation status ≠ order dual.  
‡ Два Select/enum + views возможны, native dual-axis нет.

### Сводный вердикт по shortlist

| Вопрос | Ответ |
|--------|--------|
| Fork ERPNext/Dolibarr? | **Нет** — GL, manufacturing, GPL, dense Desk |
| Fork Chatwoot? | **Нет** — support-core; нет Order/Shop |
| Fork Twenty/Espo/Krayin? | **Нет** — sales/metadata, AGPL/MIT риски, нет ops spine |
| Embed Chatwoot sidecar? | **Maybe** пилот; целевой путь — native inbox в Bloom |
| Что строить? | **Greenfield Bloom** по blueprint §10 |

---

## 3. What we STEAL from each

### ERPNext — ops backbone

- Multi-axis status: delivery × billing × payment + Hold / Close / Cancel семантика
- Document chain: Order → Fulfillment event → Payment event (не god-object)
- Partial % delivered / % billed → partial lines / partial cancel
- Multi-shop isolation: Role + record scope (User Permission) на shop
- Party split: Customer ≠ Contact ≠ Address → Buyer ≠ Recipient ≠ DeliveryAddress
- Workspace / role cabinets (магазин vs сеть)
- `ref_ext` / inter-company ref → marketplace external id link
- Naming series, timeline на документе, auto REST mindset
- **Не брать:** GL, manufacturing, Lead→Opportunity как ядро, email-inbox, Shop=Company

### Dolibarr — dual status + document links

- **Параллельные оси:** `fk_statut` (lifecycle) ∥ `billed` (оплата) — главный didactic steal
- Order → Expedition(s) → Invoice со связями; partial shipments
- `ref_ext` / `ref_client` для маркетплейса
- Triggers/hooks + extrafields
- Contact roles на документе (SHIPPING / BILLING)
- Fine-grained rights: create vs validate vs close
- **Не брать:** MultiCompany-as-shops, Ticket-as-inbox, PHP monolith fork, integer-only enums без map маркетплейса

### Chatwoot — unified inbox

- Inbox = channel line + membership ACL
- Contact + ContactInbox(`source_id`) — multi-channel identity
- Conversation: open / pending / resolved / snoozed + `waiting_since`
- Assignee + Team; Mine / Unassigned / All / Mentions
- Message: incoming/outgoing/activity, private notes, delivery status, attachments
- 3-pane desk: list | thread | **context sidebar (Order panel)**
- Channel capability registry (WA 24h window, TG cold-start ban)
- API channel → адаптер MAX
- Round-robin / capacity; bot pending → handoff → open
- Dashboard Apps / Shopify pattern → **create/link order from chat**
- Hierarchy: Network → Shop → InboxLine → Conversation
- **Не брать:** fork Rails monolit, Inbox=Shop, conversation status как order status, Help Center/Captain в MVP

### Twenty — modern CRM UX floor

- Table / Kanban / Calendar на core entities
- Saved views (private/shared), favorites, folders
- Record page = widget grid (status, customer, shop, timeline, chat embed)
- Cmd+K command palette
- Column aggregations; group-by Select
- Dual status as **two Selects** + dedicated views
- Workspace = tenant; **Shop = data object** (не workspace-per-shop)
- Workflows: webhook + record event + HTTP для marketplace intake
- Soft delete vs destroy
- **Не брать:** Opportunity=Order, AGPL fork, email-as-inbox, single stage field

### Krayin — modular admin CRM patterns

- Declarative **menu + ACL** config (IA ⇄ RBAC)
- Modular package boundaries (Order / Shop / Messenger / Catalog)
- Pipeline stage schema: code, name, sort, rotten_days → **SLA aging**
- Sources dictionary → marketplace / direct / phone / chat
- Kanban + list dual view; Quick Add multi-entity
- Custom attributes EAV для shop-specific полей
- Activity timeline; workflows + webhooks
- Groups + view_permission (soft scope до hard shop scope)
- **Не брать:** Lead=Order, groups=shops, email folders=messenger, paid multi-tenant как multi-shop

### EspoCRM — entity & status contract

- Entity Manager mindset: custom entity first-class (list/detail/kanban)
- **Status Field → Kanban** contract (primary axis = fulfillment only)
- Side panel: assignee + teams/shops + statuses always visible
- Bottom panels: lines, chat, payments, courier
- Layout Sets by role/team (florist ≠ dispatcher ≠ network)
- Case/Stream split: Claim ≠ Order
- Teams + role level own|team|all; field-level security
- Manual action buttons (guarded transitions)
- Pipelines-as-**flow variants** (marketplace vs direct stage sets) — **не** dual-axis
- Formula/guards на illegal transitions
- REST-first, every entity equal for SPA/bots/workers
- **Не брать:** Opportunity=Order, single overloaded enum, Teams=ERP multi-shop, Advanced Pack dependency, custom SPA framework lock-in

---

## 4. Target Bloom domain model

### 4.1 Entity graph (canonical)

```
Organization (Network)                    # tenant / франчайзи-сеть
  ├── Shop[]                              # ops unit: адрес, часы, зоны, слоты, рейтинг
  │     ├── StaffAssignment[]             # User ↔ Shop + role override
  │     ├── InboxLine[]                   # WA/TG/MAX line bound to shop or network
  │     ├── StockItem[]                   # per-shop stock on Product
  │     └── CatalogOverride[]             # price, visible, discount
  ├── User[]                              # staff
  │     └── Role / PermissionScope
  ├── Customer[]                          # buyer master
  │     ├── ChannelIdentity[]             # (channel, source_id) per messenger
  │     └── addresses, phones, notes
  ├── Product[]                           # global catalog SKU / bouquet template
  │     └── categories, media, base price
  ├── Order[]
  │     ├── OrderLine[]
  │     ├── fulfillment_status            # axis A
  │     ├── payment_status                # axis B
  │     ├── channel_sync_status           # axis C (marketplace only)
  │     ├── channel: marketplace|direct_*
  │     ├── external_ids (marketplace ref)
  │     ├── shop_id, assignee_id
  │     ├── Customer (payer), Recipient, DeliveryAddress
  │     ├── DeliverySlot / delivery_at
  │     ├── photos[], postcard, timeline
  │     └── Conversation? (link)
  ├── Conversation[]
  │     ├── Message[]
  │     ├── status, assignee, team, priority
  │     ├── inbox_line_id, shop_id
  │     └── order_id?
  ├── Notification[] / OutboxEvent[]
  ├── IntegrationConnection[]             # marketplace keys, messenger bridges
  └── AuditLog[]
```

### 4.2 Core entities (fields sketch)

| Entity | Key fields | Notes |
|--------|------------|--------|
| **Shop** | name, city, timezone, address, hours, delivery_zones, active, marketplace_account? | First-class; not Warehouse-only |
| **User / Role** | role enum + permission keys; shop scopes | network_admin, shop_manager, florist, courier, analyst |
| **Order** | channel, external_id, shop_id, dual+channel statuses, amounts, slot, notes | **Primary work object** |
| **OrderLine** | product_id?, title, qty, price, options, photo_ref | Partial fulfill/cancel qty |
| **Customer** | name, phones[], emails[], tags, LTV cache | Merge by phone |
| **Recipient** | name, phone, address | On Order; ≠ payer |
| **Conversation** | inbox_line, contact, status, assignee, order_id | Lifecycle ≠ order status |
| **Message** | type, private, content, attachments, delivery_status | Activity events in-thread |
| **Product** | sku, title, media, base_price, category | Network catalog |
| **Stock** | shop_id × product_id → qty, reserved | Per-shop |
| **Notification** | type, target_user, payload, channel (TG/VK/push) | SLA 3 min, new order, health |
| **ChannelIdentity** | customer_id, channel, source_id | Chatwoot ContactInbox pattern |
| **InboxLine** | shop_id?, channel, credentials, hours, assignment_policy | Channel adapter bind |
| **Claim/Case** (optional) | order_id, status, stream | Espo Case — exceptions only |

### 4.3 Invariants

1. **Bloom = source of truth** для ops-статусов; маркетплейс — consumer/producer через adapter.
2. **Прямой заказ никогда не уходит** на маркетплейс.
3. **Buyer ≠ Recipient ≠ Address**.
4. **Conversation.order_id** двусторонне в UI; order не = label.
5. Photo gate: переход в delivery требует before-photo (продуктовое правило).
6. Staff видит только scoped shops, если не network role.

---

## 5. Dual-status design

### 5.1 Оси (обязательные)

| Ось | Поле | Назначение | UI |
|-----|------|------------|-----|
| **A. Fulfillment** | `fulfillment_status` | Сборка и доставка | Primary Kanban + list column |
| **B. Payment** | `payment_status` | Деньги | Chip + filter; **не** колонка того же Kanban |
| **C. Channel sync** | `channel_sync_status` | Синк с маркетплейсом | Chip на marketplace-orders only |
| **D. Hold / exception** | `hold` / flags | Пауза, нет цветов, клиент недоступен | Banner + filter |

### 5.2 Fulfillment (axis A) — recommended

```
new → accepted → in_assembly → assembled → photo_ready
  → awaiting_courier | ready_pickup → out_for_delivery → delivered → completed
```

Ветки: `cancelled`, `rejected` (+ reason), `failed_delivery`, `returned`.

Семантика ERPNext/Dolibarr:

| Действие | Смысл |
|----------|--------|
| **Cancel** | Отмена обязательства |
| **Close** (optional) | Остаток не выполнять, история сохранена |
| **Hold** | Пауза без терминации |

### 5.3 Payment (axis B)

```
unpaid → authorized? → paid → partial_refund → refunded
```

Маркетплейс-заказы чаще стартуют как **paid**; прямые — unpaid / COD / link.

**Правило Dolibarr:** никогда не кодировать «Paid» как стадию «Assembling».

### 5.4 Channel sync (axis C) — marketplace only

```
not_applicable (direct)
  | pending_push → synced → conflict → failed → needs_reconcile
```

Внешний id: `external_ids.marketplace_order_id` (Dolibarr `ref_ext` / ERPNext inter-company ref idea).

### 5.5 Derived summary badge

UI на карточке: **2–3 chips**, не один enum.

Примеры:

- `Сборка` + `Оплачен` + `Синк OK`
- `Курьер` + `Не оплачен` (direct COD)
- `Новый` + `Оплачен` + `Sync failed` (красный — health)

### 5.6 Guards

- Transition matrix в API (не только workflow-боты): illegal combos rejected.
- Manual action buttons: «Принять», «В сборку», «Фото готово», «Передать курьеру» — Espo manual workflow pattern.
- Marketplace cancel inbound → notify + блокировка опасных outbound transitions.

### 5.7 Conversation status (отдельный lifecycle)

`open | pending | resolved | snoozed` — **не смешивать** с fulfillment.

Order может жить после resolve чата; чат может оставаться open после delivered.

---

## 6. Recommended module map

Пять модулей верхнего уровня (продуктовая IA Bloom):

```
┌────────────────────────────────────────────────────────────┐
│  Shop switcher · Search/Cmd+K · Notifications · User        │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│ Заказы   │  Чаты    │ Витрина  │ Отчёты   │  Настройки     │
└──────────┴──────────┴──────────┴──────────┴────────────────┘
```

### 6.1 Заказы

| Экран | Содержание |
|-------|------------|
| Список / Kanban | Fulfillment board; filters: shop, channel (marketplace/direct), payment, SLA overdue |
| Карточка | Dual chips, lines, recipient, slot, photos, timeline, chat link, external id |
| Сегодня / ops board | Priority: new+SLA → ASAP → slot 2h → today |
| Прямой заказ | Create form; source = phone/chat/walk-in |
| Marketplace intake | Auto-created; accept + dual sync |

### 6.2 Чаты

| Экран | Содержание |
|-------|------------|
| Inbox desk (3-pane) | Mine / Unassigned / All; channel badges WA/TG/MAX |
| Thread + composer | Reply / Note; canned; capability-aware |
| Context sidebar | Contact + **Order panel** (create/link/status) |
| Contacts | Customer + identities + history |

### 6.3 Витрина

| Экран | Содержание |
|-------|------------|
| Catalog matrix | Products × shops: price, stock, visible |
| Product card | Media, base price, overrides |
| Stock lite | Per-shop qty (MVP); deep WMS later |

### 6.4 Отчёты

| Экран | Содержание |
|-------|------------|
| Dashboard | GMV, orders count, AOV, marketplace vs direct, by shop |
| Ops health | Accept SLA, late delivery, open chats wait |
| Integrations | Marketplace/messenger connection chips |

### 6.5 Настройки

| Раздел | Содержание |
|--------|------------|
| Сеть / магазины | Shops CRUD, hours, zones |
| Команда | Users, roles, shop scopes |
| Каналы | InboxLines, marketplace keys, health |
| Статусы / словари | Sources, cancel reasons, canned replies |
| Автоматизации | Webhooks, SLA rules (lite) |
| Аудит / бэкапы | Who changed what |

### 6.6 Role cabinets (ERPNext workspace idea)

| Роль | Default home |
|------|----------------|
| Менеджер | Заказы + Чаты |
| Флорист | Kanban сборки + фото gate |
| Курьер | Delivery list / later PWA |
| Владелец сети | Отчёты + health |
| Админ | Настройки |

---

## 7. Architecture sketch (greenfield web)

### 7.1 Решение

**Не fork.** Современный stack, modular monolith → optional extract inbox/workers.

| Layer | Recommendation |
|-------|----------------|
| Frontend | **React** (or Vue) SPA + design system; mobile-responsive; Cmd+K |
| API | **NestJS** or **FastAPI** modular monolith; REST (+ optional GraphQL later) |
| DB | **PostgreSQL** |
| Cache / queue | **Redis** + workers (BullMQ / RQ / Sidekiq-style) |
| Realtime | WebSocket / SSE (orders list, inbox) |
| Files | S3-compatible (Yandex Object Storage), РФ |
| Hosting | РФ (Yandex Cloud / Timeweb) — 152-ФЗ |
| Auth | Session/JWT, multi-user; 2FA later |

### 7.2 Bounded contexts (внутри monolit)

```
Identity & Org     Directory (Shop, User, Role)
Orders             Catalog / Stock
Inbox (Messenger)  Fulfillment / Delivery
Finance lite       Analytics
Integrations       Notify
  ├── MarketplaceAdapter
  ├── ChannelPort (WA | TG | MAX | API)
  └── Outbox / Inbox / Reconcile
```

### 7.3 Integration pattern

```
Marketplace webhooks/poll ──► Intake worker ──► Order upsert (idempotent)
Bloom status change ──► Outbox ──► MarketplaceAdapter (retry, DLQ)
Messenger providers ──► ChannelPort ──► Conversation/Message
Chat sidebar ──► Order service (create/link)
```

- Idempotency keys, reconcile cursor, dead-letter + owner alert (health chip).
- ChannelPort interface: `receive`, `send`, `capabilities`, `identity`, `media`.

### 7.4 Why not fork

| Base | Blocker |
|------|---------|
| ERPNext GPL | Derivative + wrong UX/vertical |
| Dolibarr GPL | Dense PHP ERP chrome |
| Chatwoot | No orders domain; Rails gravity |
| Twenty AGPL | Network copyleft + sales core |
| Espo AGPL + paid packs | Custom SPA; dual status DIY |
| Krayin | Lead-centric; multi-shop paid wrong grain |

**Steal contracts, ship Bloom IP.**

### 7.5 Extensibility (without Salesforce metadata day-1)

- Stable core entities + typed custom fields (jsonb / EAV lite)
- Webhooks + outbox for partners
- Role layouts (Layout Sets idea) — shop vs network panels
- Versioned domain module later (`bloom-ops` pack concept from Twenty Apps)

---

## 8. Phased delivery ↔ cost packages

Маппинг на **11 пакетов** из `tz-decomposition.md` и волны КП.

| Волна | Пакеты ТЗ | Состав | Outcome |
|-------|-----------|--------|---------|
| **0. Discovery** | — | API маркетплейса, messenger platform, N shops | Смета без фантазий |
| **1. Рабочий кабинет** | **1 + 2 + 4 + 5** | Auth, multi-shop, roles; Order list/card dual status; direct orders; basic push (TG/VK), SLA 3 min | Можно жить без маркетплейса |
| **2. Маркетплейс** | **3** (+ дожим 5) | Connect shops, paid intake, bidirectional status, photo if API, health alerts | End-to-end marketplace day |
| **3. Чаты** | **6** | WA + TG + MAX (API), unified inbox, order-from-chat, canned | Messenger-first ops |
| **4. Витрина и цифры** | **7 + 8** | Analytics (GMV, AOV, channel, shop); catalog price/stock/visibility | Owner + merchandising |
| **5. Запуск** | **9 + 10 + 11** | Client import, training; backups, audit, SLA support; infra opex | Cutover production |

### MVP «под ключ» (коммерция)

**Волны 1–2** (+ разведка API) ≈ минимальный sellable ops cabinet.  
**Полный контур ТЗ** без лояльности/банка ≈ волны **1–5**.

### Порядок разработки внутри волны 1

1. Org + Shop + User/Role + shop scope  
2. Order + OrderLine + dual status + timeline  
3. Direct create + list filters + Kanban fulfillment  
4. Notifications (new + SLA)  
5. Audit lite  

### Вне оценки (отдельные ТЗ)

Лояльность · эквайринг/ОФД · advanced courier PWA · peak AI · deep WMS.

---

## 9. Risks

| # | Risk | Impact | Mitigation |
|---|------|--------|------------|
| 1 | API маркетплейса: write/status/photo limits | Волна 2 рвётся | Discovery gate; adapter + reconcile; degrade gracefully |
| 2 | Конфликт статусов marketplace ↔ Bloom | Двойные отмены, злость клиента | Bloom SoT; conflict chip; outbox idempotency |
| 3 | WA grey / ban / 24h window | Inbox dead | Official API path; capability UI; template picker |
| 4 | MAX/TG policy & bridge stability | CIS-critical channels | ChannelPort + health; no mono-vendor |
| 5 | 8 Марта peak load | SLA 3 min fails | Peak mode UI; queue scale; load test |
| 6 | 152-ФЗ / PII | Legal | Host РФ, encrypt at rest, consent, audit |
| 7 | Multi-shop «все видят всё» | Data leak between shops | Default shop scope; field-level network margins |
| 8 | Overbuilding ERP (stock/GL) early | Delay MVP | Packages 1–2 first; stock lite in wave 4 |
| 9 | Treating chat status as order status | Broken analytics | Dual models §5 |
| 10 | Fork temptation (stars) | License + wrong domain | Pattern-only policy; legal review if embedding |
| 11 | Photo storage cost | Opex | Compression, retention policy, S3 lifecycle |
| 12 | Dirty client/history import | Wave 5 pain | Import tool + manual merge by phone |

---

## 10. Final «mega CRM» blueprint

Синергия **только best patterns** — операционная система цветочной сети, не sales CRM и не ERP.

### 10.1 Product formula

```
Bloom =
  ERPNext/Dolibarr order spine (multi-axis status, document events, ref_ext)
+ Chatwoot inbox desk (channels, assignment, order sidebar)
+ Twenty UX floor (tables, kanban, views, Cmd+K, record widgets)
+ Espo entity contract (Status→Kanban, layout sets, team scope, Case≠Order)
+ Krayin admin discipline (menu⇄ACL, sources, rotten/SLA, packages)
− Lead/Opportunity core
− Full accounting / manufacturing
− Email-folder-as-messenger
− Shop = Company | Workspace | Team | Warehouse
```

### 10.2 Non-negotiables

1. **Order-first** ops cabinet  
2. **Dual (+ channel) status** always visible  
3. **Shop** entity + scope  
4. **Marketplace + direct** dual intake  
5. **Unified WA/TG/MAX** inbox with order-from-chat  
6. **Role-based** cabinets and layouts  
7. **Greenfield** modern stack, РФ hosting  
8. **Health** of integrations as first-class UI  

### 10.3 Screen priority for `mega/index.html`

1. App shell: shop switcher, 5 modules, notifications  
2. Orders list + dual chips + channel filter  
3. Order detail: fulfillment actions, payment chip, photo, recipient ≠ payer, timeline  
4. Today ops + SLA strip  
5. Inbox 3-pane + create/link order  
6. Direct order create  
7. Vitrina matrix (stub)  
8. Reports KPIs marketplace vs direct  
9. Settings: shops, team, channels health  
10. Mobile-responsive nav  

### 10.4 One-line strategy (RU)

> **Bloom — greenfield ops CRM для сети салонов: заказы с dual status и маркетплейс-синком, multi-shop scope, единый inbox WA/TG/MAX с заказом из чата; эталоны — ERPNext/Dolibarr (заказы), Chatwoot (inbox), Twenty (UX), Espo (entity/ACL); продукт не форкаем — собираем синергию паттернов.**

---

## Appendix A — Comparison matrix (quick)

| Capability | ERPNext | Dolibarr | Chatwoot | Twenty | Krayin | Espo | **Bloom target** |
|------------|:-------:|:--------:|:--------:|:------:|:------:|:----:|------------------|
| Sales order ops | ★★★★★ | ★★★★★ | — | ★★ | ★★ | ★★ | ★★★★★ native |
| Dual status | ★★★★ | ★★★★★ | — | ★★★ DIY | ★ | ★★★ DIY | ★★★★★ first-class |
| Multi-shop | ★★★★★ | ★★★ | ★★★ inbox | ★★★ WS | ★★ SaaS | ★★★ teams | ★★★★★ Shop entity |
| WA/TG/MAX inbox | ★ | ★ | ★★★★★ | ★ | ★★ paid | ★ | ★★★★★ native |
| Modern UX | ★★★ | ★★ | ★★★★ | ★★★★★ | ★★★★ | ★★★★ | ★★★★★ Twenty bar |
| Marketplace dual intake | ★ DIY | ★ DIY | — | ★★ WF | ★ source | ★★ API | ★★★★★ channel model |
| Catalog/stock | ★★★★★ | ★★★★ | — | — | ★★ | ★ paid | ★★★★ wave 4 |
| Analytics ops | ★★★★ | ★★★ | ★★★ CS | ★★★ | ★★ | ★★★ | ★★★★ shop×channel |
| License for SaaS | GPL hard | GPL hard | MIT core | AGPL hard | MIT | AGPL hard | **Own code** |

---

## Appendix B — Analyzer scores (source of truth)

| id | Overall fit (report) | Primary steal |
|----|---------------------:|---------------|
| erpnext | 7.0 | Multi-axis order, multi-entity scope |
| chatwoot | 8 inbox / 4 full → **7.5** blended | Omni-inbox + assignment + order sidebar |
| espocrm | 6.5 | Entity/status/ACL/layout sets |
| twenty | 6.0 | UX shell, views, workflows |
| dolibarr | 5.5 | billed ∥ statut, document chain |
| krayin | 5.0 | Menu+ACL, pipeline, sources |

Shortlist rank (candidates): ERPNext → Dolibarr → Chatwoot → Twenty → Krayin → Espo.  
**Bloom engineering priority of references:** Chatwoot + ERPNext + Twenty + Espo (+ Dolibarr dual status, Krayin admin).

---

## Appendix C — Deliverables checklist (Gate D)

- [x] Comparison / scoreboard  
- [x] Pattern extraction (STEAL per product)  
- [x] Bloom domain model  
- [x] Dual-status design  
- [x] Module map  
- [x] Architecture (greenfield)  
- [x] Phased delivery ↔ packages  
- [x] Risks  
- [x] Mega blueprint  
- [ ] Next: `mega/index.html` (Mega builder)

---

*Synthesizer artifact · `docs/research/crm-benchmark/mega/SYNTHESIS.md` · 2026-08-01*
