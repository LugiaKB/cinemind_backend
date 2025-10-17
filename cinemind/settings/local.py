# Arquivo: cinemind/settings/local.py

from cinemind.settings.base import *
import os # Adicione esta linha para ler variáveis de ambiente

# Remova ou comente a configuração antiga do SQLite3
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# --- NOVA CONFIGURAÇÃO PARA O POSTGRESQL ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}