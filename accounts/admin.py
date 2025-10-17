# accounts/admin.py

from django.contrib import admin
from .models import Profile, Question, Answer

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism', 'updated_at')
    search_fields = ('user__username',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # --- A LINHA ABAIXO FOI MODIFICADA ---
    list_display = ('id', 'description', 'attribute')
    list_filter = ('attribute',)
    search_fields = ('description',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'question', 'selected_value', 'created_at')
    list_filter = ('profile__user__username', 'question__attribute')
    autocomplete_fields = ('profile', 'question')