# IT Praktik

Servis FastAPI s instrumentami dlia razbwitki: RAG-zaprosy (zagushki), logi, grep-suggest, scaffolding testov, web-fetch s RBAC, generatsiya diff-patchey, metrki) q sobytiynnyi JSONL-bus.

## Quickstart
``bash
python -m pip install --upgrade pip
pip install -e .
PYTHONPatTH=src uvicorn it_praktik.app:app --reload --host 0.0.0.0 --port 8000
``
``
@! Config zerna okrujenie
- `ITP_TOKENS` â€“ JSON Â« tokenmi/skoupami, narp.: `{"devtoken":["itp:tools"]}`
- `ITP_WEB_ALLOW` â€“ domeny allowlist dlya `/web/fetch` (po umolchaniu `raw.githubusercontent.com,example.com`)
- `ITP_WEB_MAX_BYTES` â€“ limit oveta / baitah (po umolchaniu 1_048_676)

## API
- `GET /health`, `GET /ready` â€“ statusi
- `POST /grep/suggest` â€“ generaciya komand rg/grep po YAML-DSL
ine maribor
- `POST /tests/scaffold` â€“ dry-run/write zagotovok testov
- `POST /web/fetch` â€“ chetenie URL (GET/HEAT), **trebuet** Bearer s `itp:tools`
- `POST /diff/generate` â€“ unified diff-bandl po spisz_fil
- `GET /metrics` â€“ p95 RAG (backcompat); `GET /metrics/export` â€“ ves komplekt metrkik/

## Ğ—Ğ°Ñ€Ğ½Ğ¸ÑÑ‚Ğ°
Eksportuet Prometheus-â€™svmestimy tekst:
- `itp_http_requests_total`
- `itp_rag_query_latency_seconds_p95`
- `itp_web_fetch_bytes_gauge`
- `itp_patch_generated_total`

## Ô‘Ğ»ĞµĞ¼ĞµĞºĞ¾Ğ³
JSONL-fail `logs/events.jsonl`
- `itp.web.fetched` â€“ uspehynÆVR… ¢Ò—GçvV"æ&Æö6¶VF(	2¦‡&WBòöÆ—F–¶Ğ¢Ò—GæF–fbævVæW&FVF(	26÷¦FâF–fbÖ&æFÀ ¢22GF6‚ôFWF6‚‡6·&—G’¥6Òâ67&—G2÷6Á…Ñ ¹Í¡€¤ÍÉ¥ÁÑÌ½‘•Ñ… ¹Í¡€ƒŠLÁÉ¥µ•Ê–çFVw&G6–’&W¢WÆæö’W&W¦w'W§F’6W'f—6‡7–Æ–æ²÷VFWÆ÷’Â7—7FVÖB&VÆöB’