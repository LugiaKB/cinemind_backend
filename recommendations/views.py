import json
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from concurrent.futures import ThreadPoolExecutor

from .serializers import SetFavoriteGenresSerializer, GenerateMoodRecommendationsSerializer, RecommendationItemSerializer, GenreSerializer, RecommendationSetSerializer, ProfileGenreSerializer

# Modelos
from .models import (
    Genre, RecommendationSet, ProfileGenre, Mood, RecommendationItem, BlacklistedMovie
)
# Integrações
from integrations.gemini.service import GeminiService
from integrations.gemini.types import Input as GeminiInput, BlacklistedMovieInput
from integrations.tmdb.service import TMDbService

# --- VIEWS RESTAURADAS ---

class GenreListView(generics.ListAPIView):
    """
    Endpoint para listar todos os géneros de filmes disponíveis.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActiveRecommendationSetView(generics.RetrieveAPIView):
    """
    Endpoint para buscar o conjunto de recomendações ativo do utilizador.
    """
    serializer_class = RecommendationSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return RecommendationSet.objects.prefetch_related('items').filter(user=self.request.user, is_active=True).last()

class SetFavoriteGenresView(views.APIView):
    """
    Define os géneros favoritos de um utilizador.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SetFavoriteGenresSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        genre_ids = serializer.validated_data['genre_ids']
        profile = request.user.profile

        valid_genres = Genre.objects.filter(id__in=genre_ids)
        if len(valid_genres) != len(genre_ids):
            return Response({"error": "Um ou mais IDs de género são inválidos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                ProfileGenre.objects.filter(profile=profile).delete()
                profile_genres_to_create = [
                    ProfileGenre(profile=profile, genre=genre) for genre in valid_genres
                ]
                ProfileGenre.objects.bulk_create(profile_genres_to_create)
        except Exception as e:
            print(f"Erro ao salvar géneros favoritos: {e}")
            return Response({"error": "Ocorreu um erro ao salvar as suas preferências."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = ProfileGenreSerializer(ProfileGenre.objects.filter(profile=profile), many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CreateRecommendationSetView(generics.CreateAPIView):
    """
    Cria um novo conjunto de recomendações vazio e ativo.
    """
    serializer_class = RecommendationSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        RecommendationSet.objects.filter(user=user, is_active=True).update(is_active=False)
        serializer.save(user=user, is_active=True)

# --- VIEW PRINCIPAL DE ALTA PERFORMANCE ---

class GenerateMoodRecommendationsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=GenerateMoodRecommendationsSerializer,
        responses={201: RecommendationItemSerializer(many=True)},
        description="Gera 5 recomendações para o humor fornecido, usando uma abordagem híbrida de IA e busca direta."
    )
    def post(self, request, set_id, *args, **kwargs):
        serializer = GenerateMoodRecommendationsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mood_id = serializer.validated_data['mood_id']
        user = request.user

        try:
            recommendation_set = RecommendationSet.objects.get(id=set_id, user=user, is_active=True)
            mood = Mood.objects.get(id=mood_id)
        except (RecommendationSet.DoesNotExist, Mood.DoesNotExist):
            return Response({"error": "ID de Set ou Mood inválido."}, status=status.HTTP_404_NOT_FOUND)

        profile = user.profile
        favorite_genres = [pg.genre.name for pg in ProfileGenre.objects.filter(profile=profile)]
        if not favorite_genres:
            return Response({"error": "Géneros favoritos não definidos."}, status=status.HTTP_400_BAD_REQUEST)

        personality_scores = {
            "openness": profile.openness, "conscientiousness": profile.conscientiousness,
            "extraversion": profile.extraversion, "agreeableness": profile.agreeableness,
            "neuroticism": profile.neuroticism,
        }
        
        blacklisted_movies = BlacklistedMovie.objects.filter(user=user)
        blacklist_input = [BlacklistedMovieInput(title=movie.title) for movie in blacklisted_movies]
        blacklist_titles = {movie.title.lower() for movie in blacklisted_movies}

        gemini_input = GeminiInput(
            preferences=favorite_genres,
            score=personality_scores,
            blacklist=blacklist_input,
            target_mood=mood.name
        )

        gemini_service = GeminiService()
        search_params = gemini_service.get_search_parameters(gemini_input)
        if not search_params:
            return Response({"error": "Não foi possível traduzir o perfil em parâmetros de busca."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        tmdb_service = TMDbService()
        genre_map = tmdb_service.get_genre_map()
        genre_ids = [genre_map[name] for name in search_params.genres if name in genre_map]
        keyword_ids = tmdb_service.get_keyword_ids(search_params.keywords)
        
        if not genre_ids and not keyword_ids:
             return Response({"error": "Não foi possível encontrar critérios de busca válidos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        candidate_movies = tmdb_service.discover_movies(genre_ids, keyword_ids)

        final_movies = []
        for movie in candidate_movies:
            if movie.get('title', '').lower() not in blacklist_titles:
                final_movies.append(movie)
            if len(final_movies) == 5:
                break
        
        if not final_movies:
            return Response({"error": "Nenhum filme encontrado para os critérios. Tente novamente."}, status=status.HTTP_404_NOT_FOUND)

        with ThreadPoolExecutor(max_workers=len(final_movies)) as executor:
            poster_urls = list(executor.map(
                lambda movie: tmdb_service.get_poster_url(title=movie.get('title', ''), year=int(movie.get('release_date', '0000').split('-')[0])),
                final_movies
            ))

        items_to_create = []
        for i, movie_data in enumerate(final_movies):
            items_to_create.append(
                RecommendationItem(
                    recommendation_set=recommendation_set,
                    mood=mood,
                    external_id=f"tmdb:{movie_data.get('id')}",
                    title=movie_data.get('title', 'Título Desconhecido'),
                    rank=i + 1,
                    thumbnail_url=poster_urls[i],
                    movie_metadata=json.dumps(movie_data)
                )
            )
        
        if items_to_create:
            created_items = RecommendationItem.objects.bulk_create(items_to_create)

        response_serializer = RecommendationItemSerializer(created_items, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
