# CRM Benchmark Research — RUNLOG

**Project:** Bloom CRM (flower network ops cabinet)  
**Scope:** Open-source CRM research → structure MVPs → Bloom-oriented mega synthesis  
**Repo path (canonical):** `C:\Workspace\projects\flowwow-crm`  
**Worktree path:** workspace `docs/research/crm-benchmark/`  
**Phase:** 1 — Scaffold (this file). No CRM analysis yet.

---

## Mission

Benchmark 5–7 open-source (or source-available) CRMs relevant to Bloom’s domain: marketplace + direct orders, multi-shop, messenger inbox, dual status models, and analytics. Produce per-CRM analysis + clickable structure MVPs, then a Bloom-focused mega synthesis and interactive mega MVP.

---

## Pipeline Plan

### Phase 0 — Scaffold (current)

| Step | Owner | Output | Status |
|------|--------|--------|--------|
| Folder tree `reports/`, `mvp/`, `mega/` | Orchestrator | dirs | done |
| `RUNLOG.md` (this plan) | Orchestrator | this file | done |
| `ORCHESTRATOR.md` (rules + naming) | Orchestrator | coordination doc | done |

### Phase 1 — Discovery (Searcher)

| Step | Owner | Output | Status |
|------|--------|--------|--------|
| Find **5–7 CRMs** fit for Bloom ops cabinet (orders, multi-shop, inbox, statuses, analytics) | Searcher | shortlist in RUNLOG + optional `reports/_shortlist.md` | pending |
| Capture per candidate: name, license, stack, URL, why relevant | Searcher | rows below | pending |

**Selection criteria (Searcher must apply):**

- Open-source or source-available with usable docs/demo
- Strong **order / deal / pipeline** model (not pure marketing CRM only)
- Multi-entity or multi-branch affinity (shops / orgs / teams)
- Messaging, activity, or inbox-like surfaces preferred
- Status / workflow configurability preferred
- Analytics / reporting surfaces preferred
- Preference: self-hostable, modern UI, active maintenance

**Shortlist slots (fill when Searcher returns):**

| # | id (slug) | CRM name | License | Stack | Primary URL | Bloom fit notes |
|---|-----------|----------|---------|-------|-------------|-----------------|
| 1 | _TBD_ | | | | | |
| 2 | _TBD_ | | | | | |
| 3 | _TBD_ | | | | | |
| 4 | _TBD_ | | | | | |
| 5 | _TBD_ | | | | | |
| 6 | _TBD_ | | | | | |
| 7 | _TBD_ | | | | | |

`id` = lowercase kebab-case slug used in all paths (e.g. `espocrm`, `twenty`, `erpnext`).

### Phase 2 — Per-CRM deep dive (Analyzer × N)

For **each** shortlisted CRM (`{id}`):

| Step | Owner | Output | Status |
|------|--------|--------|--------|
| Structure + domain analysis | Analyzer | `reports/{id}-analysis.md` | pending |
| Clickable structure / web MVP | Analyzer (or MVP builder) | `mvp/{id}/index.html` | pending |
| Log completion line in this RUNLOG | Orchestrator | update | pending |

**Each analysis should cover (minimum):**

1. Product positioning and target user  
2. Information architecture (nav, modules, main objects)  
3. Order / deal / pipeline model  
4. Multi-shop / multi-org / multi-branch patterns  
5. Inbox / messenger / communication surfaces  
6. Status systems (single vs dual / parallel statuses if any)  
7. Analytics & reporting  
8. Extensibility, API, self-host notes  
9. UX patterns Bloom should steal / avoid  
10. Mapping table: CRM concept → Bloom concept  

**Each `mvp/{id}/index.html` should be:**

- Standalone HTML (inline CSS/JS OK)  
- Clickable IA: shell, nav, key screens as panels/routes  
- No backend required  
- Clearly labeled as structure MVP of `{id}`, not Bloom branding  

### Phase 3 — Synthesis (Synthesizer)

| Step | Owner | Output | Status |
|------|--------|--------|--------|
| Cross-CRM mega report for Bloom | Synthesizer | `mega/SYNTHESIS.md` | **done** |
| Gaps vs Bloom needs (marketplace + direct, dual status, multi-shop, messenger, analytics) | Synthesizer | section in SYNTHESIS | **done** |
| Recommended IA + status model + MVP screen list for Bloom | Synthesizer | section in SYNTHESIS | **done** |

### Phase 4 — Final mega interactive MVP

| Step | Owner | Output | Status |
|------|--------|--------|--------|
| Bloom-oriented mega CRM structure MVP | Mega builder | `mega/index.html` | pending |
| Wire key flows: shops, orders (marketplace vs direct), dual status, inbox, analytics | Mega builder | interactive shell | pending |
| Orchestrator acceptance check against ORCHESTRATOR.md | Orchestrator | RUNLOG sign-off | pending |

---

## Role handoff order

```
Orchestrator (scaffold)
    → Searcher (5–7 CRMs)
        → Analyzer per CRM (report + mvp/{id}/)
            → Synthesizer (mega/SYNTHESIS.md)
                → Mega builder (mega/index.html)
                    → Orchestrator (final QA + RUNLOG close)
```

Do **not** start Synthesizer or Mega until all selected CRM analyses + structure MVPs are present (or Orchestrator explicitly waives a slot).

---

## Output inventory (target)

```
docs/research/crm-benchmark/
├── ORCHESTRATOR.md          # coordination rules + naming
├── RUNLOG.md                # this plan + progress
├── reports/
│   └── {id}-analysis.md     # one per CRM
├── mvp/
│   └── {id}/
│       └── index.html       # structure MVP per CRM
└── mega/
    ├── SYNTHESIS.md         # Bloom-oriented mega report
    └── index.html           # final mega interactive MVP
```

---

## Progress log

| When (UTC) | Event |
|------------|--------|
| 2026-08-01 | Phase 0 scaffold: dirs + RUNLOG + ORCHESTRATOR created. Awaiting Searcher shortlist. |
| 2026-08-01 | Analyzer: `reports/espocrm-analysis.md` written (id=`espocrm`). Fit **6.5/10**. MVP `mvp/espocrm/index.html` still pending. |
| 2026-08-01 | Analyzer: `reports/chatwoot-analysis.md` written (id=`chatwoot`). Inbox-module fit **8/10** (full CRM ~4/10). MVP `mvp/chatwoot/index.html` still pending. |
| 2026-08-01 | Analyzer: `reports/twenty-analysis.md` written (id=`twenty`). Bloom fit **6.0/10** (UX benchmark ~9.5). MVP `mvp/twenty/index.html` still pending. |
| 2026-08-01 | **Synthesizer:** `mega/SYNTHESIS.md` written. Verdict: greenfield Bloom (no fork); dual status; Chatwoot+ERPNext+Twenty+Espo primary pattern sources. Gate D ready for Mega builder. |

---

## Done definition (research track)

- [ ] 5–7 CRMs shortlisted with stable `{id}` slugs  
- [ ] Every CRM has `reports/{id}-analysis.md`  
- [ ] Every CRM has `mvp/{id}/index.html` (openable offline)  
- [x] `mega/SYNTHESIS.md` maps findings → Bloom  
- [ ] `mega/index.html` is a clickable Bloom-oriented mega structure MVP  
- [ ] This RUNLOG updated with shortlist table and completion ticks  
