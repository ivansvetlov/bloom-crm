# Bloom · прототип кабинета

**Канонический файл (основа — наша демка):**  
`docs/kp/demo/demo.html`

Зеркала: `docs/demo.html`, `docs/kp/_template/demo.html`

```powershell
start C:\Workspace\projects\flowwow-crm\docs\kp\demo\demo.html
```

## Задумка

Не отдельный mega-файл, а **та же демка**, на которую навешаны модули:

| Слой | Что добавлено |
|------|----------------|
| **База** | `demo.html` — shell, sim заказов, отчёты, TG-чаты |
| **Chatwoot (#2)** | 3-я колонка контакта, private note, assign, заказ из чата, resolve |
| **Twenty (#4)** | ⌘/Ctrl+K command palette |
| **Dolibarr (#5)** | dual badge (канал + оплата), drawer, цепочка Заказ→Оплата→Сборка→Доставка |
| **Mega** | Витрина, Настройки, drawer/stream, модульная навигация |

## Меню

01 Сегодня · 02 Заказы · 03 Чаты · 04 Витрина · 05 Отчёты · 06 Настройки

## Устарело

`docs/cabinet.html` — старый standalone на базе mega (можно не использовать; канон = `kp/demo/demo.html`).
