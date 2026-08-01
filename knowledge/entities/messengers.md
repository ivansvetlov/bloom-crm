---
title: Мессенджеры (WA / TG / MAX / VK)
created: 2026-08-01
updated: 2026-08-01
type: entity
tags: [domain, messenger, integration, risk]
sources: [raw/tz/tz-customer-2026-08-01.md, raw/questions/questions-customer.md]
confidence: high
---

# Мессенджеры

## В кабинете (unified inbox)
По ТЗ: **WhatsApp, Telegram, MAX** — один раздел «Чаты», ответ от имени аккаунтов, медиа, заказ из чата в 1 клик, хранение новой переписки.

### Риски
| Канал | Официально | Серое (личные) |
|-------|------------|----------------|
| WhatsApp | Business API, платно | Дешёвая платформа, риск бана |
| Telegram | Bot API | Userbot / личные — бан |
| MAX | Business-style API (уточнять) | — |

В ТЗ: «платформу прислали» (дешёвый вариант) — **вопрос 5** формы: название и способ подключения.

## Уведомления staff
ТЗ п.5: о новых заказах — **в Telegram или ВК**; SLA 3 мин → повторное напоминание.

**Решение pre-sales:** закладываем **TG + VK** без выбора «или».  
VK Community Messages / Callback — без per-message тарифа VK; opex резерв **0–2 тыс ₽/мес**.

## Контакты исполнителя (форма вопросов)
В UI только подписи TG/WA/MAX (без raw URL). Профили владельца прошиты в `questions.html`.

## Связанное
- [[bloom-crm]]
- [[unified-inbox]]
- [[monthly-cost]]
- [[open-questions]]
- [[mvp-scope]]
