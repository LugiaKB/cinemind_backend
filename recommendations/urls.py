# recommendations/urls.py

from django.urls import path
# Adicione a nova view
from .views import GenreListView, ActiveRecommendationSetView, SetFavoriteGenresView, GenerateRecommendationsView

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('active-set/', ActiveRecommendationSetView.as_view(), name='active-recommendation-set'),
    path('genres/set-favorites/', SetFavoriteGenresView.as_view(), name='set-favorite-genres'),

    # --- NOVA ROTA PRINCIPAL ---
    path('generate/', GenerateRecommendationsView.as_view(), name='generate-recommendations'),
]