# IT Praktik

FastAPI-сервис для разработки и диагностики: RAG, парсинг логов, grep/rg suggest, scaffold тестов, diff-патчи, безопасный web-fetch, метрики и события.

## Запуск
1) python -m pip install --upgrade pip
2) pip install -e .
3) PYTHONPATH=src uvicorn it_praktik.app:app --reload --host 0.0.0.0 --port 8000

## Основные эндпоинты
- POST /rag/query
- POST /logs/parse
- POST /grep/suggest
- POST /tests/scaffold
- POST /diff/generate
- POST /web/fetch (RBAC)
- GET  /metrics/export
- GET  /health, /ready

## Конфигурация окружения
- ITP_WEB_ALLOW: список доменов для web/fetch (по умолчанию: raw.githubusercontent.com,example.com)
- ITP_WEB_MAX_BYTES: лимит байт загрузки (по умолчанию: 1048576)
- ITP_TOKENS: JSON {"<token>":["itp:tools"]} для RBAC
- ITP_LOG_DIR: каталог логов (по умолчанию: ./logs)

## Логи и метрики
- Логи JSONL: logs/itp.jsonl (obs.log_event)
- Метрики Prometheus: GET /metrics/export

## Attach/Detach
- scripts/attach.sh — подготовка окружения
- scripts/detach.sh — остановка/очистка
