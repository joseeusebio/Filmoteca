DOCKER_COMPOSE = docker compose
MANAGE = $(DOCKER_COMPOSE) exec backend python manage.py
PYTHON = $(DOCKER_COMPOSE) exec backend python
ENV_PATH = backend/dotenv_files/.env
ENV_EXAMPLE_PATH = backend/dotenv_files/.env.example

up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

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
	@if [ ! -f $(ENV_PATH) ]; then \
		cp $(ENV_EXAMPLE_PATH) $(ENV_PATH); \
		echo "✔️ Copiado .env.example para .env"; \
	else \
		echo "ℹ️ .env já existe, mantendo o arquivo atual."; \
	fi
	@SECRET_KEY=`make generate-secret` && \
	if grep -q "^SECRET_KEY=" $(ENV_PATH); then \
		sed -i.bak "s/^SECRET_KEY=.*/SECRET_KEY=$$SECRET_KEY/" $(ENV_PATH); \
	else \
		echo "SECRET_KEY=$$SECRET_KEY" >> $(ENV_PATH); \
	fi && \
	echo "🔐 SECRET_KEY atualizada em $(ENV_PATH)"
	@echo "🚀 Subindo containers com Docker..."
	$(DOCKER_COMPOSE) up -d --build
	@echo "📦 Aplicando migrations..."
	$(MANAGE) migrate
	@echo "🧱 Coletando arquivos estáticos..."
	$(MANAGE) collectstatic --noinput
	@echo "🎬 Carregando dados no banco..."
	make setup-db
	@echo "📋 Logs do backend:"
	$(DOCKER_COMPOSE) logs -f backend
