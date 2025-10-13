# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Question, Answer

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo User. Usado no registro de novos usuários.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Question. Usado para listar as perguntas.
    """
    class Meta:
        model = Question
        fields = '__all__'


# --- SERIALIZER CORRIGIDO E ADICIONADO ---

class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer para uma única resposta dentro da submissão.
    Valida o question_id e o selected_value.
    """
    question_id = serializers.UUIDField(source='question.id')

    class Meta:
        model = Answer
        fields = ['question_id', 'selected_value']

class AnswerSubmissionSerializer(serializers.Serializer):
    """
    Serializer principal para o endpoint de submissão de respostas.
    Espera um campo 'answers' que é uma lista de objetos de resposta.
    """
    answers = AnswerSerializer(many=True)