---
title: Bloom CRM
created: 2026-08-01
updated: 2026-08-01
type: entity
tags: [product, florist, pre-sales]
sources: [raw/tz/tz-customer-2026-08-01.md, raw/architecture/architecture-plan-full.md]
confidence: high
---

# Bloom CRM

Операционный кабинет сети цветочных салонов. **Bloom = source of truth** для производства, доставки, прямых продаж и переписок; **Flowwow = marketplace-канал** (оплаченные заказы + dual sync статусов/фото).

**Одна фраза:** менеджер, флорист и курьер закрывают день в одном окне: Flowwow + WhatsApp/Telegram/MAX + свои заказы, витрина и цифры.

## Связанное
- [[flowwow]] — канал заказов
- [[order-lifecycle]] — статусы
- [[unified-inbox]] — чаты
- [[mvp-scope]] — что в первой поставке
- [[monthly-cost]] — opex

## Продуктовые принципы
1. Визуал = продукт (фото до/после, photo-gate)
2. Слот и адрес важнее «красивостей»
3. Два контура: `flowwow` vs `direct/*`
4. Единый inbox — клиент пишет «как всегда»
5. Peak mode (8 Марта / НГ)
6. Надёжность как фича (health + reconcile)

## Публичные артефакты
| Файл | Назначение |
|------|------------|
| `docs/index.html` | Хаб КП |
| `docs/kp/demo/` | Демо-КП (точка входа для заказчика) |
| `docs/kp/{slug}/` | КП под клиента |

## Домены и имя
- **Продукт:** Bloom CRM
- **Боевой домен:** `crmbloom.ru` (хаб + `/kp/{slug}/`)
- **Репозиторий:** `bloom-crm` (старое имя flowwow-crm — не использовать)
- **Flowwow** в текстах = внешний маркетплейс-канал, **не** бренд продукта
