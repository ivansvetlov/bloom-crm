# Chatwoot — Bloom CRM Benchmark Analysis

| Field | Value |
|-------|--------|
| **id** | `chatwoot` |
| **Product** | Chatwoot |
| **Type** | Web omni-inbox / customer support desk |
| **Repo** | https://github.com/chatwoot/chatwoot |
| **Docs** | https://www.chatwoot.com/help-center · https://developers.chatwoot.com |
| **License** | MIT (community core); proprietary overlay under `enterprise/` |
| **Stack** | Ruby on Rails · Vue 3 · PostgreSQL · Redis · Vite · ActionCable |
| **Version reviewed** | ~4.16.x (`package.json` / develop schema ~2026-07-29) |
| **Review date** | 2026-08-01 |
| **Bloom focus** | WA / TG / MAX unified inbox + create order from chat (multi-shop flower ops) |

---

## 1. Overview

Chatwoot is an open-source, self-hostable **omnichannel customer support platform** — a practical alternative to Intercom / Zendesk / Salesforce Service Cloud for conversation ops. It is **not** a sales CRM or ERP: there are no first-class orders, stock, fulfillment, or multi-shop ops entities. Its strength is a mature **shared inbox desk**: unify channels, assign agents, collaborate with private notes, automate routing, and report on conversation health.

### Positioning

| Dimension | Chatwoot |
|-----------|----------|
| Primary user | Support / success / CX teams |
| Core unit of work | **Conversation** (thread), not deal/order |
| Multi-tenant unit | **Account** (workspace) |
| Channel model | Polymorphic **Inbox → Channel** adapters |
| Commerce | Optional (Shopify integration, Dashboard Apps embed) — not native orders |
| AI | “Captain” AI agent (assistants, scenarios, knowledge, tools) |

### Why it matters for Bloom

Bloom needs a **flower multi-shop ops CRM** with:

1. **Unified messenger inbox** (WhatsApp, Telegram, MAX and similar)
2. **Agent desk workflows** (queues, assignment, collaboration)
3. **Create / link order from chat** as a first-class action

Chatwoot is the strongest open-source **inbox reference** in the shortlist (candidates rank #3 overall; #1 for inbox/channels). It should be treated as:

- **Primary STEAL target** for inbox IA, domain model, assignment, and channel adapter patterns
- **Not** a base to fork as Bloom CRM (wrong domain core: support tickets vs flower ops orders)

### High-level feature map

| Area | Capabilities |
|------|----------------|
| Omnichannel | Website widget, Email, WhatsApp (Cloud / Twilio / 360Dialog), Telegram, Facebook, Instagram, Line, TikTok, SMS, Twilio, **API channel** |
| Desk UX | Shared inbox, filters/views, labels, priority, snooze, resolve, private notes, @mentions, canned responses, macros, keyboard/command bar |
| Routing | Inbox membership, teams, round-robin / balanced assignment policies, capacity limits, automation rules |
| Contacts | Contact + ContactInbox (channel identity), companies, custom attributes, notes, segments |
| Bots / AI | Agent bots, Dialogflow hooks, Captain assistants |
| Extensibility | REST API, webhooks, Dashboard Apps (iframe embed), Shopify, Slack, Linear, Google Translate |
| Ops | Business hours, CSAT, SLA (enterprise-oriented), reports (agent/inbox/label/team), live view |
| Self-host | Docker / Helm / Heroku / DO; full data ownership |

---

## 2. Architecture

### 2.1 Stack topology

```
┌─────────────────────────────────────────────────────────────┐
│  Vue 3 Dashboard (Vite, Pinia/Vuex, Vue Router, Tailwind)   │
│  + Widget SDK + Help Center portal UI                       │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST + ActionCable (realtime)
┌───────────────────────────▼─────────────────────────────────┐
│  Rails app (API, controllers, models, services, jobs)       │
│  Event dispatcher → listeners (notifications, assignment…)  │
└───────┬─────────────────┬──────────────────┬────────────────┘
        │                 │                  │
   PostgreSQL          Redis              Sidekiq-style jobs
   (schema.rb)      (pubsub/cache)        (assignment, sync)
        │
 Channel tables (WhatsApp, Telegram, Email, API, …)
        │
 External providers (Meta Cloud API, Telegram Bot API, IMAP/SMTP, …)
```

### 2.2 Backend patterns

- **Multi-tenant by `account_id`**: almost every domain table is account-scoped.
- **Polymorphic channel**: `Inbox` → `channel` (`channel_type` + `channel_id`) pointing at `Channel::Whatsapp`, `Channel::Telegram`, `Channel::Api`, etc.
- **Contact identity per channel**: `ContactInbox` joins `Contact` ↔ `Inbox` with `source_id` (provider user/chat id) — critical for multi-channel identity.
- **Conversation as work item**: status machine, assignee (user or agent bot), team, labels, custom/additional attributes (jsonb).
- **Messages**: polymorphic sender (`User` / `Contact` / bot), `message_type` (incoming/outgoing/activity), private notes, attachments, delivery status.
- **Event bus**: Rails dispatcher on create/update/resolve/bot handoff; drives realtime UI and automations.
- **Enterprise overlay**: `enterprise/` + `prepend_mod_with` / `include_mod_with` for plan-gated features without hard-forking OSS.

### 2.3 Frontend structure (dashboard routes)

Top-level account shell: `/app/accounts/:accountId/…`

| Module | Role |
|--------|------|
| **Conversations / Inbox** | Primary desk — lists, thread, contact sidebar |
| **Contacts / Companies** | CRM-lite customer master |
| **Notifications** | Mentions, assignments, activity |
| **Captain** | AI assistants & knowledge |
| **Help Center** | Portals / articles |
| **Campaigns** | Proactive outreach |
| **Calls** | Voice (Twilio path) |
| **Settings** | Inboxes, agents, teams, automation, labels, apps, attributes… |
| **Search** | Universal search |

### 2.4 Realtime & scaling notes

- ActionCable for live conversation/message updates.
- Redis for round-robin queues, caches, unread counts.
- Per-account conversation `display_id` sequences via DB triggers (`conv_dpid_seq_{account_id}`).
- PG extensions: `pg_trgm` (search), `pgcrypto`, `vector` (Captain embeddings).

### 2.5 Deployment / ops

- Docker Compose, Helm, Heroku one-click, DigitalOcean.
- Typical deps: Postgres, Redis, storage (S3/compatible), SMTP, optional OpenAI for Captain.
- Heavy product for a pure Bloom inbox MVP if forked whole — better as **pattern library** than runtime dependency unless embedding Chatwoot as a module.

---

## 3. Domain model

### 3.1 Core entity graph

```
Account
  ├── AccountUser (role: administrator | agent, availability, capacity policy)
  ├── User (agent identity)
  ├── Team ── TeamMember
  ├── Inbox ── InboxMember (agents who can see/work this channel)
  │     └── Channel::* (WhatsApp | Telegram | Email | API | …)
  │     └── AssignmentPolicy (via InboxAssignmentPolicy)
  │     └── AgentBot / CaptainAssistant (optional)
  ├── Contact
  │     └── ContactInbox (source_id per inbox/channel)
  │     └── Note
  ├── Company (optional B2B grouping)
  ├── Conversation
  │     ├── assignee (User) | assignee_agent_bot
  │     ├── team
  │     ├── labels, custom_attributes, additional_attributes
  │     ├── ConversationParticipant
  │     └── Message ── Attachment
  ├── AutomationRule / Macro / CannedResponse / Label
  ├── CustomAttributeDefinition (contact | conversation)
  ├── DashboardApp (embed URL/content in conversation sidebar)
  └── Integrations::Hook (Slack, Dialogflow, Shopify, …)
```

### 3.2 Conversation (primary work object)

**Statuses** (`enum`):

| Status | Meaning |
|--------|---------|
| `open` | Active queue work |
| `resolved` | Closed from agent perspective |
| `pending` | Often bot-owned / awaiting handoff |
| `snoozed` | Temporarily hidden until `snoozed_until` |

**Priority**: `low | medium | high | urgent`.

**Key fields**:

| Field | Role for Bloom |
|-------|----------------|
| `account_id`, `inbox_id` | Tenant + channel/shop surface |
| `contact_id`, `contact_inbox_id` | Customer + channel identity |
| `assignee_id` / `assignee_agent_bot_id` | Human or bot ownership |
| `team_id` | Group ownership |
| `status`, `priority` | Queue semantics |
| `waiting_since` | Unreplied wait timer (SLA-ish) |
| `first_reply_created_at` | First response metric |
| `custom_attributes` | Extensible: order_id, shop_id, etc. |
| `additional_attributes` | System/channel metadata (language, browser, …) |
| `display_id` | Human ticket number per account |
| `uuid` | External/survey links |

**Bloom mapping**: Conversation ≈ **chat thread linked to Contact**; Bloom should add **Order** as peer object, not only jsonb attributes.

### 3.3 Inbox

Inbox is the **desk surface + channel config**:

- `name`, timezone, greeting / OOO messages, working hours
- `enable_auto_assignment`, `auto_assignment_config`
- `lock_to_single_conversation` (reuse one thread per contact vs many)
- `csat_survey_enabled` / `csat_config`
- `allow_messages_after_resolved`
- Membership via `inbox_members` — **visibility ACL**: agents only see conversations from inboxes they belong to (admins broader)

**Bloom mapping**:

| Chatwoot Inbox | Bloom analogue |
|----------------|----------------|
| One WhatsApp number inbox | Shop WA line or network WA line |
| One Telegram bot inbox | Shop/network TG bot |
| API channel inbox | MAX / custom messenger adapter |
| Multi-inbox account | Multi-shop / multi-line desk |

Important: Chatwoot **Account ≠ Shop**. Multi-brand is multi-inbox, not hierarchical multi-org. Bloom needs stronger **Shop / Branch** isolation than inbox membership alone.

### 3.4 Agents & roles

| Concept | Implementation |
|---------|----------------|
| Agent | `User` via `AccountUser` with role agent |
| Admin | `AccountUser` role administrator |
| Custom roles | `custom_roles` + permissions (enterprise-oriented) |
| Availability | online / busy / offline; `auto_offline` |
| Capacity | `AgentCapacityPolicy` + per-inbox `conversation_limit` |
| Inbox access | `InboxMember` |
| Team | `Team` + members; team-level auto-assign flag |

**Assignee model evolution**: conversation can assign to **User** or **AgentBot** (polymorphic direction via separate FKs + virtual `assignee_type`).

### 3.5 Contact & channel identity

```
Contact (name, email, phone, identifier, custom_attributes)
   └── ContactInbox (inbox_id, source_id, hmac_verified, pubsub_token)
```

- Same person can appear on WA + TG as **one Contact** with multiple ContactInboxes.
- Uniqueness: email/identifier per account; `source_id` unique per inbox.
- **Bloom STEAL**: always key messenger users by `(channel, source_id)` and merge into Contact with phone/name when known.

### 3.6 Messages

- Types: incoming / outgoing / activity (system events)
- `private: true` → internal note (not sent to channel)
- `content_type` + `content_attributes` for cards, forms, email headers, etc.
- Delivery `status` (sent / delivered / read / failed) where channel supports it
- Attachments with file type + external URL / ActiveStorage

### 3.7 Objects Chatwoot does **not** have (Bloom gap)

| Bloom need | In Chatwoot? |
|------------|--------------|
| Order / line items / delivery slot | No (Shopify embed only) |
| Dual status (payment vs fulfillment) | No |
| Multi-shop hierarchy / network rollup | Weak (inboxes only) |
| Marketplace vs direct intake | No |
| Florist / courier roles | No (agent roles only) |
| Catalog / pricing / stock | No |

---

## 4. UI / Information architecture

### 4.1 Agent desk layout (canonical 3–4 pane)

Industry-standard support desk that Bloom should mirror for the **Inbox module**:

```
┌────────┬──────────────────┬────────────────────────┬─────────────────┐
│ Global │ Conversation     │ Thread                 │ Context         │
│ nav    │ list             │ (messages + composer)  │ sidebar         │
│        │                  │                        │                 │
│ Inbox  │ Filters:         │ Header: status,        │ Contact card    │
│ Cont.  │  Mine /          │ assignee, priority,    │ Attributes      │
│ Notif. │  Unassigned /    │ labels, actions        │ Previous convos │
│ Capt.  │  All /           │                        │ Labels          │
│ Help   │  Mentions /      │ Timeline of messages   │ Macros          │
│ Set.   │  Teams /         │ + activity events      │ Dashboard Apps  │
│        │  Custom views    │                        │ (Shopify/order) │
│        │                  │ Composer: reply /      │                 │
│        │ Unread badges    │ private note, attach,  │                 │
│        │ Channel icons    │ canned, emoji          │                 │
└────────┴──────────────────┴────────────────────────┴─────────────────┘
```

### 4.2 Navigation IA

| Area | Contents |
|------|----------|
| **Conversations** | Default home; status tabs (Open / Resolved / Pending / Snoozed); assignee facets |
| **Inbox filter tree** | All inboxes + per-inbox; labels-as-folders (`show_on_sidebar`) |
| **Contacts** | List, profile, conversation history, notes, segments |
| **Companies** | B2B grouping (secondary for Bloom B2C flower) |
| **Reports** | Live, agent, inbox, label, team, CSAT |
| **Campaigns** | Proactive messages |
| **Captain** | AI configuration & copilot |
| **Help Center** | Knowledge base for deflection |
| **Settings** | Agents, teams, inboxes, automations, attributes, integrations, audit |

### 4.3 Conversation actions (header / command bar)

- Assign agent / team
- Change status (open/resolve/pending/snooze)
- Priority
- Labels
- Participants / @mention
- Mute, merge contact, delete (admin)
- Macros (batch actions)
- CSAT trigger
- Channel-aware composer (formatting limited by channel capabilities)

### 4.4 UX patterns worth noting

| Pattern | Detail |
|---------|--------|
| **Custom views / filters** | Saved query JSON (`custom_filters`) per user |
| **Canned responses** | Short codes for rapid reply |
| **Private notes + @mentions** | Internal collab without customer visibility |
| **Keyboard / command bar** | Power-user desk speed |
| **Channel capability awareness** | Editor features enable/disable by channel (WA 24h window, TG formatting, etc.) |
| **Lock to single conversation** | Per-inbox policy for continuous chat vs ticket-per-issue |
| **Business hours + OOO** | Per-inbox expectation setting |
| **Dashboard Apps** | Iframe panels in conversation context — **order UI injection point** |

### 4.5 Mobile

Official mobile apps exist for agents; web is primary research target for Bloom web MVP.

---

## 5. Assignment workflows

### 5.1 Visibility before assignment

1. Conversation lands in an **Inbox** (channel).
2. Only **inbox members** (+ admins) see it.
3. Optional **Team** ownership further scopes auto-assign pool.

### 5.2 Manual assignment

- Pick agent from assignable set (inbox members ∪ admins).
- Assign team.
- Self-assign from unassigned queue (common “pull” model).
- Add participants without making them primary assignee.

### 5.3 Auto-assignment (legacy + v2)

**Legacy path** (`AutoAssignment::AgentAssignmentService`):

- Triggered when conversation becomes open and assignee blank (or assignee not in inbox).
- Pool = inbox members with capacity; if team set, intersect team members when `allow_auto_assign`.
- Round-robin style distribution historically stored in Redis queues per inbox.

**Assignment v2** (feature flag `assignment_v2`):

- Central **AssignmentPolicy** per account, linked 1:1 to inbox via `inbox_assignment_policies`.
- Policy fields (schema):
  - `assignment_order` — round-robin vs balanced
  - `conversation_priority` — earliest created vs longest waiting
  - `fair_distribution_limit` / `fair_distribution_window`
  - `exclude_older_than_hours`
  - `enabled`
- **Capacity**: `AgentCapacityPolicy` + `inbox_capacity_limits.conversation_limit`; exclusion rules (e.g. ignore certain labels/statuses).
- Job coalescing: `AutoAssignment::AssignmentJob.enqueue_for_inbox` on open **and** on resolve/snooze (to free capacity and rebalance).

### 5.4 Automation rules & macros

| Tool | Trigger / use |
|------|----------------|
| **AutomationRule** | Event-driven: conditions JSON + actions JSON (assign, label, mute, send message, …); optional delay |
| **Macro** | Manual multi-action bundle on open conversation |
| **Labels** | Workflow tags; can drive filters/automations |
| **Agent bot / Captain** | Conversations start `pending` with bot assignee; **handoff** → open + waiting_since |

### 5.5 Status-driven queue semantics

| Transition | Effect |
|------------|--------|
| New → pending (bot) | Stays out of human open queue until handoff |
| Bot handoff → open | Enters assignment pool; sets `waiting_since` |
| open → resolved | Clears wait; may free capacity (v2) |
| open → snoozed | Hidden until time; capacity reclaim path in v2 |
| Contact blocked | New conv can auto-resolve |

### 5.6 Bloom relevance

For multi-shop flower desks:

- **Pull queue** (Unassigned → Mine) + optional **auto-assign round-robin** both needed.
- Capacity limits map well to “max concurrent chats per florist/operator”.
- Team ≈ “shop shift team” or “network dispatch vs shop floor”.
- Bloom should add **shop-scoped queues** (not only inbox/channel queues).

---

## 6. Channel integrations

### 6.1 Supported channels (native)

| Channel | Table / type | Bloom priority |
|---------|--------------|----------------|
| WhatsApp Cloud / providers | `channel_whatsapp` | **P0** |
| Telegram | `channel_telegram` (bot_token) | **P0** |
| API (generic) | `channel_api` (webhook + hmac + identifier) | **P0 for MAX** |
| Website widget | `channel_web_widgets` | P2 |
| Email | `channel_email` | P2 |
| Facebook / Instagram | pages / IG | P2 |
| SMS / Twilio | SMS tables | P3 |
| Line / TikTok / Twitter | respective tables | P3 |

### 6.2 Channel adapter pattern (STEAL)

Each channel:

1. Has credentials + provider config (jsonb).
2. Binds to exactly one **Inbox**.
3. Receives webhooks → creates/finds **Contact** + **ContactInbox** by `source_id` → appends **Message** → bumps **Conversation**.
4. Sends outbound via provider client; updates delivery status async.
5. Enforces **channel policy** (WA 24h template window, TG no unsolicited outbound start, size limits, formatting).

**API channel** is the extension point for messengers Chatwoot does not ship (e.g. **MAX**): external bridge posts messages into Chatwoot and receives outbound via webhook.

### 6.3 Channel capability matrix (summary)

From official supported-features docs:

| Concern | WhatsApp | Telegram | API |
|---------|----------|----------|-----|
| In/out messages | Yes | Yes | Yes |
| Attachments | Yes (typed limits) | Yes | Yes |
| Reply-to | Cloud: yes | Yes | Yes |
| Outbound start | Templates after 24h | Customer must start | Configurable |
| Read receipts | Yes | No | Yes |
| Auto-assignment | Yes | Yes | Yes |

Bloom must encode the same **policy layer** per channel so agents see why reply is blocked (especially WA).

### 6.4 Commerce / order-adjacent integrations

| Integration | Pattern | Bloom takeaway |
|-------------|---------|----------------|
| **Shopify** | Official hook: view/manage orders **in conversation context** | Closest to “order from chat” — sidebar commerce panel |
| **Dashboard Apps** | Admin registers URL; iframe in conversation sidebar with conversation/contact context | **Best extension model** for Bloom order mini-app |
| **Linear** | Create tickets from chat | Pattern for “create entity from conversation” |
| **Slack** | Mirror desk in Slack | Secondary; not Bloom core |
| **Webhooks + REST API** | Full programmatic control | Required if Bloom owns order domain and Chatwoot is only inbox |

### 6.5 WhatsApp specifics

- Cloud API embedded signup or manual (phone number id, business id, token).
- Template store on channel (`message_templates` jsonb).
- Health metadata on phone number.
- Strict messaging window → agent UI must surface template picker when outside window.

### 6.6 Telegram specifics

- Bot token based (`channel_telegram`).
- Customer must initiate; agents cannot cold-start TG threads (platform constraint).
- Good attachment support; limited rich formatting vs web.

### 6.7 MAX (and other CIS messengers)

- **No native MAX channel** in Chatwoot as of review.
- Path: **API channel + bridge service** (MAX Bot API ↔ Chatwoot webhooks), or custom Channel model if forking.
- Bloom should design **ChannelPort** interface: `receive`, `send`, `capabilities`, `identity`, `media` — implement WA/TG/MAX behind it (Chatwoot-like).

---

## 7. STEAL for Bloom inbox

Prioritized patterns to copy into Bloom (not the Rails monolith itself).

### 7.1 Domain (must)

1. **Inbox as channel + membership ACL** — agents only see lines they staff.
2. **Contact + ContactInbox (`source_id`)** — multi-channel identity without duplicate people.
3. **Conversation statuses**: open / pending / resolved / snoozed + waiting_since.
4. **Assignee + Team dual ownership** — person responsible + group queue.
5. **Message model** with private notes, activity events, delivery status, attachments.
6. **jsonb custom_attributes** on conversation/contact for shop_id, order_id, delivery_date early on.
7. **Channel capability registry** — composer and validation per WA/TG/MAX.

### 7.2 Assignment (must)

1. Facets: **Mine / Unassigned / All / Mentions / Team**.
2. Manual assign + self-assign pull.
3. Optional **round-robin / balanced** policies with **capacity limits**.
4. Automations: on message / on create → label, assign shop team, notify.
5. Bot/automation **pending → handoff → open** for order intake bots.

### 7.3 UI/IA (must)

1. **3-pane desk**: list | thread | context sidebar.
2. Channel icon + inbox name on every list row.
3. Header actions: status, assignee, labels, priority.
4. Composer tabs: **Reply | Internal note**.
5. Canned responses / snippets for flower FAQ (“доставка сегодня”, “состав букета”).
6. **Context sidebar slot for Order panel** (Chatwoot Dashboard Apps / Shopify pattern).
7. Saved filters / folders for “Новые заказы”, “Ждут оплаты”, “Проблема доставки”.

### 7.4 Order-from-chat (must adapt)

Chatwoot’s Shopify/Dashboard App pattern → Bloom first-class:

| Action in thread sidebar | Result |
|--------------------------|--------|
| Создать заказ | New Order draft prefilled from Contact + channel |
| Привязать заказ | Link existing order id to conversation |
| Карточка заказа | Status chips (оплата / сборка / доставка), address, slot, amount |
| Быстрые реплаи | “Заказ #{n} принят”, payment link, tracking |

Do **not** store order as only a label — store `conversation.order_id` + bidirectional UI.

### 7.5 Multi-shop (adapt)

| Chatwoot | Bloom |
|----------|-------|
| Multiple inboxes | Multiple **shops × channels** |
| Teams | Shop crews + network dispatch |
| Account | Network / franchise org |
| Labels | Ops tags (срочный, витрина, маркетплейс) |

Recommend hierarchy: `Network → Shop → Inbox(ChannelLine) → Conversation`.

### 7.6 Extensibility (should)

1. Webhooks on conversation/message events for external bots.
2. Embeddable sidebar apps (order CRM panel).
3. API channel for MAX and future messengers.
4. CSAT / first response metrics later (ops quality).

### 7.7 Technical STEALs

- Per-tenant display_id sequences.
- Soft channel windows & template UX for WA.
- Realtime list updates (WebSocket).
- Activity messages in-thread (“assigned to X”, “resolved by Y”).
- Unread counts by assignee/inbox with cache invalidation discipline.

---

## 8. AVOID

| # | Avoid | Why |
|---|--------|-----|
| 1 | **Forking Chatwoot as Bloom CRM core** | Support-centric schema; enterprise overlay; no orders/stock/shops; Rails+Vue stack may not match Bloom stack |
| 2 | **Treating Inbox as Shop** | One shop has many channels; one channel may serve network-level line — need explicit Shop entity |
| 3 | **Only single status field for ops** | Chatwoot conversation status ≠ payment/fulfillment dual status Bloom needs on **orders** |
| 4 | **Hiding channel limits** | WA 24h window failures frustrate agents; always surface constraints |
| 5 | **Overbuilding Captain/Help Center first** | Bloom MVP is ops desk + orders, not knowledge base AI |
| 6 | **Enterprise-only mental model** | SLA, advanced capacity, custom roles live partly in paid overlay — don’t depend on them for OSS-like Bloom MVP |
| 7 | **Omnichannel everything on day 1** | Ship TG + WA + API(MAX) first; defer IG/TikTok/email |
| 8 | **Conversation without Order link** | Pure support desk UX fails florist “create order from chat” job-to-be-done |
| 9 | **Ignoring `lock_to_single_conversation` choice** | Flower sales often want continuous chat per customer; support tickets want new thread per issue — product decision required |
| 10 | **Monolithic channel code without ports** | Chatwoot’s many Channel::* tables work but Bloom should keep a thin adapter interface for CIS messengers |

---

## 9. Web MVP notes — TG-like desk for Bloom

Goal: standalone **web structure MVP** of a Telegram-class agent desk (pattern-inspired by Chatwoot), not a full Chatwoot deploy.

### 9.1 MVP screens (structure)

1. **Login / shop context switcher** (multi-shop).
2. **Inbox desk** (default):
   - Left: Mine | Unassigned | All; filter by channel (TG / WA / MAX).
   - Center: conversation list (avatar, name, last message, channel badge, waiting time).
   - Main: thread + composer (Reply / Note).
   - Right: Contact + **Order panel** (create / link / status).
3. **Contacts** list + profile with conversation history.
4. **Settings lite**: agents, inbox lines, canned replies (stub).
5. Optional: simple reports (open count, unassigned, median wait) — placeholder charts OK.

### 9.2 Minimum data model for MVP HTML/API later

```text
Shop, Agent, InboxLine(channel: tg|wa|max), Contact, ContactIdentity,
Conversation(status, assignee, shop_id, order_id?),
Message(private?, type), Order(dual statuses… stub)
```

### 9.3 TG-first behaviors to mock in UI

- Channel badge “TG”.
- No cold outbound (disabled “new conversation” or explain “клиент пишет первым”).
- Attachments: photo of bouquet (common flower case).
- Bot handoff banner: “Бот передал оператору”.
- Create order CTA always visible in sidebar when no `order_id`.

### 9.4 Interaction flows to prototype

| Flow | Steps |
|------|--------|
| Pull work | Unassigned → open → self-assign → reply |
| Order create | Open chat → Создать заказ → draft fields → save → status chips in sidebar |
| Order link | Search order by phone → attach to conversation |
| Handoff shop | Assign team/shop B; label “эскалация” |
| Resolve | Resolve conversation; order may stay open (dual lifecycle) |

### 9.5 Structure MVP file expectation

Per orchestrator: `mvp/chatwoot/index.html` should reflect **Chatwoot’s IA** (Conversations, Contacts, Reports, Settings, channel list), labeled as Chatwoot structure MVP — not Bloom skin. Bloom-specific mega UI belongs under `mega/`.

### 9.6 If evaluating runtime Chatwoot for pilot

- Docker-compose self-host + Telegram bot inbox + API channel stub for MAX.
- Embed Bloom order UI via **Dashboard App** iframe passing conversation/contact ids.
- Use webhooks to sync Contact phone → Bloom Order service.
- Do **not** expect multi-shop network analytics from Chatwoot alone.

---

## 10. Fit score for Bloom inbox module

### Scoring rubric (inbox module only)

| Criterion | Weight | Score (1–10) | Notes |
|-----------|--------|--------------|-------|
| Unified messenger model | 20% | 9 | Mature omni-inbox; API for missing channels |
| WA / TG readiness | 15% | 9 | First-class WA + TG |
| MAX / CIS messengers | 10% | 5 | Via API bridge only |
| Assignment & agent workflows | 15% | 9 | Policies, capacity, teams, automation |
| UI desk quality | 15% | 9 | Best-in-class OSS support desk IA |
| Order-from-chat | 15% | 4 | Shopify/Dashboard Apps only — not native orders |
| Multi-shop ops isolation | 10% | 5 | Multi-inbox/teams, not shop hierarchy |

**Weighted ≈ 7.6 → Fit score: 8 / 10 for Bloom *inbox module***  
**(≈ 4 / 10 as full Bloom CRM replacement)**

### Verdict

| Use Chatwoot as… | Recommendation |
|------------------|----------------|
| **Pattern bible for Bloom Inbox** | **Strong yes** |
| Sidebar “create order” UX reference (Shopify/Dashboard Apps) | **Yes** |
| Production inbox microservice beside Bloom orders | **Maybe** (if stack/ops accept Rails service + bridges) |
| Core of Bloom multi-shop flower CRM | **No** |

### One-line recommendation (RU)

> **Chatwoot — лучший open-source эталон unified inbox (WA/TG/API) и agent desk; для Bloom красть IA, модель Conversation/Inbox/ContactInbox и assignment, а заказы, dual status и multi-shop строить в своём домене, подключая order-panel по образцу Dashboard Apps/Shopify.**

---

## 11. Mapping: Chatwoot → Bloom

| Chatwoot concept | Bloom concept |
|------------------|---------------|
| Account | Network / organization |
| Inbox + Channel | Shop (or network) messaging line |
| InboxMember | Agent staffing a line / shop desk |
| Team | Shop shift team or dispatch group |
| Agent (User) | Operator / florist manager / support |
| Contact | Customer |
| ContactInbox.source_id | Messenger user id (tg_id, wa_id, max_id) |
| Conversation | Chat thread (ops work item) |
| Conversation.status | Thread lifecycle (not order status) |
| Message / private note | Customer message / internal collab |
| Label | Ops tag |
| Custom attributes | shop_id, order_id, source=marketplace\|direct |
| Assignment policy | Desk load balancing |
| Agent capacity | Max concurrent chats |
| Automation rule | Intake routing, SLA nags, shop routing |
| Agent bot / Captain | Order intake / FAQ bot |
| Dashboard App / Shopify panel | **Order create/link panel in chat** |
| Reports (CSAT, first response) | Inbox KPIs (later) |
| Help Center | Optional; low priority for ops MVP |
| — (missing) | **Order, dual status, stock, courier, marketplace intake** |

---

## 12. Sources

| Source | URL |
|--------|-----|
| GitHub repo | https://github.com/chatwoot/chatwoot |
| README / features | develop branch README |
| Schema | `db/schema.rb` (conversations, inboxes, channels, assignment_policies, …) |
| Models | `app/models/conversation.rb`, `inbox.rb`, `account.rb` |
| Auto-assignment | `app/models/concerns/auto_assignment_handler.rb` |
| Dashboard routes | `app/javascript/dashboard/routes/dashboard/dashboard.routes.js` |
| Channel capabilities | https://developers.chatwoot.com/self-hosted/supported-features |
| Product docs | https://www.chatwoot.com/help-center |
| Assignment / capacity features | https://www.chatwoot.com/features/assignments · agent capacity |
| Candidates shortlist | `docs/research/crm-benchmark/00-candidates.md` |

---

## 13. Analyzer checklist (orchestrator)

| Required topic | Covered in section |
|----------------|--------------------|
| Meta / positioning | §1 |
| IA | §4 |
| Core objects | §3 |
| Multi-shop / multi-tenant | §3.3, §7.5, §11 |
| Communication / inbox | §3–6 |
| Status & workflow | §3.2, §5 |
| Analytics | §1 reports, §4 nav |
| Extensibility / API / self-host | §2, §6.4, §7.6 |
| Steal / avoid | §7–8 |
| Mapping CRM → Bloom | §11 |
| Fit score | §10 |

---

*End of report — `{id}: chatwoot`*
