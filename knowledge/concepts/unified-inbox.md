---
title: Unified Inbox
created: 2026-08-01
updated: 2026-08-01
type: concept
tags: [product, messenger, ops]
sources: [raw/tz/tz-customer-2026-08-01.md, raw/architecture/architecture-plan-full.md]
confidence: high
---

# Unified Inbox

Раздел «Чаты»: все диалоги WA/TG/MAX в одном окне.

## UX
- Thread list + badges канала, unread, shop chip
- Composer: text/photo/file
- **Создать заказ** / **Привязать к заказу**
- Assignee sticky

## Routing (Full)
Identity match → shop by number → sticky assignee → round-robin → B2B keywords → SLA chat

## Create order from chat
Prefill client/channel/shop → free-text or catalog → `source=direct_{channel}`

## Связанное
- [[messengers]]
- [[bloom-crm]]
- [[order-lifecycle]]
- [[mvp-scope]]
