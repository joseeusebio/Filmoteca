DOCKER_COMPOSE = docker compose
MANAGE = $(DOCKER_COMPOSE) exec backend python manage.py
PYTHON = $(DOCKER_COMPOSE) exec backend python
ENV_PATH = backend/dotenv_files/.env
ENV_EXAMPLE_PATH = backend/dotenv_files/.env.example

up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

clean:
	@echo "Parando e removendo containers, volumes e dados locais..."
	docker compose down -v
	rm -rf backend/data
	@echo "Limpeza completa do projeto."

shell:
	$(DOCKER_COMPOSE) exec backend sh

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

createsuperuser:
	$(MANAGE) createsuperuser

collectstatic:
	$(MANAGE) collectstatic --noinput

import_movies:
	$(MANAGE) import_movies --path=/backend/data/tmdb-movies.csv --chunk=10000 --estimado=1000000

download-dataset:
	$(PYTHON) scripts/download_dataset.py

setup-db:
	make download-dataset && make import_movies

logs:
	$(DOCKER_COMPOSE) logs -f backend

restart:
	$(DOCKER_COMPOSE) restart backend

generate-secret:
	@python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

init:
	@echo "Subindo containers com Docker..."
	$(DOCKER_COMPOSE) up -d --build

	@echo "Carregando dados no banco..."
	make setup-db


