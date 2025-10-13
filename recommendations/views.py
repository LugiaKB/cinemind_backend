# recommendations/views.py

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Genre, RecommendationSet, ProfileGenre, Mood, RecommendationItem
from .serializers import GenreSerializer, RecommendationSetSerializer, ProfileGenreSerializer
# --- NOVAS IMPORTAÇÕES (AQUI ESTÁ A CORREÇÃO) ---
from integrations.gemini.service import GeminiService
from integrations.gemini.types import Input as GeminiInput
from integrations.tmdb import TMDbService
import json

class GenreListView(generics.ListAPIView):
    """
    Endpoint para listar todos os gêneros de filmes disponíveis no banco de dados.
    O usuário pode usar esta lista para escolher seus favoritos. Requer autenticação.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]


class ActiveRecommendationSetView(generics.RetrieveAPIView):
    """
    Endpoint para buscar o conjunto de recomendações mais recente e ativo do usuário.
    O frontend deve usar esta rota para exibir os filmes na tela inicial.
    Requer autenticação.
    """
    serializer_class = RecommendationSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return RecommendationSet.objects.filter(user=self.request.user, is_active=True).last()


class SetFavoriteGenresView(generics.GenericAPIView):
    """
    Endpoint para o usuário definir ou atualizar sua lista de gêneros favoritos.
    Recebe uma lista de UUIDs de gêneros. As preferências antigas são substituídas.
    Requer autenticação.
    """
    serializer_class = ProfileGenreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        genre_ids = serializer.validated_data['genre_ids']

        ProfileGenre.objects.filter(profile=profile).delete()

        genres_to_add = []
        for genre_id in genre_ids:
            if Genre.objects.filter(id=genre_id).exists():
                genres_to_add.append(ProfileGenre(profile=profile, genre_id=genre_id))
        
        ProfileGenre.objects.bulk_create(genres_to_add)

        return Response({"message": "Gêneros favoritos atualizados com sucesso!"}, status=status.HTTP_200_OK)


# --- VIEW PRINCIPAL (AGORA COM A IMPORTAÇÃO CORRETA) ---
class GenerateRecommendationsView(views.APIView):
    """
    [PRINCIPAL] Endpoint que gera um novo conjunto de recomendações personalizadas.
    Coleta o perfil, chama a IA, enriquece os dados com a API do TMDb e salva o resultado.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        
        # 1. Coletar dados do perfil (sem alterações)
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

        # 2. Chamar o serviço do Gemini (sem alterações)
        gemini_service = GeminiService()
        recommendations_output = gemini_service.get_recommendations(gemini_input)

        if not recommendations_output or not recommendations_output.recommendations:
            return Response({"error": "Não foi possível gerar recomendações no momento."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 3. Processar e Salvar Recomendações (COM A NOVA LÓGICA)
        try:
            # Desativa o set antigo e cria um novo
            RecommendationSet.objects.filter(user=user, is_active=True).update(is_active=False)
            new_set = RecommendationSet.objects.create(user=user, is_active=True, input_snapshot=gemini_input.model_dump_json())

            moods_from_db = {mood.name: mood for mood in Mood.objects.all()}
            items_to_create = []
            
            # Instancia o serviço do TMDb uma única vez
            tmdb_service = TMDbService()

            for mood_rec in recommendations_output.recommendations:
                mood_obj = moods_from_db.get(mood_rec.mood)
                if not mood_obj: continue

                for movie in mood_rec.movies:
                    # --- LÓGICA DE ENRIQUECIMENTO ---
                    thumbnail_url = tmdb_service.get_poster_url(title=movie.title, year=movie.year)
                    # --------------------------------

                    items_to_create.append(
                        RecommendationItem(
                            recommendation_set=new_set,
                            mood=mood_obj,
                            external_id=f"tmdb:{movie.title}-{movie.year}", # Usando um ID mais robusto
                            title=movie.title,
                            rank=movie.rank,
                            thumbnail_url=thumbnail_url,  # Salva a URL encontrada
                            movie_metadata=json.dumps(movie.model_dump())
                        )
                    )

            RecommendationItem.objects.bulk_create(items_to_create)

        except Exception as e:
            # Se algo der errado (ex: TMDb fora do ar), retorna um erro sem quebrar o app
            print(f"Erro ao processar e salvar recomendações: {e}")
            return Response({"error": "Ocorreu um erro ao salvar as recomendações."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. Retornar o novo conjunto (sem alterações)
        serializer = RecommendationSetSerializer(new_set)
        return Response(serializer.data, status=status.HTTP_201_CREATED)