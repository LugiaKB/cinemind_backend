# recommendations/serializers.py

from rest_framework import serializers
# A linha abaixo é a correção. Adicionamos ProfileGenre aqui.
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
        fields = ['id', 'title', 'rank', 'movie_metadata', 'mood']

class RecommendationSetSerializer(serializers.ModelSerializer):
    items = RecommendationItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = RecommendationSet
        fields = ['id', 'created_at', 'is_active', 'items']

# --- NOVO SERIALIZER (Agora com o import correto) ---
class ProfileGenreSerializer(serializers.ModelSerializer):
    genre_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )

    class Meta:
        model = ProfileGenre
        fields = ('genre_ids',)