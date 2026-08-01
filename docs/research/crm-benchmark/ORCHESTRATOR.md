# CRM Benchmark — Orchestrator Rules

**Program:** Bloom CRM open-source CRM research  
**Root:** `docs/research/crm-benchmark/`  
**Authority:** This file defines coordination, naming, and acceptance for all agents (Searcher, Analyzer, Synthesizer, Mega builder).  
**Progress:** Always append status to `RUNLOG.md`. Do not invent alternate trees.

---

## Bloom context (do not re-scope)

Bloom CRM is a **flower network ops cabinet**, not a generic sales CRM:

| Bloom surface | Research focus when benchmarking |
|---------------|----------------------------------|
| Marketplace + direct orders | Dual intake channels; order vs deal models |
| Multi-shop | Org/branch/store isolation and shared ops |
| Messenger inbox | Threads, assignment, order-linked chat |
| Dual status | Parallel status dimensions (e.g. fulfillment vs payment / shop vs network) |
| Analytics | Ops KPIs, shop/network rollups |

Agents must map findings **to Bloom**, not only describe third-party products.

---

## Roles

| Role | Responsibility | Primary outputs |
|------|----------------|-----------------|
| **Orchestrator** | Scaffold, gate phases, naming enforcement, RUNLOG, final QA | `ORCHESTRATOR.md`, `RUNLOG.md` |
| **Searcher** | Discover 5–7 CRMs; assign stable `{id}` slugs; fill shortlist | `RUNLOG.md` shortlist table; optional `reports/_shortlist.md` |
| **Analyzer** | Per-CRM deep dive + structure MVP | `reports/{id}-analysis.md`, `mvp/{id}/index.html` |
| **Synthesizer** | Cross-CRM Bloom-oriented mega report | `mega/SYNTHESIS.md` |
| **Mega builder** | Final interactive Bloom structure MVP | `mega/index.html` |

One Analyzer pass per `{id}`. Synthesizer and Mega builder run **after** the accepted shortlist is fully analyzed (unless Orchestrator waives a slot in RUNLOG).

---

## Output file naming (strict)

All paths are under `docs/research/crm-benchmark/`.

| Artifact | Path | Rules |
|----------|------|--------|
| Analysis report | `reports/{id}-analysis.md` | One file per CRM. `{id}` = kebab-case slug only (`a-z0-9-`). |
| Structure MVP | `mvp/{id}/index.html` | Directory per CRM; entry always `index.html`. Extra assets only under `mvp/{id}/`. |
| Mega synthesis | `mega/SYNTHESIS.md` | Single file. Uppercase name fixed. |
| Mega interactive MVP | `mega/index.html` | Single entry; assets only under `mega/`. |
| Run log | `RUNLOG.md` | Append-only progress + shortlist + checkboxes. |
| Orchestrator rules | `ORCHESTRATOR.md` | This file; change only with Orchestrator approval. |

### `{id}` conventions

- Lowercase kebab-case: `twenty`, `espocrm`, `erpnext`, `suite-crm`, `odoo-crm`
- No spaces, no underscores, no version numbers in the slug
- Same `{id}` in shortlist, report filename, and `mvp/{id}/`
- Do **not** rename an `{id}` after first report/MVP is written without Orchestrator + RUNLOG note

### Forbidden / discouraged

- Ad-hoc folders (`analysis/`, `html/`, `outputs/`, etc.)
- Names like `report.md`, `crm1.md`, `mvp.html` at tree root
- Putting Bloom mega UI under `mvp/` (mega is only under `mega/`)
- Mixing multiple CRMs into one `mvp/` folder

### Target tree

```
docs/research/crm-benchmark/
├── ORCHESTRATOR.md
├── RUNLOG.md
├── reports/
│   ├── _shortlist.md          # optional Searcher artifact
│   └── {id}-analysis.md
├── mvp/
│   └── {id}/
│       └── index.html
└── mega/
    ├── SYNTHESIS.md
    └── index.html
```

---

## Phase gates

### Gate A — After Searcher

- Shortlist has **5–7** CRMs  
- Each row has: `{id}`, name, license, stack, primary URL, Bloom fit notes  
- Orchestrator (or Searcher under Orchestrator rules) updates `RUNLOG.md` shortlist table  

### Gate B — After each Analyzer CRM

- `reports/{id}-analysis.md` exists and includes Bloom mapping section  
- `mvp/{id}/index.html` opens offline (no required backend)  
- RUNLOG progress log line for that `{id}`  

### Gate C — Before Synthesizer

- All shortlisted IDs have report + MVP **or** explicit waiver in RUNLOG  

### Gate D — Before Mega builder

- `mega/SYNTHESIS.md` present with recommended Bloom IA / status model / screen list  

### Gate E — Done

- `mega/index.html` clickable; RUNLOG done-definition checkboxes complete  

---

## Content standards

### `reports/{id}-analysis.md`

Required sections (headings may vary slightly, content must exist):

1. Meta (name, license, stack, URLs, version/date of review)  
2. Positioning  
3. Information architecture  
4. Core objects (orders/deals/contacts/orgs)  
5. Multi-shop / multi-tenant patterns  
6. Communication / inbox  
7. Status & workflow model  
8. Analytics  
9. Extensibility / API / self-host  
10. Steal / avoid for Bloom  
11. Mapping: CRM concept → Bloom concept  

### `mvp/{id}/index.html`

- Self-contained structure prototype of **that CRM’s IA**, not Bloom skin  
- Clickable navigation between main modules  
- Placeholder content OK; labels must reflect analyzed structure  
- Title/header must include product name + `{id}`  

### `mega/SYNTHESIS.md`

- Comparison matrix across shortlist  
- Pattern extraction (IA, status, multi-shop, inbox, analytics)  
- Explicit Bloom recommendations and gaps  
- Prioritized screen list for `mega/index.html`  

### `mega/index.html`

- Bloom-oriented ops cabinet structure MVP  
- Must surface: multi-shop, marketplace vs direct orders, dual status, messenger inbox, analytics  
- Standalone HTML preferred; no production backend  

---

## Coordination protocol

1. **Read first:** `ORCHESTRATOR.md` + latest `RUNLOG.md` before writing artifacts.  
2. **Claim work:** Note in RUNLOG which `{id}` or phase you take.  
3. **Write only named outputs:** Use the table above; no parallel naming schemes.  
4. **Update RUNLOG** on start and on finish of each unit of work.  
5. **No phase skip** without Orchestrator waiver line in RUNLOG.  
6. **Conflicts:** Prefer Orchestrator rules over agent improvisation.  
7. **Citations:** Analysis should note official docs/demo URLs used.  
8. **Language:** English for structure keys/ids; RU/EN prose OK if consistent within a file—prefer English for shared research artifacts unless product copy is RU.  

---

## Agent prompts (copy pack)

### Searcher

> Find 5–7 open-source/source-available CRMs suitable for Bloom (orders, multi-shop, inbox, statuses, analytics). Assign kebab-case `{id}`. Update `RUNLOG.md` shortlist table. Optional: `reports/_shortlist.md`. Do not write per-CRM analyses.

### Analyzer (per `{id}`)

> For CRM `{id}`, write `reports/{id}-analysis.md` per ORCHESTRATOR sections, and `mvp/{id}/index.html` clickable structure MVP. Map to Bloom. Update RUNLOG when done.

### Synthesizer

> Read all `reports/*-analysis.md` and MVPs. Write `mega/SYNTHESIS.md` for Bloom: matrix, patterns, dual-status recommendation, IA, prioritized mega screens.

### Mega builder

> Implement `mega/index.html` from `mega/SYNTHESIS.md`: multi-shop, marketplace + direct orders, dual status, messenger inbox, analytics. Standalone interactive structure MVP.

---

## Acceptance checklist (Orchestrator final QA)

- [ ] Naming matches `reports/{id}-analysis.md` and `mvp/{id}/index.html` for every shortlist id  
- [ ] No orphan files outside the target tree  
- [ ] `mega/SYNTHESIS.md` references shortlist CRMs by `{id}`  
- [ ] `mega/index.html` reflects Bloom surfaces listed above  
- [ ] `RUNLOG.md` shortlist + progress + done definition complete  

---

## Revision history

| Date | Change |
|------|--------|
| 2026-08-01 | Initial Orchestrator rules + naming for phase 1 scaffold |
