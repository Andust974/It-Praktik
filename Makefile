SHELL := /bin/bash

.PHONY: setup lint fmt typecheck test run dev build clean validate bump

help:
	@echo "Targets: setup lint fmt typecheck test run dev build clean validate bump"

setup:
	pip install -U pip
	pip install -e .[dev]

lint:
	ruff check .

fmt:
	black .
	ruff check --fix .

typecheck:
	mypy src

# Run API with uvicorn
run:
	uvicorn it_praktik.app:app --reload --port 8000

# Dev helper (CLI)
dev:
	python -m it_praktik.cli --help

validate:
	python scripts/validate_module.py

bump:
	python scripts/bump_version.py --set $(VERSION)

build:
	python -m build

clean:
	rm -rf build dist *.egg-info .mypy_cache .pytest_cache htmlcov .ruff_cache
