# -*- coding: utf-8 -*-
"""Strip OSS/research tech jargon from demo + admin-access product UI copy."""
from pathlib import Path
import re

BASE = Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\demo")
COPIES_DEMO = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\demo.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\demo.html"),
]
COPIES_ADMIN = [
    Path(r"C:\Workspace\projects\flowwow-crm\docs\admin-access.html"),
    Path(r"C:\Workspace\projects\flowwow-crm\docs\kp\_template\admin-access.html"),
]

demo = (BASE / "demo.html").read_text(encoding="utf-8")
admin = (BASE / "admin-access.html").read_text(encoding="utf-8")

# ─── exact string replacements (demo) ───
repls = [
    ("Bloom CRM — прототип кабинета", "Bloom CRM — кабинет"),
    ("Система для цветочной сети. CRM для маркетплейса цветов — демо кабинета.",
     "Кабинет цветочной сети: заказы, чаты, склады, обращения."),
    ("Bloom CRM <span class=\"pro\">ПРОТОТИП</span>", "Bloom CRM"),
    ("title=\"Twenty\">⌘K поиск", "title=\"Быстрый поиск\">⌘K поиск"),
    (
        """    <div class="demo-note">
      <span class="tag">LIVE</span>
      <span>Прототип на базе демо · слои: <b>Chatwoot</b> (чаты) · <b>Twenty</b> (⌘K) · <b>Dolibarr</b> (dual status / витрина) · <b>mega</b> (модули)</span>
    </div>""",
        """    <div class="demo-note">
      <span class="tag">LIVE</span>
      <span>Демо-данные сети · 3 точки · заказы, чаты и склады обновляются в реальном времени</span>
    </div>""",
    ),
    # top proto chips block under note
    (
        """    <div class="proto-chips">
      <span class="chip">Chatwoot · mine/unassigned · labels · snooze · canned · note</span>
      <span class="chip">Twenty · клиенты + задачи + заметки + ⌘K</span>
      <span class="chip">ERPNext · список заказов + номенклатура</span>
      <span class="chip">Dolibarr · счета + склады</span>
      <span class="chip">Dolibarr · оплата ∥ статус</span>
      <span class="chip sage">Mega · витрина / настройки / drawer</span>
    </div>
""",
        "",
    ),
    ('data-oview="list">Список · ERPNext</button>', 'data-oview="list">Список</button>'),
    ("Оси статуса (ERPNext-style)", "Статус и оплата"),
    ("Карточка · Chatwoot", "Карточка диалога"),
    # section chips + intros
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Twenty · Tasks workspace</span>
      </div>
""",
        "",
    ),
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Twenty · Notes workspace</span>
      </div>
""",
        "",
    ),
    ("Выберите задачу · как Tasks в Twenty", "Выберите задачу"),
    ("Выберите заметку · как Notes в Twenty", "Выберите заметку"),
    ("Выберите клиента в таблице · как People в Twenty", "Выберите клиента в таблице"),
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">ERPNext · Item / Stock</span>
        <span class="chip">Dolibarr · остатки</span>
      </div>
""",
        "",
    ),
    (
        """        <b>Номенклатура</b> — справочник SKU как в ERPNext Item.
""",
        """        <b>Номенклатура</b> — букеты, упаковка, доп. позиции. Остатки по точкам и цены.
""",
    ),
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Dolibarr · multi-warehouse</span>
      </div>
""",
        "",
    ),
    (
        """        <b>Склады</b> — остатки SKU по складам сети (как multi-warehouse в Dolibarr).
""",
        """        <b>Склады</b> — остатки по точкам сети и хабу.
""",
    ),
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Dolibarr · Facture / счета</span>
      </div>
""",
        "",
    ),
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">EspoCRM · Cases</span>
        <span class="chip">Жалобы · обратная связь · претензии</span>
        <span class="chip">Отдельно от заказа (KPI)</span>
      </div>
""",
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Жалобы · обратная связь · претензии</span>
        <span class="chip">Отдельно от заказа</span>
      </div>
""",
    ),
    ("Выберите обращение · Case + Stream (EspoCRM)", "Выберите обращение"),
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Krayin · Mail folders</span>
        <span class="chip">Связь с клиентом / заказом</span>
      </div>
""",
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Входящие · исходящие · черновики</span>
        <span class="chip">Связь с клиентом и заказом</span>
      </div>
""",
    ),
    (
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Конфиг под опросник · 25 Q / 9 блоков</span>
        <span class="chip">Максимальные ответы заказчика (демо)</span>
      </div>
""",
        """      <div class="proto-chips" style="margin-top:0">
        <span class="chip">Настройки сети</span>
        <span class="chip">Каналы · точки · права · доставка</span>
      </div>
""",
    ),
    ("Bloom CRM · демо кабинета для флористов", "Bloom CRM · кабинет цветочной сети"),
    ("body: 'Dolibarr-цепочка: заказ → счёт.'", "body: 'Нужен счёт по заказу с герберами.'"),
    ("text: 'Из почты · email-to-case'", "text: 'Создано из письма'"),
    ("toast(state.noteMode ? 'Private note · Chatwoot' : 'Ответ клиенту');",
     "toast(state.noteMode ? 'Приватная заметка' : 'Ответ клиенту');"),
    ("history: [{ t: Date.now(), text: 'Создан из чата (Chatwoot pattern)' }]",
     "history: [{ t: Date.now(), text: 'Создан из чата' }]"),
    ("'<div style=\"font-weight:800;font-size:0.84rem;margin-bottom:6px\">Лента (Espo-style stream)</div>' +",
     "'<div style=\"font-weight:800;font-size:0.84rem;margin-bottom:6px\">Лента заказа</div>' +"),
    ("'<button type=\"button\" class=\"btn\" id=\"odMakeInv\">+ Счёт (Dolibarr)</button>';",
     "'<button type=\"button\" class=\"btn\" id=\"odMakeInv\">+ Счёт</button>';"),
    ("toast('Ответ · черновик (stub Krayin compose)');",
     "toast('Черновик ответа создан');"),
    ("{ id: 'mailcfg', ix: '10', title: 'Почта IMAP/SMTP', sub: 'Krayin Email settings', q: '—' },",
     "{ id: 'mailcfg', ix: '10', title: 'Почта', sub: 'Ящики и подписи', q: '—' },"),
    ("html += '<div class=\"set-block\"><h4>Krayin Email settings</h4>';",
     "html += '<div class=\"set-block\"><h4>Почтовые ящики</h4>';"),
    ("html += setRow('Связь', 'Письмо ↔ клиент / заказ (как Lead link в Krayin)', setTag('ok', 'link'));",
     "html += setRow('Связь', 'Письмо привязано к клиенту и заказу', setTag('ok', 'link'));"),
    ("html += '<div class=\"set-max\"><b>Паттерн Krayin:</b> folders + compose + entity-linked thread. Не замена мессенджеров — email-канал рядом с inbox.</div>';",
     "html += '<div class=\"set-max\"><b>Почта</b> — отдельный канал рядом с мессенджерами: папки, ответ, связь с заказом.</div>';"),
    ("html += setRow('Паттерны UI', 'Chatwoot · Twenty · Dolibarr · Krayin mail', setTag('ok', 'OSS'));",
     "html += setRow('Статус', 'Каналы подключены · демо-данные', setTag('ok', 'ok'));"),
    ("el.innerHTML = '<div style=\"color:var(--ink-faint);font-size:0.86rem\">Выберите клиента · People как в Twenty</div>';",
     "el.innerHTML = '<div style=\"color:var(--ink-faint);font-size:0.86rem\">Выберите клиента</div>';"),
    ("o.history.push({ t: Date.now(), text: 'Счёт ' + inv.id + ' создан (Dolibarr Facture)' });",
     "o.history.push({ t: Date.now(), text: 'Счёт ' + inv.id + ' создан' });"),
    ("el.innerHTML = '<div class=\"tw-empty\">Выберите задачу · workspace Tasks (Twenty)</div>';",
     "el.innerHTML = '<div class=\"tw-empty\">Выберите задачу</div>';"),
    ("el.innerHTML = '<div class=\"tw-empty\">Выберите заметку · workspace Notes (Twenty)</div>';",
     "el.innerHTML = '<div class=\"tw-empty\">Выберите заметку</div>';"),
    ("el.innerHTML = '<div class=\"cs-empty\">Выберите обращение · Case + Stream (EspoCRM)</div>';",
     "el.innerHTML = '<div class=\"cs-empty\">Выберите обращение</div>';"),
    ("'<div class=\"cs-stream-title\">Лента (Stream)</div>' +",
     "'<div class=\"cs-stream-title\">Лента</div>' +"),
    ("'<button type=\"button\" class=\"btn terra\" data-cs-act=\"note\">Добавить в Stream</button>' +",
     "'<button type=\"button\" class=\"btn terra\" data-cs-act=\"note\">Добавить в ленту</button>' +"),
    # settings intros with questionnaire tech
    ("html += '<div class=\"set-lead\">' + esc(sec.sub) + ' · значения ниже = демо «максимум требований» из формы вопросов</div>';",
     "html += '<div class=\"set-lead\">' + esc(sec.sub) + '</div>';"),
    ("html += '<span class=\"set-qref\">Опросник · вопросы ' + esc(sec.q) + '</span>';",
     "html += (sec.q && sec.q !== '—' ? '<span class=\"set-qref\">Связано с брифом · ' + esc(sec.q) + '</span>' : '');"),
    ("subtitle: 'Демо Bloom CRM · test login',",
     "subtitle: 'Вход в демо-кабинет сети',"),
    ("toast('Настройки сохранены (демо, local only)');",
     "toast('Настройки сохранены');"),
    ("Позже: ACL по выбранному магазину<span>roadmap</span>",
     "Права по магазину настраиваются в админке<span>доступ</span>"),
]

# generic soft replacements that may appear in multiple places
soft = [
    (r"Private note · Chatwoot", "Приватная заметка"),
    (r"Chatwoot", ""),
    (r"Twenty", ""),
    (r"Dolibarr", ""),
    (r"ERPNext", ""),
    (r"Krayin", ""),
    (r"EspoCRM", ""),
    (r"Espo-style", ""),
    (r"Espo-like", ""),
    (r"Espo Teams", "команды"),
    (r"Espo", ""),
    (r"\(stub[^)]*\)", ""),
    (r"stub", ""),
    (r"OSS", ""),
    (r"workspace Tasks \(Twenty\)", "задачу"),
    (r"workspace Notes \(Twenty\)", "заметку"),
    (r" ·  +", " · "),
    (r"  +", " "),
]

# CSS comment cleanup (not user-visible but keep product tone in source)
css_comments = [
    ("/* ═══ Prototype layers: Chatwoot · Twenty · Dolibarr · Mega ═══ */", "/* product modules */"),
    ("/* ═══ Shop switcher + Clients (Twenty) ═══ */", "/* shop switcher + clients */"),
    ("/* ═══ ERPNext: order list + nomenclature ═══ */", "/* orders list + catalog */"),
    ("/* ═══ Dolibarr: invoices + warehouses ═══ */", "/* invoices + warehouses */"),
    ("/* ═══ Chatwoot inbox features · Bloom style ═══ */", "/* chats inbox */"),
    ("/* ═══ Twenty: Tasks + Notes ═══ */", "/* tasks + notes */"),
    ("/* ═══ Krayin: Mail + Settings ═══ */", "/* mail + settings */"),
    ("/* ═══ EspoCRM: Cases → Обращения ═══ */", "/* cases / appeals */"),
    ("/* Stream (Espo) */", "/* case stream */"),
    ("/* Mail (Krayin) + Settings nav */", "/* mail + settings nav */"),
    ("/* Cases (EspoCRM → Обращения) */", "/* cases */"),
    ("/* ────────────────────────── ORDER DRAWER (Dolibarr chain + stream) ────────────────────────── */",
     "/* ────────────────────────── ORDER DRAWER ────────────────────────── */"),
    ("/* ────────────────────────── MAIL (Krayin) ────────────────────────── */",
     "/* ────────────────────────── MAIL ────────────────────────── */"),
    ("/* ────────────────────────── SETTINGS (опросник 25Q) ────────────────────────── */",
     "/* ────────────────────────── SETTINGS ────────────────────────── */"),
    ("/* Демо: «максимальные» ответы заказчика — верхняя граница потребностей из questions.html */",
     "/* demo settings values */"),
    ("/* ────────────────────────── CMD+K  /* ────────────────────────── CMD+K (Twenty) ────────────────────────── */",
     "/* ────────────────────────── CMD+K ────────────────────────── */"),
    ("/* ────────────────────────── CLIENTS (Twenty) ────────────────────────── */",
     "/* ────────────────────────── CLIENTS ────────────────────────── */"),
    ("/* ────────────────────────── WAREHOUSES (Dolibarr) ────────────────────────── */",
     "/* ────────────────────────── WAREHOUSES ────────────────────────── */"),
    ("/* ────────────────────────── INVOICES (Dolibarr Facture) ────────────────────────── */",
     "/* ────────────────────────── INVOICES ────────────────────────── */"),
    ("/* ────────────────────────── TASKS + NOTES (Twenty) ────────────────────────── */",
     "/* ────────────────────────── TASKS + NOTES ────────────────────────── */"),
    ("/* ────────────────────────── CASES RENDER (EspoCRM → Обращения) ────────────────────────── */",
     "/* ────────────────────────── CASES ────────────────────────── */"),
    ("<!-- ═════════════ CHATS · Chatwoot patterns in Bloom style ═════════════ -->",
     "<!-- ═════════════ CHATS ═════════════ -->"),
    ("<!-- ═════════════ CLIENTS (Twenty people) ═════════════ -->",
     "<!-- ═════════════ CLIENTS ═════════════ -->"),
    ("<!-- ═════════════ TASKS (Twenty) ═════════════ -->",
     "<!-- ═════════════ TASKS ═════════════ -->"),
    ("<!-- ═════════════ NOTES (Twenty) ═════════════ -->",
     "<!-- ═════════════ NOTES ═════════════ -->"),
    ("<!-- ═════════════ 05 · VITRINA (Dolibarr stock) ═════════════ -->",
     "<!-- ═════════════ CATALOG ═════════════ -->"),
    ("<!-- ═════════════ 06 · SETTINGS (mega) ═════════════ -->",
     "<!-- ═════════════ SETTINGS ═════════════ -->"),
    ("<!-- ═════════════ WAREHOUSES (Dolibarr multi-warehouse) ═════════════ -->",
     "<!-- ═════════════ WAREHOUSES ═════════════ -->"),
    ("<!-- ═════════════ INVOICES (Dolibarr Facture) ═════════════ -->",
     "<!-- ═════════════ INVOICES ═════════════ -->"),
    ("<!-- ═════════════ CASES / ОБРАЩЕНИЯ (EspoCRM) ═════════════ -->",
     "<!-- ═════════════ CASES ═════════════ -->"),
    ("<!-- ═════════════ MAIL (Krayin) ═════════════ -->",
     "<!-- ═════════════ MAIL ═════════════ -->"),
]

for a, b in repls + css_comments:
    if a in demo:
        demo = demo.replace(a, b)
    else:
        # try flexible whitespace for multi-line
        pass

# HTML comments with sources that remain
demo = re.sub(r"\(Twenty\)|\(Chatwoot[^)]*\)|\(Dolibarr[^)]*\)|\(ERPNext[^)]*\)|\(Krayin[^)]*\)|\(EspoCRM[^)]*\)|\(mega\)", "", demo, flags=re.I)

# Remaining product strings - careful sequential
more = [
    ("Источники паттернов", "Интеграции"),
    ("dual status · витрина", "статус и оплата"),
    ("mega", ""),
    ("Mega", ""),
    ("Facture", "счёт"),
    ("Item / Stock", "каталог"),
    ("multi-warehouse", "склады"),
    ("email-to-case", "из письма"),
    ("People как в", ""),
    ("как в ERPNext Item", ""),
    ("как multi-warehouse в", ""),
    ("(как Lead link в )", ""),
    ("Паттерн :", "Почта:"),
    ("roadmap", "доступ"),
    ("local only", ""),
    ("test login", "демо"),
    ("Прототип", "Демо"),
    ("прототип", "демо"),
    ("ПРОТОТИП", "ДЕМО"),
]

for a, b in more:
    demo = demo.replace(a, b)

# Clean empty badges / double spaces in chips left over - only in visible-ish patterns
demo = re.sub(r" · \.", ".", demo)
demo = re.sub(r"·\s*·", "·", demo)
demo = re.sub(r"  {2,}", " ", demo)

# Fix settings integrations leftover empty
demo = demo.replace("html += setRow('Статус', 'Каналы подключены · демо-данные', setTag('ok', 'ok'));",
                    "html += setRow('Статус', 'Каналы подключены · демо-данные', setTag('ok', 'ok'));")

# ─── admin-access ───
admin_repls = [
    ("Bloom CRM — Админка доступа", "Bloom CRM — Админка доступа"),
    ("<div class=\"sb-pill\">Только access_admin · не кабинет смены</div>",
     "<div class=\"sb-pill\">Только для владельца сети · не кабинет смены</div>"),
    ("<span class=\"chip ok\">Espo-like ACL</span>",
     "<span class=\"chip ok\">Права по ролям</span>"),
    ("<span class=\"chip warn\">Прототип</span>",
     "<span class=\"chip warn\">Демо</span>"),
    ("несколько ролей сливаются permissive (как Espo). Партнёр никогда не получает network / чужие ключи / export ПДн.",
     "несколько ролей складываются в пользу большего доступа. Партнёр не видит сеть, чужие ключи и выгрузку всех клиентов."),
    ("Опциональный слой Espo Teams: утренняя смена, B2B-группа. Не заменяет shop scope.",
     "Смены и рабочие группы. Не заменяют доступ к точкам."),
    ("Экспорт CSV (stub)", "Экспорт CSV"),
    ("Загрузить (stub)", "Загрузить"),
    ("toast('Пароль сброшен · ссылка 48ч (stub)');",
     "toast('Пароль сброшен · ссылка на 48 часов');"),
    ("toast('Ключ ротирован (stub)');", "toast('Ключ обновлён');"),
    ("toast('Состав команды (stub)');", "toast('Состав команды');"),
    ("toast('CSV аудита (stub)');", "toast('CSV аудита');"),
    ("toast('Импорт CSV (stub)');", "toast('Импорт CSV');"),
    ("subtitle: 'Только access_admin · test login',",
     "subtitle: 'Вход только для администратора сети',"),
    ("Модель (кратко)", "Как устроены права"),
    ("User × Roles (merge max) × ShopScope × PartnerFlag. Уровни: none → own → shop → network | partner.",
     "Сотрудник · роли · точки · признак партнёра. Уровни: нет · свои · точка · сеть · партнёр."),
    ("Контур управления правами сети: роли, точки, партнёры, аудит. Отделён от операционного кабинета, чтобы случайно не сломать ACL со смены.",
     "Роли, точки, партнёры и журнал изменений. Отдельно от кабинета смены — чтобы случайно не сменить права во время работы."),
    ("Membership user ↔ shop. Директор = network (все). Партнёр = ровно одна изолированная точка.",
     "К каким точкам допущен сотрудник. Директор — вся сеть. Партнёр — только своя точка."),
    ("Q23: изолированный доступ. White-list модулей, запрет network и чужих клиентов.",
     "Изолированный доступ партнёра: только свои модули, без сети и чужих клиентов."),
    ("Q13: логин+пароль без SMS. Восстановление — admin reset (+ опц. секретный вопрос).",
     "Вход по логину и паролю. Восстановление — сброс администратором (или секретный вопрос)."),
    ("Q7: ключи маркетплейса per-shop. Кто может смотреть / ротировать.",
     "Ключи маркетплейса по точкам. Кто может смотреть и обновлять."),
    ("Маскирование и запрет edit на чувствительных полях — поверх module level.",
     "Скрытие и запрет правок на чувствительных полях."),
    ("Immutable log: кто менял роли, scope, ключи. Create-only (152‑ФЗ / разбор инцидентов).",
     "Кто менял роли, точки и ключи. Записи только добавляются."),
    ("Шаблоны ролей под масштаб (Q20–22) и CSV сотрудников.",
     "Шаблоны ролей под размер сети и импорт сотрудников из CSV."),
    ("Пресеты + custom", "пресеты"),
    ("scope membership", "доступы к точкам"),
    ("action marketplace_keys:", "Ключи маркетплейса:"),
    ("только owner + директор (по умолчанию). Менеджер точки — нет.",
     "только владелец и директор. Менеджер точки — нет."),
    ("Hard deny network.", "без доступа к сети."),
    ("Invite batch.", "пакетное приглашение."),
    ("magic link 48h", "ссылка 48 ч"),
    ("(stub)", ""),
]

for a, b in admin_repls:
    if a in admin:
        admin = admin.replace(a, b)

for a, b in [
    ("Espo-like", ""),
    ("Espo Teams", "команды"),
    ("Espo", ""),
    ("access_admin", "админка"),
    ("(stub)", ""),
    (" stub", ""),
    ("ACL", "права"),
    ("network", "сеть"),
    ("Shop scope", "точки"),
    ("permissive", "максимальные права"),
    ("White-list", "Разрешённый список"),
    ("Create-only", "Только добавление"),
]:
    # only in visible text portions - do carefully for admin
    pass

# Safer admin visible cleanups already done; fix leftover "админка" over-replace in module id
# Don't replace access_admin in JS ids - I already only changed display strings

# Clean "// Twenty ⌘K" comments etc in demo
demo = re.sub(r"// Twenty ⌘K", "// quick search", demo)
demo = re.sub(r"// open order drawer.*", "// open order drawer", demo)
demo = re.sub(r"// mock:.*", "// sync stock", demo)
demo = re.sub(r"// mock site drift", "", demo)
demo = re.sub(r"// siteStock stays until API sync", "", demo)

# Product polish: set-max leftover questionnaire wording
demo = demo.replace("демо «максимум требований» из формы вопросов", "типовые значения для сети")
demo = demo.replace("Максимум из формы:", "Типовой максимум:")
demo = demo.replace("Максимум:", "Типовой максимум:")
demo = demo.replace("<b>Максимум:</b>", "<b>Типовой максимум:</b>")
demo = demo.replace("Опросник · вопросы", "Бриф ·")
demo = demo.replace("Связано с брифом", "Бриф")

# Remove orphan empty class remnants like " ·  · "
demo = re.sub(r" · \s*·", " ·", demo)

# Footer / auth product
demo = demo.replace("Демо Bloom CRM · test login", "Вход в кабинет")
demo = demo.replace("Демо Bloom CRM · демо", "Вход в кабинет")

# Write
(BASE / "demo.html").write_text(demo, encoding="utf-8")
(BASE / "admin-access.html").write_text(admin, encoding="utf-8")
for c in COPIES_DEMO:
    c.write_text(demo, encoding="utf-8")
for c in COPIES_ADMIN:
    c.write_text(admin, encoding="utf-8")

# Report remaining tech terms
terms = ["Chatwoot", "Twenty", "Dolibarr", "ERPNext", "Krayin", "EspoCRM", "Espo", "Mega CRM", "OSS", "прототип", "ПРОТОТИП", "stub", "workspace Tasks"]
print("=== remaining in demo (visible-ish) ===")
for term in terms:
    n = demo.count(term)
    if n:
        print(f"  {term}: {n}")
print("=== remaining in admin ===")
for term in terms:
    n = admin.count(term)
    if n:
        print(f"  {term}: {n}")
print("OK", len(demo), len(admin))
