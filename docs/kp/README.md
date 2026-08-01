# Коммерческие предложения (КП)

Каждый заказчик — отдельная папка:

```text
docs/kp/
  index.json          ← реестр всех КП (читает хаб на главной)
  _template/          ← чистый шаблон (не править «под клиента»)
  flowwow/            ← пример: первое КП
  {slug}/             ← следующий клиент
    client.json
    index.html        ← точка входа (КП)
    demo.html
    questions.html
    …
```

## Ссылки

| Что | URL (GitHub Pages) |
|---|---|
| Хаб | `https://ivansvetlov.github.io/flowwow-crm/` |
| КП flowwow | `…/kp/flowwow/` |
| Демо | `…/kp/flowwow/demo.html` |
| Опросник | `…/kp/flowwow/questions.html` |

На Timeweb после деплоя: `https://flowww.webtm.ru/kp/flowwow/`  
(файлы класть в `public_html` **сайта flowww.webtm.ru**, с сохранением папки `kp/`).

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

## Деплой на Timeweb (в WebConsole)

```bash
# путь сайта flowww.webtm.ru (уточните find'ом, если другой)
WEB="$HOME/flowww.webtm.ru/public_html"
# или: WEB=$(find ~ -maxdepth 4 -type d -path '*flowww*' -name public_html | head -1)

cd /tmp
rm -rf flowwow-crm-master crm.zip
curl -fsSL -o crm.zip https://github.com/ivansvetlov/flowwow-crm/archive/refs/heads/master.zip
unzip -qo crm.zip
mkdir -p "$WEB/kp"
cp -f flowwow-crm-master/docs/index.html "$WEB/"
cp -rf flowwow-crm-master/docs/kp/* "$WEB/kp/"
chmod -R a+rX "$WEB/kp" "$WEB/index.html"
echo "OK https://flowww.webtm.ru/  и  https://flowww.webtm.ru/kp/flowwow/"
```

**Важно:** не копировать «первый попавшийся» `public_html` — только папка **flowww.webtm.ru**.
