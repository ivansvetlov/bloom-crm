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
| `docs/index.html` | КП |
| `docs/demo.html` | Демо-кабинет |
| `docs/questions.html` | Опрос 25 вопросов |
| `docs/security.html` | Безопасность / 152-ФЗ |
| `docs/test-dynamic.html` | 12 недель внедрения |

## Домены
- **Боевой бренд:** `crmbloom.ru` (хаб + `/kp/{slug}/`)
- Песочница (legacy): `flowww.webtm.ru`
- Бэкап: GitHub Pages `ivansvetlov.github.io/flowwow-crm`
- В бренде/домене нет слова flowwow; slug КП может быть `flowwow` (контекст клиента)
