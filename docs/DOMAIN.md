# Домен crmbloom.ru

**Боевой бренд-домен продукта:** `https://crmbloom.ru`  
Без «flowwow» в имени. Flowwow — только интеграция/контекст КП, не бренд.

| Назначение | URL |
|---|---|
| Хаб КП | `https://crmbloom.ru/` |
| КП (пример) | `https://crmbloom.ru/kp/flowwow/` |
| Демо | `https://crmbloom.ru/kp/flowwow/demo.html` |
| Опросник | `https://crmbloom.ru/kp/flowwow/questions.html` |
| Потом CRM | `https://app.crmbloom.ru` (когда появится) |

Песочница (можно не использовать): `flowww.webtm.ru`, GitHub Pages.

## Привязка в Timeweb (после покупки)

1. **Домены** → `crmbloom.ru` должен быть в аккаунте.
2. **Сайты** → создать сайт **или** привязать домен к существующему (лучше новый «Основной сайт» / отдельный сайт):
   - домен: `crmbloom.ru` (+ `www.crmbloom.ru` по желанию)
   - корень: `public_html` этого сайта
3. **DNS** (если NS уже Timeweb — обычно A проставится сам):
   - `@` → A → IP хостинга (как у сайта, часто `92.53.x.x` — смотрите в карточке сайта)
   - `www` → CNAME → `crmbloom.ru` **или** A на тот же IP
4. **SSL** → Let’s Encrypt на `crmbloom.ru` (и www), подождать 5–30 мин после DNS.
5. Залить файлы **в public_html сайта crmbloom.ru** (не в `flwww.dev.crm.ru` и не «первый попавшийся» public_html).

### Деплой из WebConsole

```bash
WEB="$HOME/crmbloom.ru/public_html"
# если путь другой:
# find ~ -maxdepth 4 -type d -name public_html

cd /tmp && rm -rf flowwow-crm-master crm.zip
curl -fsSL -o crm.zip https://github.com/ivansvetlov/flowwow-crm/archive/refs/heads/master.zip
unzip -qo crm.zip
mkdir -p "$WEB/kp"
cp -f flowwow-crm-master/docs/index.html "$WEB/"
cp -f flowwow-crm-master/docs/{demo,questions,landing,security,test-dynamic}.html "$WEB/" 2>/dev/null || true
cp -rf flowwow-crm-master/docs/kp/. "$WEB/kp/"
chmod -R a+rX "$WEB/kp" "$WEB/index.html"
echo "https://crmbloom.ru/kp/flowwow/"
```

Проверка:

```bash
ls -la "$WEB/index.html" "$WEB/kp/flowwow/index.html"
```

В браузере: `https://crmbloom.ru/` и `https://crmbloom.ru/kp/flowwow/`.

## Заказчику отдавать

Только: **`https://crmbloom.ru/kp/flowwow/`**  
(не хаб со списком всех клиентов, если не хотите светить других).
