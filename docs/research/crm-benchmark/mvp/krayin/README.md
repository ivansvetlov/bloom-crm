# Krayin CRM — Structure MVP (web shell)

**Program:** Bloom CRM open-source benchmark  
**id:** `krayin`  
**Source product:** [Krayin Laravel CRM](https://github.com/krayin/laravel-crm) (MIT, Webkul)  
**Stack of source:** Laravel (PHP) · Vue.js · MySQL  
**This artifact:** offline clickable **information-architecture shell**, not a product clone and not Bloom branding.

## Open

Open in any browser (no server required):

```text
docs/research/crm-benchmark/mvp/krayin/index.html
```

Or from repo root:

```powershell
start docs\research\crm-benchmark\mvp\krayin\index.html
```

## Badge

UI shows: **`MVP · Krayin structure → web`**

## Modules (clickable)

| Route | Screen | Notes |
|-------|--------|--------|
| `#dashboard` | Dashboard | KPI cards, stage bars, top leads, recent quotes |
| `#leads` | Leads pipeline | Kanban (default) + list toggle; drag-and-drop stages |
| `#lead/{id}` | Lead detail | Fields, person/org, timeline, linked quotes |
| `#quotes` | Quote list | Status filter: all / draft / sent / accepted |
| `#mail` | Mail stub | Folders (inbox/draft/outbox/sent/trash), preview, lead link |
| `#settings` | Settings stubs | Users, Roles, Groups, Pipelines, Sources, Types, Attributes, Email, Warehouses, Webhooks |

## Krayin structure reflected

- **Sales core:** Leads (pipeline stages) → Quotes → Mail  
- **Default pipeline stages:** New → Follow Up → Prospect → Negotiation → Won / Lost  
- **Objects on cards:** title, organization, value, source, owner, expected close  
- **Lead detail:** person, org, type, source, activities timeline, linked quotes  
- **Settings IA:** users/roles/groups, pipeline config, sources/types, attributes, email  

Russian UI labels are intentional for Bloom research readability; module names stay close to Krayin English IA.

## Bloom mapping (quick)

| Krayin concept | Bloom angle |
|----------------|-------------|
| Lead + pipeline stages | Order/deal intake; dual status still needs design (fulfillment vs payment not native) |
| Quote | Commercial offer before / alongside order |
| Mail folders + lead link | Messenger inbox pattern (weaker than Chatwoot; useful “entity-linked thread” idea) |
| Groups / multi-tenant path | Multi-shop isolation research |
| Attributes / pipelines | Configurable fields and shop-specific workflows |

## Constraints

- Self-contained single `index.html` (inline CSS/JS)  
- Demo data only; create/edit actions are toasts/stubs  
- No backend, no auth, no persistence  
- Structure prototype of **Krayin IA**, not a Bloom skin  

## Related paths

- Analysis report (when present): `docs/research/crm-benchmark/reports/krayin-analysis.md`  
- Orchestrator rules: `docs/research/crm-benchmark/ORCHESTRATOR.md`  
- Candidates: `docs/research/crm-benchmark/00-candidates.md`
