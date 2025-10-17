"""
WSGI config for cinemind project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# cinemind/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

# --- LINHA CORRIGIDA ---
# Aponta explicitamente para as configurações de produção
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinemind.settings.production')

application = get_wsgi_application()
