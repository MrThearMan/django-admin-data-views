export DJANGO_SETTINGS_MODULE = tests.django.settings

.PHONY: help dev docs translations tests test tox hook pre-commit pre-commit-update Makefile

# Trick to allow passing commands to make
# Use quotes (" ") if command contains flags (-h / --help)
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

# If command doesn't match, do not throw error
%:
	@:

help:
	@echo ""
	@echo "Commands:"
	@echo "  dev                  Serve manual testing server"
	@echo "  docs                 Serve mkdocs for development."
	@echo "  translations         Make and compile translations."
	@echo "  tests                Run all tests with coverage."
	@echo "  test <name>          Run all tests maching the given <name>"
	@echo "  tox                  Run all tests with tox."
	@echo "  hook                 Install pre-commit hook."
	@echo "  pre-commit           Run pre-commit hooks on all files."
	@echo "  pre-commit-update    Update pre-commit hookds."
	@echo "  mypy                 Run mypy on all files."

dev:
	@poetry run python manage.py runserver localhost:8000

docs:
	@poetry run mkdocs serve -a localhost:8080

translations:
	@echo ""
	@echo Making translations...
	@poetry run python manage.py makemessages -l fi --ignore=.venv/* --ignore=.tox/*
	@echo ""
	@echo Compiling...
	@poetry run python manage.py compilemessages --ignore=.venv/* --ignore=.tox/*
	@echo ""
	@echo Done!

tests:
	@poetry run coverage run -m pytest -vv -s --log-cli-level=INFO

test:
	@poetry run pytest -s -vv --log-cli-level=INFO -k $(call args, "")

tox:
	@poetry run tox

hook:
	@poetry run pre-commit install

pre-commit:
	@poetry run pre-commit run --all-files

pre-commit-update:
	@poetry run pre-commit autoupdate

mypy:
	@poetry run mypy admin_data_views/
