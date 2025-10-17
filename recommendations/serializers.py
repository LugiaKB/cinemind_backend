# recommendations/serializers.py

from rest_framework import serializers
from .models import Genre, RecommendationSet, RecommendationItem, Mood, ProfileGenre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = '__all__'

class RecommendationItemSerializer(serializers.ModelSerializer):
    mood = MoodSerializer(read_only=True)
    
    class Meta:
        model = RecommendationItem
        # Adicionado thumbnail_url para ser retornado na API
        fields = ['id', 'title', 'rank', 'thumbnail_url', 'movie_metadata', 'mood']

class RecommendationSetSerializer(serializers.ModelSerializer):
    items = RecommendationItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = RecommendationSet
        fields = ['id', 'created_at', 'is_active', 'items']

class ProfileGenreSerializer(serializers.ModelSerializer):
    genre_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )

    class Meta:
        model = ProfileGenre
        fields = ('genre_ids',)

class SetFavoriteGenresSerializer(serializers.Serializer):
    genre_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        help_text="Lista de IDs dos gêneros favoritos."
    )

# --- NOVO SERIALIZER ADICIONADO ---
class GenerateMoodRecommendationsSerializer(serializers.Serializer):
    """
    Serializer para validar o corpo da requisição da geração por humor.
    Espera o ID do humor que o usuário selecionou.
    """
    mood_id = serializers.UUIDField(help_text="O ID do Mood para o qual gerar recomendações.")
