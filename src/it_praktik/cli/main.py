from __future__ import annotations

import json
from pathlib import Path
import typer

from it_praktik import __version__
from it_praktik.grep_dsl import parse_rules_yaml, build_commands
from it_praktik.tests_scaffold import scaffold as scaffold_tests

app = typer.Typer(help="IT Praktik CLI")

@app.command()
def version():
    """Показать версию пакета"""
    typer.echo(__version__)

@app.command()
def grep_suggest(paths: list[str], rules_file: Path, tool: str = "rg"):
    """Сгенерировать команды rg/grep по YAML-правилам

    
    """
    inline = rules_file.read_text(encoding="utf-8")
    rules = parse_rules_yaml(inline)
    cmds = build_commands([str(p) for p in paths], rules, tool=tool)
    typer.echo(json.dumps(cmds, ensure_ascii=False, indent=2))

@app.command()
def scaffold_tests_cmd(mode: str = typer.Option("dry-run", help="dry-run|write")):
    """Сгенерировать каркасы тестов (dry-run|write)."""
    res = scaffold_tests(dry_run=(mode == "dry-run"))
    typer.echo(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    app()
