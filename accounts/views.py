# accounts/views.py

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response

from .models import Question, Answer, Profile
from .serializers import UserSerializer, QuestionSerializer, AnswerSubmissionSerializer

class UserCreateView(generics.CreateAPIView):
    """
    Endpoint para registrar um novo usuário no sistema.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class QuestionListView(generics.ListAPIView):
    """
    Endpoint para listar todas as perguntas do questionário Big Five.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmitAnswersView(views.APIView):
    """
    Recebe e processa as respostas do questionário de personalidade de um usuário.
    Calcula os scores do Big Five e os salva no perfil do usuário.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnswerSubmissionSerializer

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers_data = serializer.validated_data['answers']
        
        # --- CORREÇÃO 1 ---
        # Acessa o ID da questão através do dicionário aninhado
        question_ids = [answer['question']['id'] for answer in answers_data]
        
        questions_map = {q.id: q for q in Question.objects.filter(id__in=question_ids)}

        if len(questions_map) != len(answers_data):
            return Response({"error": "Uma ou mais questões enviadas são inválidas."}, status=status.HTTP_400_BAD_REQUEST)

        scores = {
            'openness': 0.0, 'conscientiousness': 0.0, 'extraversion': 0.0,
            'agreeableness': 0.0, 'neuroticism': 0.0,
        }

        for answer in answers_data:
            # --- CORREÇÃO 2 ---
            question = questions_map[answer['question']['id']]
            scores[question.attribute] += answer['selected_value']

        try:
            with transaction.atomic():
                for answer_data in answers_data:
                    Answer.objects.update_or_create(
                        profile=profile,
                        # --- CORREÇÃO 3 ---
                        question_id=answer_data['question']['id'],
                        defaults={'selected_value': answer_data['selected_value']}
                    )

                profile.openness = scores['openness']
                profile.conscientiousness = scores['conscientiousness']
                profile.extraversion = scores['extraversion']
                profile.agreeableness = scores['agreeableness']
                profile.neuroticism = scores['neuroticism']
                profile.save()

        except Exception as e:
            print(f"Erro ao salvar respostas e perfil: {e}")
            return Response(
                {"error": "Ocorreu um erro ao processar suas respostas."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            "message": "Respostas computadas com sucesso!",
            "scores": scores
        }, status=status.HTTP_200_OK)