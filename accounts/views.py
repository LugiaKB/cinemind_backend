# accounts/views.py

from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from collections import defaultdict
from .serializers import UserSerializer, QuestionSerializer, AnswerSerializer
from .models import Question, Profile, Answer

class UserCreateView(generics.CreateAPIView):
    """
    Endpoint para registrar um novo usuário no sistema.
    Qualquer pessoa pode acessar esta rota para criar uma conta.
    Retorna os dados do usuário criado (sem a senha).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class QuestionListView(generics.ListAPIView):
    """
    Endpoint para listar todas as perguntas do questionário Big Five.
    O usuário deve estar autenticado para acessar esta lista.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmitAnswersView(generics.GenericAPIView):
    """
    Endpoint para o usuário submeter suas respostas ao questionário.
    Recebe uma lista de respostas, recalcula e atualiza os scores de 
    personalidade no perfil do usuário. Requer autenticação.
    """
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        answers_data = request.data.get('answers', [])

        if not isinstance(answers_data, list) or not answers_data:
            return Response(
                {"error": "O campo 'answers' deve ser uma lista e não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deleta respostas antigas para garantir que o cálculo seja sempre sobre o novo conjunto
        Answer.objects.filter(profile=profile).delete()

        # Salva as novas respostas
        for answer_data in answers_data:
            serializer = self.get_serializer(data=answer_data)
            serializer.is_valid(raise_exception=True)
            question = Question.objects.get(id=serializer.validated_data['question_id'])
            Answer.objects.create(
                profile=profile,
                question=question,
                selected_value=serializer.validated_data['selected_value']
            )

        # Calcula os novos scores
        self.calculate_and_update_scores(profile)
        
        return Response({"message": "Respostas enviadas e perfil atualizado com sucesso!"}, status=status.HTTP_200_OK)

    def calculate_and_update_scores(self, profile):
        scores = defaultdict(int)
        answers = Answer.objects.filter(profile=profile).select_related('question')
        
        for answer in answers:
            attribute = answer.question.attribute
            scores[attribute] += answer.selected_value
            
        profile.openness = scores.get('openness', 0.0)
        profile.conscientiousness = scores.get('conscientiousness', 0.0)
        profile.extraversion = scores.get('extraversion', 0.0)
        profile.agreeableness = scores.get('agreeableness', 0.0)
        profile.neuroticism = scores.get('neuroticism', 0.0)
        profile.save()

class CreateSuperUserView(views.APIView):
    """
    UMA VIEW TEMPORÁRIA E INSEGURA. REMOVA IMEDIATAMENTE APÓS O USO.
    Cria um superutilizador com dados diretamente no código.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        
        # --- DEFINA AQUI AS SUAS CREDENCIAIS ---
        username = "cinemind_user"  # Escolha um nome de utilizador
        email = "wnrj@cin.ufpe.br"   # Coloque o seu e-mail
        password = "cinemind" # Escolha uma palavra-passe forte
        # -----------------------------------------

        if User.objects.filter(username=username).exists():
            return Response(
                {"message": f"O utilizador '{username}' já existe. Nenhum utilizador novo foi criado."},
                status=status.HTTP_200_OK
            )
        
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            return Response(
                {"message": f"Superutilizador '{username}' criado com sucesso! POR FAVOR, REMOVA ESTE CÓDIGO AGORA."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"Ocorreu um erro ao criar o superutilizador: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
