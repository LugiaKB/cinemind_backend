#!/usr/bin/env bash
# exit on error
set -o errexit

# Instala as dependências do Pipfile diretamente no ambiente do sistema
pip install pipenv
pipenv install --system --deploy

# Executa os comandos de build do Django
python manage.py collectstatic --no-input
python manage.py migrate
# Popula as perguntas do questionário
python manage.py populate_questions

# Cria o superusuário se as variáveis de ambiente estiverem definidas
if [[ -n "$DJANGO_SUPERUSER_USERNAME" && -n "$DJANGO_SUPERUSER_PASSWORD" && -n "$DJANGO_SUPERUSER_EMAIL" ]]; then
  python manage.py createsuperuser --noinput || true
fi
