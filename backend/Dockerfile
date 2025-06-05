FROM python:3.11.3-alpine3.18
LABEL maintainer="seuemail@exemplo.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    build-base \
    linux-headers \
    netcat-openbsd

# Copia o código para o container
COPY . /backend
WORKDIR /backend

# Instala dependências do Python
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Cria diretórios e ajusta permissões
RUN mkdir -p /backend/data/web/static && \
    mkdir -p /backend/data/web/media && \
    chmod -R 775 /backend/data/web/static && \
    chmod -R 775 /backend/data/web/media && \
    chmod -R +x /backend/scripts

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PATH="/venv/bin:$PATH"

CMD ["/entrypoint.sh"]
