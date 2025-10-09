# accounts/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Question, Answer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Cria um perfil automaticamente para cada novo usuário
        Profile.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    # Adicionamos o question_id para que seja write_only
    question_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Answer
        # O profile será pego do usuário logado, não enviado pelo frontend
        fields = ['question_id', 'selected_value']