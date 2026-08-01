---
title: MVP scope
created: 2026-08-01
updated: 2026-08-01
type: concept
tags: [product, mvp, full, later]
sources: [raw/architecture/architecture-plan-full.md, raw/questions/questions-customer.md]
confidence: high
---

# MVP scope

## Must (закрыть смену)
- Auth + org + shops
- Orders hub + detail (FW + direct)
- Flowwow ingest + dual status + photo + reconcile
- Unified inbox (WA/TG/MAX per chosen path)
- Notifications + SLA 3 min
- Integration health
- Customers basic
- Roles bare
- Deploy РФ + backups

## Should (Full)
- Vitrina multi-shop (цены, остатки, hide)
- Analytics
- Delivery / couriers
- Finance register
- Full RBAC + shop scope option
- Reminders

## Could / Later
- Loyalty (отд. ТЗ)
- Bank acquiring + OFD — **не в v1** (только отметка «оплачено»)
- Courier PWA advanced
- Reviews scrape
- Peak AI, multi-stop routing

## Банк / ОФД (позиция)
В первой версии: **только ручная отметка оплаты**.  
Эквайринг и ОФД — отдельные этапы.

## Склад
Нужно понять: остатки **в Bloom** или интеграция со **своей складской** системой.  
См. вопрос 11 в [[customer-questions]].

## Связанное
- [[bloom-crm]]
- [[order-lifecycle]]
- [[monthly-cost]]
- [[open-questions]]
- [[modules-map]]
