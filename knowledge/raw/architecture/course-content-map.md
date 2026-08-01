---
source_url: local://knowledge/raw/architecture/course-content-map.md
ingested: 2026-08-01
sha256: 394770df00debf945c377a2a17ddbf26ea587d05b62afcdb60c07d908e8961dc
---

# Content map — Lectoria «CRM с нуля» (эпизоды 1–31)

**Плейлист:** [CRM с нуля](https://www.youtube.com/playlist?list=PLbdTa1GXiMEezle0JF5p0qr_b3TkIcUCj) · канал Lectoria  
**Статус транскриптов:** **24/31 OK** (~529k символов, ru auto-subs в `transcripts/`).  
Эпизоды **25–31** (DialogChoose → Vue) — pending из‑за YouTube rate limit.  
Ниже — takeaways с опорой на фактические транскрипты 01–24 + titles 25–31.

## Фазы курса

| Фаза | Эпизоды | Суть |
|------|---------|------|
| A. Продукт & ТЗ | 001–006 | Что строим, как писать и финализировать ТЗ, обсуждение с «заказчиком» |
| B. IA & прототипы | 007–013 | Диаграмма интерфейсов, Figma-компоненты, Dashboard, таблицы, ревью |
| C. Design system | 011–014, 017–022 | База DS, Button, Textbox, radio/checkbox/datepicker/tabs, filters, dialogs |
| D. Вёрстка HTML/CSS | 015–028 | Среда, BEM, переменные, иконки, SignIn/SignUp/Dashboard/Profile |
| E. Vue foundation | 029–031+ | Stateful TextBox, avatar drop-upload, Composition vs Options API |

---

## По эпизодам — takeaways для Bloom

### 001 Introduction (7JSMhu9MCuk) ✅ transcript
- Open-source CRM «с нуля»: не только код, а **ТЗ → интерфейсы → вёрстка → логика**.
- Идея от подписчика; гибкая базовая версия под кастом клиентов.
- **Bloom:** full cabinet как продукт; florist-domain поверх generic CRM-скелета курса.

### 002 Basis of TZ (udBUieOtmLY) ✅
- ТЗ в git (открытый репозиторий, PR от сообщества).
- Зачем разделы ТЗ, организация хранения.
- **Bloom:** `tz.md` + git; изменения scope — через questions/PR-style freeze.

### 003 Detailing TZ (e-AyosP5o4g) ✅
- Пошаговая детализация требований.
- **Bloom:** acceptance criteria на dual-channel orders, photo-gate, SLA 3 мин.

### 005–006 TZ с стейкхолдером + freeze ✅
- Живое обсуждение ТЗ; финализация перед дизайном.
- **Bloom:** не монтировать full HTML до закрытия P0 (API FW, messengers, courier).

### 007 Диаграмма интерфейсов (LjVZbNyfTzU) ✅
- **Диаграмма переходов** экранов (блоки + стрелки), не pixel UI.
- Первый шаг визуализации после ТЗ.
- **Bloom:** sitemap §9 как interface-transition map; nav shell = edges.

### 008 Компоненты + первый интерфейс Figma (mtuPo2nt-Pg)
- Atomic components → первый экран.
- **Bloom:** DS уже частично в `demo.html` (btn, chip, panel, kcard) — формализовать tokens.

### 009 Dashboard prototype (oHCWltss-3k) + 009.1/009.2 обсуждения
- Dashboard = ops hub дня.
- **Bloom:** «Сегодня» = KPI + feed + hot orders + connection chips (не terminal).

### 010 Таблицы Figma + 010.1 прототипы done (JQe7CdDrVLI, r84WknQ9BP0)
- Data tables = ядро CRM.
- **Bloom:** Orders list + filters + client list — dense table + mobile card fallback.

### 011–014 Design system base (A5TqEtcjR60 … Ktm9Q748kSA)
- Tokens, кнопки, поля, pre-final review.
- **Bloom:** зафиксировать coral/terra hybrid tokens; primary/ghost/danger; inputs с has-val.

### 015–016 Среда + BEM (VZVRL7Ka-bc, YYgWF8NWv0k)
- Структура CSS, BEM naming.
- **Bloom HTML monorepo docs:** `.kcard`, `.kb-col`, `.chat-tab` — держать единый BEM/префикс `bl-`.

### 017–022 Компонентная вёрстка
- Button, Textbox, icons, radio/checkbox/date, tabs, linked-fields, filters, notification, DialogChoose.
- **Bloom must-have DS set для full HTML:** status chips, date slot picker, multi-shop filter, toast, confirm dialog (reject reason), photo dropzone.

### 023–024 Auth + Dashboard + Profile layout
- SignIn/SignUp, Dashboard page, Profile.
- **Bloom:** Login (ТЗ: без SMS) + shell; Profile/staff card в «Команда».

### Layout complete! (Fq72fU7m4xg)
- Static CRM HTML complete milestone.
- **Bloom DoD wave-1:** все пункты sitemap кликабельны + happy path FW + chat→order.

### 029–031 Vue
- Stateful inputs, avatar upload, Composition API.
- **Bloom later stack:** Vue/React SPA; photo upload на order card = dropzone как в 030; composition для order store.

---

## Что применить к Bloom — приоритет

| # | Практика из курса | Действие в проекте |
|---|-------------------|--------------------|
| 1 | ТЗ → freeze → design | Не монтировать full CRM без закрытых P0-вопросов |
| 2 | Диаграмма интерфейсов | Закрепить sitemap в HTML-навигации demo |
| 3 | DS first (button/field/table) | Вынести tokens + components sheet |
| 4 | Dashboard = день операций | «Сегодня» как home, не «analytics dump» |
| 5 | Tables + filters | Orders/Clients dense UI |
| 6 | Dialogs (choose, confirm) | Reject reason, shop pick, courier assign |
| 7 | Notification pattern | Toast + in-app feed (уже seed) |
| 8 | Auth pages | Login simple password |
| 9 | BEM/structure | Чистая структура full-crm.html |
| 10 | Vue later | HTML static first (курс сам так шёл: layout → framework) |

## Чего в курсе нет (наш домен)

- Flowwow dual sync, photo-before-leave, unified WA/TG/MAX, multi-shop vitrina, peak 8 Марта, 152-ФЗ, courier PWA.  
Эти блоки — из `tz.md` + research courier, **не** из Lectoria.

## Next for transcripts

1. Скачать субтитры с домашней сети / cookies Chrome (закрыть браузер → `yt-dlp --cookies-from-browser chrome`).  
2. Или вручную: открыть плейлист → CC → сохранить.  
3. Повторить `_fetch_playlist.py` / batch yt-dlp когда спадёт 429.
