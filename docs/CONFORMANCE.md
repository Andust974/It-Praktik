# CONFORMANCE

Мини-набор проверок соответствия сервису IT Praktik.

- `/health` → 200 и JSON со `status=ok`.
- `/ready` → 200 и `ready=true`.
- `/metrics/export` → Prometheus text и ключ `itp.rag.query_latency_p95_seconds`.
- RBAC: `/web/fetch` требует `Authorization: Bearer` со скоупом `itp:tools`.
- Security: `/web/fetch` ограничен по доменам (allowlist).

Скрипт запуска: `scripts/conformance.sh`.
