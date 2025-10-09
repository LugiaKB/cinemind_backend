#!/usr/bin/env bash
# exit on error
set -o errexit

# Instala as dependências do Pipfile diretamente no ambiente do sistema
pip install pipenv
pipenv install --system --deploy

# Executa os comandos de build do Django
python manage.py collectstatic --no-input
python manage.py migrate
