#!/bin/sh

echo "Aguardando o banco de dados ficar disponível em $POSTGRES_HOST:$POSTGRES_PORT..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "Banco disponível. Executando migrações e iniciando o servidor..."

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

gunicorn --bind 0.0.0.0:8005 --timeout 120 filmoteca.wsgi:application
