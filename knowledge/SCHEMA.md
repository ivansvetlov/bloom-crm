# Wiki Schema — Bloom CRM / flowwow-crm

## Domain
Pre-sales, product and architecture knowledge for **Bloom CRM** (flowwow-crm):
cabinet for flower shops (Flowwow + messengers + direct sales + vitrina + delivery).

Audience: hosting agent, sales/dev agents, owner. Language: **Russian** for product text; technical IDs in English.

## Conventions
- File names: lowercase, hyphens, no spaces
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` (min 2 outbound per page)
- Bump `updated` on every edit
- New pages → `index.md` + `log.md`
- Provenance: `^[raw/...]` when synthesizing 3+ sources

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: []
sources: []
confidence: high | medium | low
---
```

## Tag taxonomy
- product: product, module, mvp, full, later
- domain: florist, flowwow, messenger, delivery, catalog, loyalty, payment
- arch: architecture, api, data-model, integration, security, hosting
- ops: order-lifecycle, roles, sla, peak, photo-gate
- sales: pre-sales, pricing, questions, demo, kp
- meta: decision, risk, open-question

## Page thresholds
- Create entity/concept when central to TZ or architecture OR appears in 2+ sources
- Don't create pages for one-off mentions
- Split pages over ~200 lines

## RAG layer
- Compiled retrieval index: `chunks/chunks.jsonl` + `rag.sqlite` (FTS5)
- Rebuild: `python knowledge/scripts/build_rag.py`
- Query: `python knowledge/scripts/query_rag.py "запрос"`
- Manifest: `chunks/manifest.json` (source list, chunk counts, version)

## Update policy
Newer project decisions (commits, owner answers) supersede older drafts.
Mark contradictions in frontmatter; don't silently overwrite.
