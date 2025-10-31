.PHONY: setup lint test run

setup:
	python -m pip install --upgrade pip
	@if [ -f pyproject.toml ]; then pip install -e .; fi
	pip install pytest ruff mypy pyyaml uvicorn fastapi

lint:
	ruff check src || true
	mypy --ignore-missing-imports src || true

test:
	PYTHONPATH=src pytest -q --maxfail=1 --disable-warnings

run:
	PYTHONPATH=src uvicorn it_praktik.app:app --reload --host 0.0.0.0 --port 8000
