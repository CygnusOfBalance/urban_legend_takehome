PYTHON ?= $(shell command -v python3.10 2>/dev/null || command -v python3)
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

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
	@test -n "$(PYTHON)" || (echo "python3 not found; install Python 3.10+" && exit 1)
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
