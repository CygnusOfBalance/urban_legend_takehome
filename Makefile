PYTHON ?= python3.10
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

define require_python310
	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "Python 3.10+ required (install python3.10)" && exit 1)
	@$(PYTHON) -c 'import sys; assert sys.version_info >= (3, 10), f"Python 3.10+ required, got {sys.version}"'
endef

.PHONY: help setup install migrate test run shell clean

help:
	@echo "Targets:"
	@echo "  make setup    Create venv, install deps, run migrations"
	@echo "  make install  Install deps into existing venv"
	@echo "  make migrate  Apply database migrations"
	@echo "  make test     Run integration tests"
	@echo "  make run      Start the dev server"
	@echo "  make shell    Open Django shell"
	@echo "  make clean    Remove venv and local database"

$(VENV)/bin/python:
	$(require_python310)
	$(PYTHON) -m venv $(VENV)

setup: $(VENV)/bin/python install migrate
	@echo "Ready. Run: make run"

install: $(VENV)/bin/python
	$(PIP) install -r requirements.txt

migrate: $(VENV)/bin/python
	$(PY) manage.py migrate

test: $(VENV)/bin/python
	$(PY) manage.py test tinyrouter.tests

run: $(VENV)/bin/python
	$(PY) manage.py runserver

shell: $(VENV)/bin/python
	$(PY) manage.py shell

clean:
	rm -rf $(VENV) db.sqlite3
	find . -path './.venv' -prune -o -type d -name __pycache__ -print -exec rm -rf {} +
