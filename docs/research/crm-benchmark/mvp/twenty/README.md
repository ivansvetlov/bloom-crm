# Twenty — Structure MVP (web)

**Program:** Bloom CRM open-source CRM research  
**CRM id:** `twenty`  
**Artifact:** Clickable IA / UX shell inspired by [Twenty](https://github.com/twentyhq/twenty) (not a product clone)  
**Entry:** [`index.html`](./index.html) — open offline in any modern browser  

Badge in UI: **MVP · Twenty structure → web**

---

## Purpose

Structural prototype of Twenty’s information architecture for the Bloom benchmark:

| Twenty surface | In this MVP |
|----------------|-------------|
| Workspace left nav | People, Companies, Opportunities, Tasks, Notes, Settings |
| Record tables | Sortable-looking lists + text filter |
| Opportunity pipeline | Table + **Kanban** by stage |
| Record detail | Right **side panel** with fields, relations, activity stubs |
| Global search | **Command palette** (`Ctrl/⌘ K`) — filter nav + records |
| Appearance | Light / dark theme (persisted in `localStorage`) |

Demo data is flower-network flavoured (Bloom / shops / logistics) only to make research walkthroughs concrete. This is **Twenty structure**, not Bloom product UI.

---

## How to open

```text
docs/research/crm-benchmark/mvp/twenty/index.html
```

- Double-click or serve the folder as static files.  
- **No backend**, no build step, no CDN required (system fonts).  
- Works fully offline after first open.

---

## Interactions

1. **Nav** — switch modules in the left sidebar.  
2. **Filter** — toolbar search narrows the current table / kanban.  
3. **Row / card click** — opens detail panel; related records are clickable.  
4. **Opportunities** — toggle **Таблица / Канбан**.  
5. **Command palette** — top search chip or `Ctrl+K` / `⌘K`; `↑↓` + Enter.  
6. **Theme** — sidebar footer toggle.  
7. **Esc** — close palette, then close panel.

---

## Object model (demo)

```text
Company ──< Person
    │           │
    └──── Opportunity ──── Task
              │
            Note (also links Person / Company)
```

**Opportunity stages:** Новые → Квалификация → Предложение → Переговоры → Выиграно / Проиграно  

Aligned with Twenty’s core CRM objects (people, companies, opportunities) plus tasks/notes as first-class related surfaces.

---

## Files

| File | Role |
|------|------|
| `index.html` | Self-contained HTML + CSS + JS MVP |
| `README.md` | This note |

---

## Out of scope (intentionally)

- Auth, multi-workspace switcher backend, real GraphQL API  
- Custom object builder / field editor  
- Workflows, permissions matrix, email sync  
- Drag-and-drop kanban persistence  
- Production Twenty branding / assets  

Use the analysis report (`reports/twenty-analysis.md` when present) for steal/avoid mapping to Bloom.

---

## Acceptance checklist (Orchestrator)

- [x] Path: `mvp/twenty/index.html`  
- [x] Offline, self-contained  
- [x] Clickable nav between main modules  
- [x] Product name + `{id}` context (`twenty`) in title/chrome  
- [x] Labels reflect Twenty-like structure  
- [x] Badge: MVP · Twenty structure → web  
