.PHONY: up down build logs ps migrate fmt lint test

build:
\tdocker compose build

up:
\tdocker compose up -d

down:
\tdocker compose down

logs:
\tdocker compose logs -f --tail=200

ps:
\tdocker compose ps

migrate:
\tdocker compose exec backend alembic upgrade head

fmt:
\tdocker compose exec backend black src && docker compose exec backend ruff check --fix src

lint:
\tdocker compose exec backend ruff check src && docker compose exec backend mypy src

test:
\tdocker compose exec backend pytest
