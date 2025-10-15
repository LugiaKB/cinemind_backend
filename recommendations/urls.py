# recommendations/urls.py

from django.urls import path
from .views import (
    GenreListView,
    ActiveRecommendationSetView,
    SetFavoriteGenresView,
    # --- NOVAS VIEWS ---
    CreateRecommendationSetView,
    GenerateMoodRecommendationsView,
)

urlpatterns = [
    # Rotas de setup
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/set-favorites/', SetFavoriteGenresView.as_view(), name='set-favorite-genres'),
    path('genres/check-favorites/', CheckFavoriteGenresView.as_view(), name='check-favorite-genres'), # Adicione esta linha
    
    # Rota para buscar o set ativo (continua útil para o frontend)
    path('active-set/', ActiveRecommendationSetView.as_view(), name='active-recommendation-set'),

    # --- NOVAS ROTAS PARA O FLUXO DE GERAÇÃO ---
    
    # 1. Cria um "contêiner" de recomendações vazio e ativo
    path('sets/', CreateRecommendationSetView.as_view(), name='create-recommendation-set'),

    # 2. Gera 3 filmes para um humor específico e os adiciona a um set existente
    path('sets/<uuid:set_id>/generate-for-mood/', GenerateMoodRecommendationsView.as_view(), name='generate-mood-recommendations'),
]
