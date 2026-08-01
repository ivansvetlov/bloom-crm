# Dolibarr Structure MVP

**Program:** Bloom CRM open-source CRM research  
**CRM id:** `dolibarr`  
**Entry:** [index.html](./index.html) (offline, no backend)

## Purpose

Clickable **information-architecture shell** of Dolibarr (not a Bloom skin):

- Top module bar + left submenu (classic Dolibarr layout)
- Third parties (Tiers), Commercial, Products, Orders, Invoices stub
- Mock flower-retail data for Bloom-oriented review
- Working order/invoice status buttons and stock adjustments

Badge on UI: **MVP · Dolibarr structure → web**

## Modules

| Top menu | Left menu | Interactive |
|----------|-----------|-------------|
| Главная | Рабочий стол | Stats + module cards + recent orders |
| Контрагенты | Список / Клиенты / Поставщики / Контакты | List, card, status buttons, linked orders |
| Коммерция | КП (stub) / Заказы клиентов / Воронка (stub) | Order list + status flow |
| Товары | Номенклатура / Склад / Склады | Stock adjust +/−, low-stock flags |
| Заказы | Все / В работе / Доска статусов | Advance status, cancel, board columns |
| Счета | Список / К оплате | Validate, pay partial/full, cancel; create from order |

## Order status flow (mock)

`draft → validated → processing → shipped → delivered` (+ `cancelled`)

Mirrors a simplified Dolibarr customer-order lifecycle for ops discussion (Bloom dual-channel: marketplace / direct tags on orders).

## How to open

Open `index.html` in any modern browser (file:// or static server). No build step.

## Out of scope

- Real PHP/Dolibarr backend, ACL, multi-company module
- Full propale → order → invoice document chain
- Drag-and-drop kanban, PDF, payments ledger
