# accounts/models.py

import uuid
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Perfil estendido do usuário, contendo os scores de personalidade.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Scores do Big Five
    openness = models.FloatField(default=0.0, help_text="Abertura a novas experiências")
    conscientiousness = models.FloatField(default=0.0, help_text="Nível de organização e disciplina")
    extraversion = models.FloatField(default=0.0, help_text="Nível de sociabilidade")
    agreeableness = models.FloatField(default=0.0, help_text="Nível de empatia e cooperação")
    neuroticism = models.FloatField(default=0.0, help_text="Instabilidade emocional")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Question(models.Model):
    """
    Armazena uma pergunta do questionário Big Five.
    """
    class PersonalityAttribute(models.TextChoices):
        OPENNESS = 'openness', 'Abertura'
        CONSCIENTIOUSNESS = 'conscientiousness', 'Conscienciosidade'
        EXTRAVERSION = 'extraversion', 'Extroversão'
        AGREEABLENESS = 'agreeableness', 'Amabilidade'
        NEUROTICISM = 'neuroticism', 'Neuroticismo'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    attribute = models.CharField(
        max_length=20,
        choices=PersonalityAttribute.choices,
        help_text="O traço de personalidade que esta pergunta avalia"
    )
    
    # Alternativas e seus respectivos valores
    first_alternative = models.CharField(max_length=255)
    first_alternative_value = models.IntegerField()
    
    second_alternative = models.CharField(max_length=255)
    second_alternative_value = models.IntegerField()
    
    third_alternative = models.CharField(max_length=255)
    third_alternative_value = models.IntegerField()

    def __str__(self):
        return f"({self.get_attribute_display()}) {self.description[:50]}..."

class Answer(models.Model):
    """
    Registra a resposta de um usuário a uma pergunta específica.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um usuário só pode responder a uma pergunta uma vez.
        unique_together = ('profile', 'question')

    def __str__(self):
        return f"Resposta de {self.profile.user.username} para a questão {self.question.id}"