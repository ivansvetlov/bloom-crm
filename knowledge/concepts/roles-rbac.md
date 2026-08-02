---
title: Роли и доступы
created: 2026-08-01
updated: 2026-08-01
type: concept
tags: [ops, product]
sources: [raw/tz/tz-customer-2026-08-01.md, raw/architecture/architecture-plan-full.md]
confidence: high
---

# Роли и доступы

## ТЗ
- Вход login/password, без SMS
- Multi-user, без лимита
- «Менеджеры видят все магазины» — дефолт; опция shop-scope

## Роли (Full)
| Роль | Суть |
|------|------|
| Владелец / директор | всё + интеграции + роли |
| Старший менеджер | все точки, цены, отказ |
| Менеджер | заказы + чаты (scope shop) |
| Флорист | сборка + фото |
| Курьер | свои доставки |
| Бухгалтер | финансы read/export |

## UI mock
Неделя 04 в `docs/test-dynamic.html` — команда, матрица прав, журнал действий.

## Демо-вход (auth gate)
`docs/auth.js` — гейт входа с выбором роли карточками:
- **Кабинет менеджера** — `admin/admin` (Анна К., владелец сети, все магазины)
- **Кабинет флориста** — `florist/florist` (Светлана П., свой магазин «Ленина 92»)
- + сворачиваемая форма ручного входа по логину.
Роль определяется через `BloomAuth.profile().role` / `.shop` (см. [[florist-cabinet]]).

## Связанное
- [[bloom-crm]]
- [[mvp-scope]]
- [[customer-questions]]
- [[reliability-position]]
- [[florist-cabinet]]
