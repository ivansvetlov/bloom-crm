---
source_url: local://knowledge/raw/architecture/architecture-plan-full.md
ingested: 2026-08-01
sha256: d97571c18c6d2e12ecf3defbae73e01551d4c985ee9ef54f9de7c8e088dd1997
---

# Bloom CRM Full — Product & Architecture Plan

> Источник: plan-subagent 2026-08-01 · опора: `tz.md`, `questions.md`, `demo.html`, `index.html`, `test-dynamic.html`, `research/courier-ux-everest-hybrid.md`

## 1. Product vision

**Bloom CRM** — операционный кабинет сети цветочных салонов, где **Bloom = source of truth** для производства, доставки, прямых продаж и переписок, а **Flowwow = marketplace-канал** (входящие оплаченные заказы + двусторонний sync статусов/фото, где API это позволяет).

**Одна фраза:**  
*«Менеджер, флорист и курьер закрывают день в одном окне: Flowwow + WhatsApp/Telegram/MAX + свои заказы, витрина и цифры — без Excel и «где этот букет?»».*

### Job-to-be-done

| Роль | JTBD |
|------|------|
| Владелец | Видеть выручку FW vs прямые, точки, пики (8 Марта), здоровье интеграций |
| Менеджер | Принять заказ за секунды, ответить в чате, создать прямой заказ, не потерять срочное |
| Флорист | Очередь сборки, фото «как на витрине», состав/открытка/время |
| Курьер | Взять → фото до выезда → еду → вручил, ETA к слоту события |
| Бухгалтер | Оплаты, отказы, возвраты, сверка каналов (позже — ОФД/банк) |

### Принципы продукта

1. **Визуал = продукт** — фото до/после, замена только с новым фото.
2. **Слот и адрес раньше «красивостей»** — ASAP vs окно (18:00 «к празднику»).
3. **Два контура заказов** — `channel=flowwow` (sync out) и `channel=direct/*` (только Bloom).
4. **Единый inbox** — клиент пишет «как всегда», менеджер отвечает из кабинета.
5. **Пиковый режим** — 8 Марта / НГ: упрощённый UI, только P0-кнопки, SLA приёма 3 мин.
6. **Надёжность как фича** — health Flowwow/мессенджеров + reconcile.

---

## 2. Personas & roles

| Persona | Боль | Успех |
|---------|------|--------|
| Ольга · владелец | Не видит, где теряют деньги и заказы | Дашборд дня/месяца, FW vs direct, health |
| Анна · менеджер | Переключение вкладок, пропуск новых | Inbox + канбан, accept за 1 клик |
| Дарья · флорист | Неясная очередь, нет фото-чеклиста | Board «Собрать», photo gate |
| Игорь · курьер | Непонятный адрес/слот | Mobile shift, verb-кнопки |
| Марина · бухгалтер | «Кто оплатил» в чатах | Payments ledger, export |

**Auth:** login/password, multi-user, no SMS. Full: reset, session TTL, audit, optional 2FA later. **152-ФЗ:** серверы РФ, consent, encryption at rest for PII.

---

## 3. Module map

| Модуль | Зачем | Priority |
|--------|-------|----------|
| Auth & Org | Вход, сеть, магазины | **must** |
| Orders hub | Канбан/список FW + direct | **must** |
| Order card | Состав, фото, слот, адрес, открытка, timeline | **must** |
| Flowwow sync | Ingest + dual status + photo + reconcile | **must** |
| Direct sales | Ручные заказы без push в FW | **must** |
| Unified Inbox | WA + TG + MAX | **must** |
| Notifications | Новый заказ, SLA 3 мин | **must** |
| Integrations health | Отвал ключа → алерт | **must** |
| Customers | Карточка, LTV, merge | **must** (базово) |
| Catalog / Vitrina | Цены, остатки, hide multi-shop | **should** |
| Inventory | Остатки, списание | **should** |
| Analytics | Выручка, AOV, топ, FW vs direct | **should** |
| Delivery / Couriers | Назначение, ETA, photo-before-leave | **should** |
| Finance | Оплаты, возвраты | **should** |
| Roles & staff | RBAC | **must/should** |
| Reminders | Поздравления, follow-up | **should** |
| Loyalty | Баллы (отд. ТЗ) | **could** |
| Bank/ОФД | Эквайринг, чеки | **could** |
| Reviews FW | Рейтинги/отзывы | **could** |
| Courier app | Mobile PWA | **could** |
| Peak mode | UI 8 Марта | **could** |
| Multi-stop routing | Маршрут N адресов | **later** |
| WMS deep | Закупки, партии | **later** |

---

## 4. Domain model (sketch)

```
Organization → Shop[] → StaffAssignment, CatalogOverride, FlowwowAccount?, MessengerIdentity[]
User (staff) → Role, permissions
Customer ↔ ChannelIdentity[] ↔ Order[] / Conversation[]
Order: source, external_ids, shop, status, payer, recipient, delivery, items, photos, timeline
Product/Offer → shop_state (price, stock, visible)
Conversation → Message[] (WA|TG|MAX)
IntegrationConnection + Outbox/Inbox + AuditLog
```

**Инварианты:**
- Прямой заказ никогда не уходит во Flowwow.
- FW-заказ: Bloom → outbox → FW; FW cancel → notify.
- Photo gate: assembled → out_for_delivery требует before-photo.
- Source of truth статусов: Bloom.

---

## 5. Order lifecycle

`new → accepted → in_assembly → assembled → photo_ready → awaiting_courier|ready_pickup → out_for_delivery → delivered → completed`

Ветки: отказ, отмена клиентом, failed_delivery, returned.

**Priority sort:** new+overdue SLA → ASAP/slot 2h → today → rest.

---

## 6. Chat / inbox

Routing: identity match → shop by number → sticky assignee → round-robin → B2B keywords → SLA chat.

**Create order from chat:** prefill client/channel/shop → free-text or catalog → source=direct_{channel}.

Channel stance: grey = cheap risk; official = recommended Full for year SLA.

---

## 7. Integration map

Flowwow adapter (webhook+poll, status+photo) · Messenger hub (WA/TG/MAX) · Notify (TG/VK) · Object storage · (Full) Payments/OFD/Maps.

Patterns: idempotency, outbox retry, reconcile cursor, dead-letter + owner alert.

---

## 8. Architecture blueprint

| Layer | Default |
|-------|---------|
| Frontend | Responsive SPA shell (console CRM) |
| API | Modular monolith (Nest/FastAPI/Go) |
| DB | PostgreSQL |
| Queue | Redis + workers |
| Realtime | WebSocket/SSE |
| Files | S3-compatible (Yandex), РФ |
| Hosting | Yandex Cloud / Timeweb РФ |

**Domains:** Identity, Directory, Orders, Catalog, CRM, Inbox, Fulfillment, Delivery, Finance, Analytics, Integrations, Notify.

---

## 9. Screen sitemap (full UI)

Auth · Сегодня · Заказы (+ detail drawer) · Чаты · Клиенты · Витрина · Склад · Доставка · Финансы · Аналитика · Команда · Настройки · Лояльность · Alerts/Audit · Courier PWA satellite.

---

## 10. MVP → Full roadmap

**MVP:** Auth+shell → Orders+direct → Flowwow dual → Ops UX (SLA) → Inbox → Customers → Health → Deploy РФ.

**Full:** Vitrina · Analytics · Delivery · Finance · Full RBAC · Reminders · Parallel-run tools.

**Later:** Loyalty · Bank/OFD · Courier advanced · Reviews · B2B · Peak AI.

---

## 11. Risks & open questions

Grey ban · FW API limits · status conflicts · 8 Марта load · 152-ФЗ · vendor lock · dirty import · photo cost · «все видят всё» · GPS privacy.

Blockers from questions.md: messenger path, FW write API, multi-account, courier model, scale, client DB, parallel period, loyalty/bank, password recovery, MAX API.

---

## 12. First HTML montage sequence

1. App shell full nav  
2. Order detail drawer (payer≠recipient, открытка, photo, timeline)  
3. Status actions + photo gate  
4. Inbox → Create order  
5. Today ops + SLA + connection chips  
6. Filters/search  
7. Vitrina matrix  
8. Client card  
9. Delivery board  
10. Analytics  
11. Settings/health  
12. Roles  
13. Peak mode  
14. Courier mini-PWA  

**DoD full HTML:** all sitemap clickable · happy path FW new→done + chat→direct · 3 shops · reject · health warn · mobile nav.
