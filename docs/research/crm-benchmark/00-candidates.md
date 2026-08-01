# Open-source CRM candidates for Bloom benchmark

Research date: 2026-08-01  
Scope: Ready-to-run open-source CRM / ops platforms (web or desktop) relevant to Bloom-like flower-shop ops CRM: marketplace + direct orders, multi-shop, multi-channel inbox (WA/TG/MAX), statuses, analytics.

**Ranking** (1 = strongest fit for Bloom-like product: ops + multi-entity + UI richness):  
1 ERPNext · 2 Dolibarr · 3 Chatwoot · 4 Twenty · 5 Krayin CRM · 6 EspoCRM

Stars/licenses via GitHub API on 2026-08-01 (approx).

## Candidates

### 1. ERPNext
- repo: https://github.com/frappe/erpnext
- stars: ~37.5k
- license: GPL-3.0
- type: web
- stack: Python (Frappe Framework) / Vue (Frappe UI) / MariaDB
- relevance: Full ops ERP with multi-company, sales/purchase orders, stock, shipping/fulfillment, CRM module, and analytics — closest open product model to multi-shop flower operations.
- last activity: very active (pushed 2026-08-01); ~60k commits

### 2. Dolibarr
- repo: https://github.com/Dolibarr/dolibarr
- stars: ~7.5k
- license: GPL-3.0+
- type: web (also packaged desktop-style installers: DoliWamp etc.)
- stack: PHP / JavaScript / MySQL|MariaDB|PostgreSQL
- relevance: Shop-scale ERP/CRM: customer orders, stock/warehouses, POS, invoices, multi-user rights; multi-company via module — practical reference for retail ops + order status flows.
- last activity: very active (pushed 2026-07-31); ~156k commits

### 3. Chatwoot
- repo: https://github.com/chatwoot/chatwoot
- stars: ~35.3k
- license: MIT (community core); proprietary license for `enterprise/` features
- type: web
- stack: Ruby on Rails / Vue.js / PostgreSQL / Redis
- relevance: Omni-channel support desk (WhatsApp, Telegram, email, social, live chat) — best open reference for Bloom-style WA/TG/MAX unified inbox and agent workflows.
- last activity: very active (pushed 2026-08-01)

### 4. Twenty
- repo: https://github.com/twentyhq/twenty
- stars: ~54k
- license: AGPL-3.0 (repo SPDX: Other / NOASSERTION; project markets AGPL-3.0)
- type: web
- stack: TypeScript / NestJS / React / PostgreSQL / Redis
- relevance: Modern Salesforce-class CRM with custom objects, views, workflows, multi-workspace model, and rich UI — strong benchmark for CRM UX, statuses, and extensibility (weaker on native order/stock ops).
- last activity: very active (pushed 2026-08-01); 14k+ commits

### 5. Krayin CRM
- repo: https://github.com/krayin/laravel-crm
- stars: ~23.6k
- license: MIT
- type: web
- stack: Laravel (PHP) / Vue.js / MySQL
- relevance: Full lifecycle SME CRM with modular architecture, multi-tenant SaaS extension path, and official WhatsApp/VoIP extensions — useful for multi-entity CRM + messaging channel patterns.
- last activity: active (pushed 2026-07-31); branch 2.2, 4k+ commits

### 6. EspoCRM
- repo: https://github.com/espocrm/espocrm
- stars: ~3.2k
- license: AGPL-3.0
- type: web (SPA)
- stack: PHP (REST API) / custom SPA frontend (JS/TS) / MySQL|MariaDB|PostgreSQL
- relevance: Mature, highly customizable CRM platform (entities, fields, workflows, cases, email, kanban) with clean admin UX — good blueprint for order/status entity modeling without ERP bulk.
- last activity: active (pushed 2026-07-30); ~23k commits

---

## Excluded / deferred (notable)

| Product | Why not in final 6 |
|--------|---------------------|
| Odoo | Excellent multi-company/orders depth, but dual CE/EE model and enterprise module lock-in complicate “pure OSS CRM” benchmarking. |
| SuiteCRM | Solid enterprise CRM (~5.6k★, AGPL-3.0), active; more classic sales CRM than shop ops + inbox. |
| IDURAR ERP CRM | Node/React ERP-CRM (~8.6k★); weaker recent activity signal vs finalists. |
| Monica | Personal CRM — not B2B/ops. |
| Atomic CRM | Modern React/Supabase CRM; smaller product depth for multi-shop ops. |
| Ever Gauzy | Broad ERP/CRM/HRM platform; less focused CRM+orders+inbox benchmark. |

## Ranking rationale (Bloom fit)

| Rank | Product | Ops / orders | Multi-entity | Inbox / channels | UI richness |
|-----:|---------|:------------:|:------------:|:----------------:|:-----------:|
| 1 | ERPNext | ★★★★★ | ★★★★★ | ★★ | ★★★★ |
| 2 | Dolibarr | ★★★★★ | ★★★★ | ★★ | ★★★ |
| 3 | Chatwoot | ★ | ★★★ | ★★★★★ | ★★★★ |
| 4 | Twenty | ★★ | ★★★★ | ★★ | ★★★★★ |
| 5 | Krayin | ★★ | ★★★★ | ★★★ | ★★★★ |
| 6 | EspoCRM | ★★ | ★★★ | ★★★ | ★★★★ |

**Machine-readable twin:** `00-candidates.json`
