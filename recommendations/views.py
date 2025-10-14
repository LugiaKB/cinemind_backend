# recommendations/views.py

import json
from django.db import transaction
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .serializers import SetFavoriteGenresSerializer

# Modelos
from .models import (
    Genre, RecommendationSet, ProfileGenre, Mood, RecommendationItem, BlacklistedMovie
)
# Serializers
from .serializers import (
    GenreSerializer, RecommendationSetSerializer, ProfileGenreSerializer
)
# Integrações
from integrations.gemini.service import GeminiService
from integrations.gemini.types import Input as GeminiInput, BlacklistedMovieInput
from integrations.tmdb import TMDbService


class GenreListView(generics.ListAPIView):
    """
    Endpoint para listar todos os gêneros de filmes disponíveis.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]


class ActiveRecommendationSetView(generics.RetrieveAPIView):
    """
    Endpoint para buscar o conjunto de recomendações ativo do usuário.
    """
    serializer_class = RecommendationSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # --- ALTERAÇÃO DE OTIMIZAÇÃO APLICADA AQUI ---
        # Usamos .prefetch_related('items') para buscar todos os itens de recomendação
        # relacionados em uma única consulta extra, evitando o problema "N+1"
        # que causa alto consumo de memória.
        return RecommendationSet.objects.prefetch_related('items').filter(user=self.request.user, is_active=True).last()


class SetFavoriteGenresView(views.APIView):
    """
    Define os gêneros favoritos de um usuário.
    Recebe uma lista de IDs de gênero, apaga os favoritos antigos e cria os novos.
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
            return Response({"error": "Um ou mais IDs de gênero são inválidos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                ProfileGenre.objects.filter(profile=profile).delete()
                profile_genres_to_create = [
                    ProfileGenre(profile=profile, genre=genre) for genre in valid_genres
                ]
                ProfileGenre.objects.bulk_create(profile_genres_to_create)
        except Exception as e:
            print(f"Erro ao salvar gêneros favoritos: {e}")
            return Response({"error": "Ocorreu um erro ao salvar suas preferências."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = ProfileGenreSerializer(ProfileGenre.objects.filter(profile=profile), many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class GenerateRecommendationsView(views.APIView):
    """
    [PRINCIPAL] Gera um novo conjunto de recomendações personalizadas.
    Otimizado para ambientes com pouca memória.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecommendationSetSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        
        # 1. Coletar dados do perfil
        favorite_genres = [pg.genre.name for pg in ProfileGenre.objects.filter(profile=profile)]
        if not favorite_genres:
            return Response({"error": "Por favor, defina seus gêneros favoritos primeiro."}, status=status.HTTP_400_BAD_REQUEST)

        personality_scores = {
            "openness": profile.openness, "conscientiousness": profile.conscientiousness,
            "extraversion": profile.extraversion, "agreeableness": profile.agreeableness,
            "neuroticism": profile.neuroticism,
        }
        
        blacklist_movies = BlacklistedMovie.objects.filter(user=user)
        blacklist_input = [BlacklistedMovieInput(title=movie.title) for movie in blacklist_movies]

        gemini_input = GeminiInput(
            preferences=favorite_genres,
            score=personality_scores,
            blacklist=blacklist_input
        )

        # 2. Chamar o serviço do Gemini
        gemini_service = GeminiService()
        recommendations_output = gemini_service.get_recommendations(gemini_input)

        if not recommendations_output or not recommendations_output.recommendations:
            return Response({"error": "Não foi possível gerar recomendações no momento."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 3. Processar e Salvar Recomendações
        try:
            with transaction.atomic():
                RecommendationSet.objects.filter(user=user, is_active=True).update(is_active=False)
                new_set = RecommendationSet.objects.create(user=user, is_active=True, input_snapshot=gemini_input.model_dump_json())

                moods_from_db = {mood.name: mood for mood in Mood.objects.all()}
                tmdb_service = TMDbService()

                for mood_rec in recommendations_output.recommendations:
                    mood_obj = moods_from_db.get(mood_rec.mood)
                    if not mood_obj: continue

                    for movie in mood_rec.movies:
                        thumbnail_url = tmdb_service.get_poster_url(title=movie.title, year=movie.year)
                        
                        RecommendationItem.objects.create(
                            recommendation_set=new_set,
                            mood=mood_obj,
                            external_id=f"tmdb:{movie.title}-{movie.year}",
                            title=movie.title,
                            rank=movie.rank,
                            thumbnail_url=thumbnail_url,
                            movie_metadata=json.dumps(movie.model_dump())
                        )

        except Exception as e:
            print(f"Erro ao processar e salvar recomendações: {e}")
            return Response({"error": "Ocorreu um erro ao salvar as recomendações."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. Retornar o novo conjunto
        serializer = RecommendationSetSerializer(new_set)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
