"""
URL configuration for cinemind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# cinemind/urls.py

from django.contrib import admin
from django.urls import path, include # Adicione 'include'
# --- NOVAS IMPORTAÇÕES ---
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Suas rotas da API que já existem
    path('api/accounts/', include('accounts.urls')),
    path('api/recommendations/', include('recommendations.urls')),

    # --- ROTAS ADICIONAIS PARA DOCUMENTAÇÃO ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Opção 1: Documentação interativa com Swagger UI (mais popular)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Opção 2: Documentação visual com ReDoc (alternativa)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]#