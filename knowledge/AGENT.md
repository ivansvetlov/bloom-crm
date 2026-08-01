# Инструкция для агента (хостинг)

Ты — агент по проекту **Bloom CRM** (`flowwow-crm`).

## Каждый сеанс
1. `knowledge/SCHEMA.md`
2. `knowledge/index.md`
3. последние записи `knowledge/log.md`

## Ответ на вопрос
```bash
python knowledge/scripts/query_rag.py "<вопрос пользователя>"
```
Дополнительно читай wiki-страницы из hits (`entities/`, `concepts/`).

## Правила
- Не выдумывай возможности API Flowwow — см. `[[open-questions]]`
- Мессенджеры: grey vs official — `[[messengers-official-vs-grey]]`
- MVP vs Full — `[[mvp-scope]]`
- Стоимость — `[[monthly-cost]]`
- Вопросы формы — `[[customer-questions]]` (25 шт.)

## Пересборка индекса
```bash
python knowledge/scripts/build_rag.py
```

## Machine RAG
- `knowledge/chunks/chunks.jsonl` — для vector store
- `knowledge/rag.sqlite` — FTS5
- `knowledge/chunks/manifest.json` — метаданные
