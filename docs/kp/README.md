# Коммерческие предложения (КП)

Каждый заказчик — отдельная папка:

```text
docs/kp/
  index.json          ← реестр всех КП (читает хаб на главной)
  _template/          ← чистый шаблон (не править «под клиента»)
  flowwow/            ← первое КП (slug клиента, не бренд!)
  {slug}/             ← следующий клиент
    client.json
    index.html        ← точка входа (КП)
    demo.html
    questions.html
    …
```

## Боевой домен

**`https://crmbloom.ru`** — см. [docs/DOMAIN.md](../DOMAIN.md).

| Что | URL |
|---|---|
| Хаб | `https://crmbloom.ru/` |
| КП | `https://crmbloom.ru/kp/flowwow/` |
| Демо | `https://crmbloom.ru/kp/flowwow/demo.html` |
| Опросник | `https://crmbloom.ru/kp/flowwow/questions.html` |

Бэкап (GitHub Pages): `https://ivansvetlov.github.io/flowwow-crm/kp/flowwow/`

## Новое КП за 1 минуту

Из корня репозитория:

```powershell
.\docs\scripts\new-kp.ps1 -Slug roza-spb -Title "Роза СПб" -Client "ООО Роза"
```

Скрипт:
1. копирует `_template` → `kp/roza-spb`
2. пишет `client.json`
3. добавляет запись в `kp/index.json`

Потом поправьте тексты/контакты в HTML под клиента и задеплойте.

## Правила

1. **Не кладите** research, transcripts, knowledge в папку клиента — только то, что видит заказчик.
2. **Не правьте `_template` «под одного клиента»** — правки шаблона только общие; кастом — в `kp/{slug}/`.
3. Статус в `client.json` / `index.json`: `draft` | `active` | `archived`.
4. Имя папки = **slug** латиницей, коротко: `roza-spb`, `cvetochny-mir`.
5. В **домене и бренде** не используем слово flowwow — только в slug КП, если клиент на Flowwow.

## Деплой на Timeweb (в WebConsole)

```bash
WEB="$HOME/crmbloom.ru/public_html"
# или: find ~ -maxdepth 4 -type d -name public_html

cd /tmp
rm -rf flowwow-crm-master crm.zip
curl -fsSL -o crm.zip https://github.com/ivansvetlov/flowwow-crm/archive/refs/heads/master.zip
unzip -qo crm.zip
mkdir -p "$WEB/kp"
cp -f flowwow-crm-master/docs/index.html "$WEB/"
cp -rf flowwow-crm-master/docs/kp/. "$WEB/kp/"
chmod -R a+rX "$WEB/kp" "$WEB/index.html"
echo "OK https://crmbloom.ru/  и  https://crmbloom.ru/kp/flowwow/"
```

**Важно:** копировать в `public_html` сайта **crmbloom.ru**, не в чужой домен аккаунта.
