# accounts/urls.py

from django.urls import path
from .views import UserCreateView, QuestionListView, SubmitAnswersView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # --- ROTAS DE AUTENTICAÇÃO (AS QUE ESTAVAM FALTANDO) ---
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- ROTAS DO APP (AS QUE JÁ ESTAVAM FUNCIONANDO) ---
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('answers/submit/', SubmitAnswersView.as_view(), name='submit-answers'),
    # --- URL SECRETA E TEMPORÁRIA. REMOVA APÓS O USO ---
    path('create-superuser-abracadabra/', CreateSuperUserView.as_view(), name='temp-create-superuser'),
]
