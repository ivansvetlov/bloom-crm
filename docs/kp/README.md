# Коммерческие предложения (КП)

```text
docs/kp/
  index.json          ← реестр
  _template/          ← шаблон
  demo/               ← демо-КП (бренд Bloom)
  {slug}/             ← клиент
```

## Боевой домен

**`https://crmbloom.ru`** — см. [docs/DOMAIN.md](../DOMAIN.md).

| Что | URL |
|---|---|
| Хаб | `https://crmbloom.ru/` |
| Демо-КП | `https://crmbloom.ru/kp/demo/` |

## Новое КП

```powershell
.\docs\scripts\new-kp.ps1 -Slug roza-spb -Title "Роза СПб" -Client "ООО Роза"
```

## Правила

1. В **бренде и путях продукта** не используем маркетплейс / маркетплейс-crm.
2. Слона маркетплейс в текстах КП — только как **маркетплейс-канал** (интеграция), не как имя продукта.
3. Статус: `draft` | `active` | `archived`.
4. slug — латиница: `roza-spb`, `demo`.

## Деплой

См. `docs/DOMAIN.md` и `docs/scripts/deploy-timeweb.sh`.
