# API

Сводка основных эндпоинтов и примеров. См. также `/openapi.json`.

- `POST /rag/query` — базовый RAG.
- `POST /logs/parse` — правила в YAML для парсинга логов.
- `POST /grep/suggest` — команды `rg/grep` по DSL.
- `POST /tests/scaffold` — генерация тестов.
- `POST /diff/generate` — unified diff.
- `POST /web/fetch` — защищённый GET/HEAD (RBAC + allowlist).
- `GET /metrics/export` — Prometheus.
- `GET /health`, `GET /ready` — статусы.

## Примеры см. в `README.md`.
