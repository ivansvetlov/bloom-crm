# Wiki Index — Bloom CRM knowledge

> Content catalog for agents. Last updated: 2026-08-01 | Total wiki pages: 18

## Entities
- [[bloom-crm]] — продукт, принципы, артефакты pre-sales
- [[flowwow]] — marketplace-канал, multi-account
- [[messengers]] — WA/TG/MAX inbox + VK alerts

## Concepts
- [[order-lifecycle]] — статусы, gates, priority
- [[mvp-scope]] — must/should/could
- [[modules-map]] — карта модулей
- [[unified-inbox]] — чаты UX + routing
- [[photo-gate]] — фото до доставки
- [[delivery]] — курьеры и tracking
- [[catalog-vitrina]] — витрина и остатки
- [[roles-rbac]] — роли и доступы
- [[florist-cabinet]] — кабинет флориста (демо)
- [[architecture-stack]] — стек и domains
- [[sitemap-ui]] — экраны full cabinet
- [[monthly-cost]] — opex диапазоны
- [[customer-questions]] — форма 25 вопросов
- [[open-questions]] — блокеры
- [[reliability-position]] — SLA / поддержка
- [[security-152]] — 152-ФЗ
- [[order-client-contact]] — связь с клиентом по заказу (отложено)

## Comparisons
- [[messengers-official-vs-grey]] — официально vs серое

## Raw sources
- `raw/tz/tz-customer-2026-08-01.md`
- `raw/questions/questions-customer.md`
- `raw/architecture/architecture-plan-full.md`
- `raw/architecture/course-content-map.md`
- `raw/research/courier-ux-everest-hybrid.md`

## RAG machine index
- `chunks/chunks.jsonl` — чанки для embedding/FTS
- `rag.sqlite` — SQLite FTS5
- `chunks/manifest.json` — метаданные сборки
- Query: `python knowledge/scripts/query_rag.py "запрос"`
