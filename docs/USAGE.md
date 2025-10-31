# USAGE

## CLI (Typer)
После установки (или `pip install -e .[dev]`) доступны команды:

```bash
itp version
itp grep-suggest --help
itp scaffold-tests-cmd --help
```

Примеры:

```bash
# Сгенерировать команды rg по YAML-правилам
itp grep-suggest . --rules-file rules.yaml --tool rg > cmds.json

# Сгенерировать тесты в режиме dry-run
itp scaffold-tests-cmd --mode dry-run
# И записать файлы
itp scaffold-tests-cmd --mode write
```
