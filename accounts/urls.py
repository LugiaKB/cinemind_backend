# accounts/urls.py

from django.urls import path
# --- A LINHA ABAIXO É A CORREÇÃO ---
from .views import UserCreateView, QuestionListView, SubmitAnswersView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Rotas de Autenticação
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Rotas do App
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('answers/submit/', SubmitAnswersView.as_view(), name='submit-answers'),

    
]
