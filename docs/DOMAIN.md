# Домен crmbloom.ru

**Боевой бренд-домен продукта:** `https://crmbloom.ru`  
Продукт называется **Bloom CRM**, не маркетплейс / маркетплейс-crm.

| Назначение | URL |
|---|---|
| Хаб КП | `https://crmbloom.ru/` |
| КП (демо) | `https://crmbloom.ru/kp/demo/` |
| Демо UI | `https://crmbloom.ru/kp/demo/demo.html` |
| Опросник | `https://crmbloom.ru/kp/demo/questions.html` |
| Потом CRM | `https://app.crmbloom.ru` (когда появится) |

Бэкап: GitHub Pages (репозиторий `bloom-crm`, если переименован).

## Привязка в Timeweb (после покупки)

1. **Домены** → `crmbloom.ru` в аккаунте.
2. **Сайты** → сайт с доменом `crmbloom.ru`, корень `public_html`.
3. **DNS** — NS Timeweb или A на IP сайта; `www` → CNAME на `crmbloom.ru`.
4. **SSL** → Let’s Encrypt.
5. Залить файлы **только** в `public_html` сайта **crmbloom.ru**.

### Деплой из WebConsole

```bash
WEB="$HOME/crmbloom.ru/public_html"
# find ~ -maxdepth 4 -type d -name public_html

cd /tmp && rm -rf bloom-crm-master crm.zip
# если репо ещё маркетплейс-crm — замените имя архива/URL
curl -fsSL -o crm.zip https://github.com/ivansvetlov/bloom-crm/archive/refs/heads/master.zip \
  || curl -fsSL -o crm.zip https://github.com/ivansvetlov/flowwow-crm/archive/refs/heads/master.zip
unzip -qo crm.zip
SRC=$(ls -d /tmp/*crm*-master/docs 2>/dev/null | head -1)
mkdir -p "$WEB/kp"
cp -f "$SRC/index.html" "$WEB/"
cp -f "$SRC"/{demo,questions,landing,security,test-dynamic}.html "$WEB/" 2>/dev/null || true
cp -rf "$SRC/kp/." "$WEB/kp/"
chmod -R a+rX "$WEB/kp" "$WEB/index.html"
echo "https://crmbloom.ru/kp/demo/"
```

## Заказчику отдавать

**`https://crmbloom.ru/kp/demo/`** (или `/kp/{slug}/` для конкретного клиента).
