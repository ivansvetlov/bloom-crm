# EspoCRM structure MVP · web shell

**Path:** `docs/research/crm-benchmark/mvp/espocrm/`  
**Entry:** [`index.html`](./index.html)  
**Program:** Bloom CRM open-source CRM research  
**CRM id:** `espocrm`

## What this is

Self-contained **clickable structure prototype** of EspoCRM’s entity SPA — not a Bloom product skin and not a full EspoCRM clone.

Opens **offline** in any modern browser (no backend, no build).

Badge in chrome: **MVP · EspoCRM structure → web**

## Surfaces

| Surface | What you can click |
|---------|-------------------|
| **Nav** | Главная, Аккаунты, Контакты, Возможности, Обращения, Лента |
| **List** | Entity tables with filter; open row → detail |
| **Detail** | Overview fields, related records, action buttons (mock) |
| **Stream** | Activity feed on every detail + global Stream; post mock note |
| **Kanban** | Cases only: New / Assigned / In Progress / Closed; advance status |

### Entities (EspoCRM mental model)

- **Account** — organization / shop / partner  
- **Contact** — person linked to Account  
- **Opportunity** — sales pipeline stages  
- **Case** — ticket / service case (status workflow + Kanban)

## Bloom note · Cases → flower order statuses

EspoCRM **Case** statuses map as a research mental model for flower-network order ops:

| Case status | Bloom-ish order stage |
|-------------|------------------------|
| **New** | Новый / принят |
| **Assigned** | Назначен флористу / точке |
| **In Progress** | Сборка / в доставке |
| **Closed** | Доставлен / отменён / решён |

Stream ≈ order timeline + notes + status changes + email-like events.

## How to open

```text
# file URL or any static server
C:\Workspace\projects\flowwow-crm\docs\research\crm-benchmark\mvp\espocrm\index.html
```

Or:

```bash
# from repo root
npx --yes serve docs/research/crm-benchmark/mvp/espocrm
```

## Technical notes

- Single HTML file: inline CSS + JS  
- Russian UI labels  
- Placeholder data only; create/edit/email are toasts  
- Kanban “→ статус” advances Case along the four statuses and appends a Stream event  

## Related research paths

- Orchestrator: `docs/research/crm-benchmark/ORCHESTRATOR.md`  
- Run log: `docs/research/crm-benchmark/RUNLOG.md`  
- Analysis (when present): `docs/research/crm-benchmark/reports/espocrm-analysis.md`  
- Candidates: `docs/research/crm-benchmark/00-candidates.md`
