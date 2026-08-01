---
title: Flowwow
created: 2026-08-01
updated: 2026-08-01
type: entity
tags: [domain, flowwow, integration]
sources: [raw/tz/tz-customer-2026-08-01.md, raw/questions/questions-customer.md]
confidence: high
---

# Flowwow

Маркетплейс цветов/подарков. Для Bloom — **входящий канал** оплаченных заказов и (по возможности API) исходящий sync статусов и фото.

## Модель аккаунтов (зафиксировано с заказчиком)
- Сайт Flowwow **общий** для сети
- У **каждого магазина свой аккаунт** Flowwow
- В Bloom — один кабинет на все аккаунты (отдельные ключи API)

## Что нужно от API (open questions)
- Webhook vs poll
- Write: статусы, отмена, фото, цены, остатки, hide/show
- Multi-account auth

## Связанное
- [[bloom-crm]]
- [[order-lifecycle]]
- [[catalog-vitrina]]
- [[mvp-scope]]
- [[open-questions]]
