.DEFAULT_GOAL := help
SHELL := bash

.PHONY : check init help

ALEMBIC_CONFIG = src/configs/alembic.ini

# Запускаем проект
run:
	uv run granian --interface asgi src/app:app

# Проверяем линтером
check:
	@echo Running project linters...
	uv run ruff check src

# Делаем автоформат
format:
	@echo Running project formaters...
	uv run ruff format src

test:
	uv run pytest

check-alembic:
	@command -v alembic >/dev/null 2>&1 || { echo "Alembic is not installed. Run 'make install'."; exit 1; }

revision: check-alembic
	alembic -c $(ALEMBIC_CONFIG) revision -m '$(msg)' --autogenerate

upgrade: check-alembic
	alembic -c $(ALEMBIC_CONFIG) upgrade head

downgrade: check-alembic
	alembic -c $(ALEMBIC_CONFIG) downgrade -1

#
help:
	@ echo '  Использование:'
	@ echo ''
	@ echo '    make <target> [flags...]'
	@ echo ''
	@ echo '  Цели:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?:/{ print "   ", $$1, comment }' $(MAKEFILE_LIST) | column -t -s ':' | sort
	@ echo ''
	@ echo ''
	@ echo '  Обратите внимание:'
	@ echo '      Для запуска необходимы установленные:'
	@ echo '      - uv, granian, ruff'
