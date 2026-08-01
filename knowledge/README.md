# Bloom CRM — RAG / knowledge base

База знаний для **агента на хостинге** (и локальных агентов) по проекту flowwow-crm / Bloom CRM.

Два слоя:
1. **Wiki** (markdown + `[[wikilinks]]`) — скомпилированные ответы, как Karpathy LLM Wiki  
2. **RAG index** — `chunks.jsonl` + **SQLite FTS5** (`rag.sqlite`) для поиска по чанкам

```
knowledge/
├── SCHEMA.md              # правила
├── index.md               # каталог страниц
├── log.md                 # журнал
├── entities/ concepts/ comparisons/
├── raw/                   # исходники (immutable)
├── chunks/
│   ├── chunks.jsonl       # для embeddings / OpenWebUI / custom RAG
│   └── manifest.json
├── rag.sqlite             # FTS5 (пересобрать скриптом)
└── scripts/
    ├── build_rag.py
    └── query_rag.py
```

## Быстрый старт (хостинг / VPS)

```bash
cd /path/to/flowwow-crm
python knowledge/scripts/build_rag.py
python knowledge/scripts/query_rag.py "Flowwow аккаунты"
python knowledge/scripts/query_rag.py "SLA поддержка" --limit 8
python knowledge/scripts/query_rag.py "склад остатки" --json
```

Системные зависимости: только **Python 3.10+** (stdlib + sqlite FTS5).  
Embeddings / Chroma / LanceDB **не обязательны**.

## Как агенту пользоваться

### 1. Ориентация (каждый сеанс)
1. Прочитать `knowledge/SCHEMA.md`
2. Прочитать `knowledge/index.md`
3. Хвост `knowledge/log.md`

### 2. Вопрос по продукту / ТЗ / архитектуре
```bash
python knowledge/scripts/query_rag.py "<вопрос>"
```
Затем при необходимости открыть wiki-страницы из `index.md` (entities/concepts).

### 3. Ингест в другой RAG-стек (OpenWebUI, custom vector store)
Загрузить `knowledge/chunks/chunks.jsonl` — поля:
- `id`, `source_id`, `title`, `kind`, `text`, `chunk_index`, `sha256`, `chars`

### 4. System prompt (фрагмент для хостинг-агента)

```
Ты агент по проекту Bloom CRM (flowwow-crm).
Перед ответом: knowledge/index.md + query_rag.py по вопросу.
Цитируй wiki pages ([[name]]) и source_id чанков.
Не выдумывай API Flowwow — сверяйся с open-questions и questions form.
```

## Пересборка
После правок в `docs/tz.md`, `questions.md`, architecture или wiki:

```bash
python knowledge/scripts/build_rag.py
```

## Связанные public pages
| URL path | Role |
|----------|------|
| docs/index.html | КП |
| docs/demo.html | Демо |
| docs/questions.html | Опрос |
| docs/security.html | 152-ФЗ narrative |

## Версия
- knowledge v1.0.0 · 2026-08-01
- chunk sources: TZ, questions, architecture plan, course map, courier research, wiki pages
