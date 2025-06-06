#!/bin/sh

echo "Aguardando o banco de dados ficar disponivel em $POSTGRES_HOST:$POSTGRES_PORT..."

for i in $(seq 1 30); do
  nc -z "$POSTGRES_HOST" "$POSTGRES_PORT" && break
  echo "Tentativa $i: aguardando o PostgreSQL iniciar..."
  sleep 1
done

if ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; then
  echo "Erro: banco de dados não esta acessivel após 30 segundos."
  exit 1
fi

echo "Banco disponivel. Executando migracoes e iniciando o servidor..."

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

gunicorn --bind 0.0.0.0:8005 --timeout 120 filmoteca.wsgi:application
