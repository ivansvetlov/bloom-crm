# Wiki Log

> Append-only. Format: `## [YYYY-MM-DD] action | subject`

## [2026-08-01] create | Wiki + RAG initialized
- Domain: Bloom CRM / flowwow-crm pre-sales + product/architecture
- Structure: SCHEMA, index, entities, concepts, comparisons, raw, chunks, scripts
- Ingested raw: tz, questions, architecture plan, course map, courier research
- Wiki pages: 18
- Built: chunks.jsonl + rag.sqlite (via build_rag.py)

## [2026-08-02] create | Кабинет флориста (concept)
- Решение по роли «Флорист»: свой магазин, ведёт до «В доставке», чаты read-only, витрина своего магазина, «Вернуть менеджеру» вместо отмены
- Фото-гейт «нужно фото до» переносится из тостов менеджера в шаг флориста
- HTML-отчёт: docs/florist-cabinet.html

## [2026-08-02] update | Роли и доступы (демо-вход)
- Auth-гейт с выбором роли карточками: менеджер (admin/admin) / флорист (florist/florist) + ручной вход
- Кабинет флориста реализован в docs/demo.html и синхронизирован в docs/kp/demo, docs/kp/_template

## [2026-08-02] create | Связь с клиентом по заказу (concept, ОТЛОЖЕНО)
- Крайние события: нет диалога / не дозвониться / комментарий клиента
- Автомат 🔵 диалог есть / 🟡 пишем-звоним / 📝 комментарий клиента — согласован, НЕ реализуется в текущей сборке

## [2026-08-02] polish | Кабинет и лендинги (внедрено)
- demo.html: светящаяся рамка на срочные, живые цифры в отчётах, тосты, стеклянный док, список с фото, скелетоны, bento-дашборд, сворачиваемый сайдбар, чип «Сверка с МП» → светящаяся рамка (03)
- auth.js: премиум-гейт (стекло, лепестки, карточки ролей) + «← к КП» виден и флористу
- offer/index/landing: плавающие цветы + текст-волна + KPI-карточки + чипы-гарантии в финальном CTA
- Синхронизировано в docs/kp/demo и docs/kp/_template
