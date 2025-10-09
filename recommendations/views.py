# recommendations/views.py

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Genre, RecommendationSet, ProfileGenre, Mood, RecommendationItem
from .serializers import GenreSerializer, RecommendationSetSerializer, ProfileGenreSerializer
# --- NOVAS IMPORTAÇÕES (AQUI ESTÁ A CORREÇÃO) ---
from integrations.gemini.service import GeminiService
from integrations.gemini.types import Input as GeminiInput
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
    Ele coleta o perfil do usuário (personalidade + gêneros), chama a IA do Gemini,
    salva os resultados e retorna os 15 filmes recomendados. Requer autenticação.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        
        # 1. Coletar dados do perfil
        favorite_genres = [pg.genre.name for pg in ProfileGenre.objects.filter(profile=profile)]
        if not favorite_genres:
            return Response(
                {"error": "Por favor, defina seus gêneros favoritos primeiro."},
                status=status.HTTP_400_BAD_REQUEST
            )

        personality_traits = self._map_scores_to_traits(profile)

        # O 'current_vibe' foi removido
        gemini_input = GeminiInput(
            name=user.username,
            preferences=favorite_genres,
            personality=personality_traits
        )

        # 2. Chamar o serviço do Gemini
        gemini_service = GeminiService()
        recommendations_output = gemini_service.get_recommendations(gemini_input)

        if not recommendations_output or not recommendations_output.recommendations:
            return Response(
                {"error": "Não foi possível gerar recomendações no momento. Tente novamente mais tarde."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 3. Salvar as recomendações no banco de dados
        RecommendationSet.objects.filter(user=user, is_active=True).update(is_active=False)
        new_set = RecommendationSet.objects.create(
            user=user,
            is_active=True,
            input_snapshot=gemini_input.model_dump_json()
        )

        moods_from_db = {mood.name: mood for mood in Mood.objects.all()}
        items_to_create = []

        # Itera sobre a nova estrutura de resposta da IA
        for mood_rec in recommendations_output.recommendations:
            mood_name = mood_rec.mood
            mood_obj = moods_from_db.get(mood_name)

            if not mood_obj:
                print(f"Aviso: Humor '{mood_name}' retornado pela IA não encontrado no banco de dados.")
                continue

            for movie in mood_rec.movies:
                items_to_create.append(
                    RecommendationItem(
                        recommendation_set=new_set,
                        mood=mood_obj,
                        external_id=movie.title, # Provisório
                        title=movie.title,
                        rank=movie.rank,
                        movie_metadata=json.dumps(movie.model_dump())
                    )
                )

        RecommendationItem.objects.bulk_create(items_to_create)

        # 4. Retornar o novo conjunto de recomendações
        serializer = RecommendationSetSerializer(new_set)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _map_scores_to_traits(self, profile):
        traits = []
        if profile.openness > 0: traits.append("Aberto a novas experiências")
        if profile.conscientiousness > 0: traits.append("Organizado e disciplinado")
        if profile.extraversion > 0: traits.append("Extrovertido e sociável")
        if profile.agreeableness > 0: traits.append("Amável e cooperativo")
        if profile.neuroticism > 0: traits.append("Emocionalmente sensível")
        
        if not traits:
            traits.append("Equilibrado")
            
        return traits

    # A função _find_mood_for_movie não é mais necessária aqui e pode ser removida