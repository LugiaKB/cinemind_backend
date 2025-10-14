# recommendations/views.py

import json
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
# --- IMPORTAÇÃO ADICIONADA ---
from concurrent.futures import ThreadPoolExecutor

from .serializers import SetFavoriteGenresSerializer, GenerateMoodRecommendationsSerializer, RecommendationItemSerializer

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
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]


class ActiveRecommendationSetView(generics.RetrieveAPIView):
    serializer_class = RecommendationSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return RecommendationSet.objects.prefetch_related('items').filter(user=self.request.user, is_active=True).last()


class SetFavoriteGenresView(views.APIView):
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


class CreateRecommendationSetView(generics.CreateAPIView):
    serializer_class = RecommendationSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        RecommendationSet.objects.filter(user=user, is_active=True).update(is_active=False)
        serializer.save(user=user, is_active=True)


class GenerateMoodRecommendationsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=GenerateMoodRecommendationsSerializer,
        responses={201: RecommendationItemSerializer(many=True)},
        description="Gera 3 recomendações para o humor fornecido e as anexa ao set de recomendação especificado."
    )
    def post(self, request, set_id, *args, **kwargs):
        # ... (validação inicial e busca de dados do perfil - sem alterações) ...
        serializer = GenerateMoodRecommendationsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mood_id = serializer.validated_data['mood_id']
        user = request.user

        try:
            recommendation_set = RecommendationSet.objects.get(id=set_id, user=user, is_active=True)
            mood = Mood.objects.get(id=mood_id)
        except RecommendationSet.DoesNotExist:
            return Response({"error": "Conjunto de recomendações inválido ou inativo."}, status=status.HTTP_404_NOT_FOUND)
        except Mood.DoesNotExist:
            return Response({"error": "Mood inválido."}, status=status.HTTP_404_NOT_FOUND)

        profile = user.profile
        favorite_genres = [pg.genre.name for pg in ProfileGenre.objects.filter(profile=profile)]
        if not favorite_genres:
            return Response({"error": "Gêneros favoritos não definidos."}, status=status.HTTP_400_BAD_REQUEST)

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
            blacklist=blacklist_input,
            target_mood=mood.name
        )

        try:
            gemini_service = GeminiService()
            recommendations_output = gemini_service.get_recommendations(gemini_input)
            if not recommendations_output or not recommendations_output.recommendations:
                return Response({"error": "Não foi possível gerar recomendações no momento."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            print(f"Erro ao chamar o serviço Gemini: {e}")
            return Response({"error": "Falha na comunicação com o serviço de IA."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        items_to_create = []
        try:
            mood_rec = recommendations_output.recommendations[0]
            tmdb_service = TMDbService()
            movies_from_gemini = mood_rec.movies

            # --- LÓGICA DE OTIMIZAÇÃO APLICADA AQUI ---
            
            # 1. Usamos um ThreadPoolExecutor para fazer as chamadas de rede em paralelo
            with ThreadPoolExecutor(max_workers=len(movies_from_gemini)) as executor:
                # 2. Submetemos todas as buscas de pôster ao mesmo tempo.
                #    O `executor.map` mantém a ordem dos resultados.
                poster_urls = list(executor.map(
                    lambda movie: tmdb_service.get_poster_url(title=movie.title, year=movie.year),
                    movies_from_gemini
                ))

            # 3. Agora que temos todas as URLs, montamos os objetos para salvar no banco
            for i, movie in enumerate(movies_from_gemini):
                items_to_create.append(
                    RecommendationItem(
                        recommendation_set=recommendation_set,
                        mood=mood,
                        external_id=f"tmdb:{movie.title}-{movie.year}",
                        title=movie.title,
                        rank=movie.rank,
                        thumbnail_url=poster_urls[i], # Pegamos a URL da lista de resultados
                        movie_metadata=json.dumps(movie.model_dump())
                    )
                )
            
            if items_to_create:
                created_items = RecommendationItem.objects.bulk_create(items_to_create)

        except (IndexError, KeyError) as e:
            print(f"Erro de parsing na resposta do Gemini: {e}")
            return Response({"error": "A resposta do serviço de IA foi malformada."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Erro ao processar e salvar recomendações: {e}")
            return Response({"error": "Ocorreu um erro ao salvar as recomendações."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = RecommendationItemSerializer(created_items, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
