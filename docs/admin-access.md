# Bloom CRM · Админка доступа (Access Admin)

**Статус:** прототип IA + clickable shell  
**Файл UI:** [`admin-access.html`](./admin-access.html)  
**Контекст:** отдельно от операционного кабинета (`demo.html`) — зона только для директора / владельца сети / IT.

---

## 1. Зачем отдельно

| Кабинет менеджера | Админка доступа |
|-------------------|-----------------|
| Заказы, чаты, склад, обращения | Пользователи, роли, ACL, аудит |
| Scope «мой магазин» | Scope «вся сеть + кто что видит» |
| Ошибки = потеря заказа | Ошибки = утечка ПДн / чужих точек |

Операционный UI не должен смешиваться с матрицей прав: меньше случайных правок, ясный «admin-only» контур (как Roles/Teams в EspoCRM).

---

## 2. Модель доступа (ядро)

```
User ──*── Role (merge: most permissive wins)
  │           └── Permission[]  (module.action + level)
  ├── ShopScope[]   (own shops | list | network)
  ├── Team[]        (смена / группа, опционально)
  └── PartnerFlag   (изолированный партнёр / франчайзи)
```

### 2.1 Уровни записи (Espo-like)

| Level | Смысл для Bloom |
|-------|-----------------|
| `none` | Нет доступа к модулю |
| `own` | Только свои записи (назначенные менеджеру) |
| `shop` | Все записи точек, в которые входит user |
| `network` | Вся сеть (директор) |
| `partner` | Только «своя» партнёрская точка, без сети |

### 2.2 Модули (permission keys)

| Key | Модуль кабинета |
|-----|-----------------|
| `orders` | Заказы |
| `clients` | Клиенты |
| `chats` | Чаты |
| `mail` | Почта |
| `cases` | Обращения |
| `tasks` | Задачи |
| `notes` | Заметки |
| `catalog` | Номенклатура |
| `warehouses` | Склады |
| `invoices` | Счета |
| `reports` | Отчёты |
| `settings_ops` | Операционные настройки точки |
| `access_admin` | **Эта** админка |
| `marketplace_keys` | API-ключи маркетплейса |
| `export_pdn` | Выгрузка ПДн клиентов |

### 2.3 Действия (поверх level)

Не только CRUD:

- `orders.create_manual` — ручной заказ (Q8)
- `orders.cancel` — отмена
- `orders.edit_price` — цены
- `orders.mark_paid` — отметка оплаты (v1 банк)
- `orders.photo_before` — фото «до» обязательное перед передачей курьеру (флорист)
- `stock.edit` — остатки
- `stock.sync_marketplace` — пуш на маркетплейс
- `cases.close` — закрытие обращения
- `users.invite` / `users.reset_password`
- `roles.edit` — правка матрицы

### 2.4 Роли по умолчанию (пресеты сети)

| Роль | Scope | Суть |
|------|-------|------|
| **Флорист** | shop (1) | Только свой магазин: заказы от «Принят» до «В доставке», фото «до» обязательное, чаты — только чтение, номенклатура своего магазина. Не отменяет заказы — «Вернуть менеджеру»; без счетов, отчётов, настроек, команды, почты, обращений |
| **Менеджер** | shop (1–N) | Заказы + чаты + клиенты точки; отмена; без админки |
| **Старший** | shop (N) | + цены/остатки, обращения, счета точки |
| **Директор сети** | network | Всё + отчёты сети; без tech-only если нужен split |
| **Владелец / Admin** | network | + access_admin, ключи API, аудит |
| **Партнёр / франчайзи** | partner | Только своя точка; чужие клиенты/остатки скрыты |
| **Наблюдатель** | shop/network RO | Read-only для бухгалтерии / инвестора |

Merge ролей: если user = «Менеджер Мира 14» + «Флорист Рижская» → permissive union + union shop list.

---

## 3. Разделы UI админки

1. **Обзор** — KPI: активные users, открытые invites, роли, last ACL change  
2. **Пользователи** — список, invite, disable, shops, роль(и), last login, reset pwd  
3. **Роли** — карточки пресетов + clone/custom  
4. **Матрица прав** — module × action × level (кликабельная)  
5. **Точки и scope** — shop membership matrix user↔shop  
6. **Команды** — teams/смены (опционально, Espo Teams)  
7. **Партнёры** — изолированные профили, white-list модулей  
8. **Вход и пароли** — policy, recovery (admin reset / secret Q, Q13), session  
9. **API и интеграции** — кто видит/ротирует ключи маркетплейса  
10. **Поля (field ACL)** — hide/mask phone export, edit price  
11. **Аудит** — журнал изменений прав  
12. **Пресеты и импорт** — CSV users, apply template  

Связь с опросником: **Q12** (роли), **Q13** (восстановление пароля), **Q20–23** (масштаб/партнёры), **Q7** (ключи per-shop), **Q19** (ПДн export).

---

## 4. Правила безопасности (продукт)

1. **Нельзя снять у себя** `access_admin`, если ты последний admin.  
2. **Partner** никогда не получает `network` / `export_pdn` / `marketplace_keys` чужих точек.  
3. **Chat messages** наследуют shop scope заказа/диалога (child ACL, урок Espo).  
4. **Audit** immutable: create-only log.  
5. **Invite** — magic link 48h; role + shops обязательны до активации.  
6. **Break-glass** — временный network-read для support (TTL + audit), optional later.

---

## 5. Не в v1 админки (явно)

- SSO / SAML  
- SMS 2FA (Q13: без SMS в v1)  
- ABAC по тегам клиента  
- Делегирование «на время отпуска» (можно backlog)

---

## 6. Навигация в продукте

- Из кабинета: Настройки → Сотрудники → **«Открыть админку доступа»** (только `access_admin`)  
- Прямой URL: `/admin/access` (в демо: `admin-access.html`)  
- Не показывать пункт в сайдбаре менеджера

---

## 7. Acceptance (прототип)

- [x] Отдельная страница, Bloom shell  
- [x] 12 разделов IA  
- [x] Матрица прав кликабельна (toggle demo)  
- [x] Users / roles / shops / audit seed data  
- [x] Ссылка из demo Settings → staff  
- [ ] Backend enforcement (вне scope static demo)
