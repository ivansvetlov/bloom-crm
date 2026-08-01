---
title: Жизненный цикл заказа
created: 2026-08-01
updated: 2026-08-01
type: concept
tags: [ops, order-lifecycle, product]
sources: [raw/tz/tz-customer-2026-08-01.md, raw/architecture/architecture-plan-full.md]
confidence: high
---

# Жизненный цикл заказа

## UI / demo (5 шагов)
`new → accepted → assembled → delivering → done`  
(в демо: «Доставлен» вместо «Выполнен» на финале UI)

## Full operational set
```
new → accepted → in_assembly → assembled → photo_ready
  → awaiting_courier | ready_pickup
  → out_for_delivery → delivered → completed
```
Ветки: `rejected`, `cancelled_client`, `failed_delivery`, `returned`.

## Gates
- **Photo gate:** перед «В доставку» — фото букета (before)
- **Direct orders** никогда не уходят во Flowwow
- **Source of truth статусов:** Bloom; FW — consumer + source of new paid orders

## Priority sort списка
1. `new` + overdue SLA (3 мин)
2. ASAP / slot within 2h
3. delivery_date today
4. rest

## Связанное
- [[bloom-crm]]
- [[flowwow]]
- [[photo-gate]]
- [[mvp-scope]]
- [[delivery]]
