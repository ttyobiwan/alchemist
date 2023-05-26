up:
	docker compose up

build:
	docker compose build

enter:
	docker compose exec fastapi bash

migrate:
	python scripts/migrate.py
