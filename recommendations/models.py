# recommendations/models.py

import uuid
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile # Importa o Profile da outra app

class Genre(models.Model):
    """
    Catálogo de gêneros cinematográficos.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ProfileGenre(models.Model):
    """
    Tabela de junção para a relação Muitos-para-Muitos entre Profile e Genre.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'genre')

    def __str__(self):
        return f"{self.profile.user.username} - {self.genre.name}"

class Mood(models.Model):
    """
    Catálogo dos humores usados para categorizar recomendações.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SubMood(models.Model):
    """
    Subcategoria opcional para um humor principal.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='submoods')
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.mood.name} - {self.name}"

class RecommendationSet(models.Model):
    """
    Agrupa um lote de recomendações geradas em uma única chamada à API.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_sets')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    input_snapshot = models.TextField(help_text="Snapshot serializado do perfil (JSON string)")

    def __str__(self):
        return f"Conjunto de Recomendações para {self.user.username} em {self.created_at}"

class RecommendationItem(models.Model):
    """
    Um único filme dentro de um RecommendationSet.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recommendation_set = models.ForeignKey(RecommendationSet, on_delete=models.CASCADE, related_name='items')
    mood = models.ForeignKey(Mood, on_delete=models.PROTECT, related_name='recommendations')
    external_id = models.CharField(max_length=100, help_text="ID do filme vindo da API externa")
    title = models.CharField(max_length=255)
    rank = models.PositiveSmallIntegerField(help_text="Posição (1, 2, ou 3) do filme dentro do seu humor")
    # --- CAMPO ADICIONADO ---
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL do pôster do filme")
    movie_metadata = models.TextField(help_text="Metadados serializados (JSON string)")
    relevance_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

class ShownHistory(models.Model):
    """
    Log de filmes que foram efetivamente exibidos ao usuário.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    recommendation_item = models.ForeignKey(RecommendationItem, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    mood = models.ForeignKey(Mood, on_delete=models.SET_NULL, null=True)
    shown_at = models.DateTimeField(auto_now_add=True)
    context = models.TextField(blank=True, help_text="Contexto serializado (JSON string)")

    def __str__(self):
        return f"{self.user.username} viu '{self.title}'"

class BlacklistedMovie(models.Model):
    """
    Lista de filmes que um usuário pediu para não ver novamente.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blacklist')
    external_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'external_id')

    def __str__(self):
        return f"'{self.title}' na lista negra de {self.user.username}"