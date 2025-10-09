# recommendations/admin.py

from django.contrib import admin
from .models import (
    Genre, 
    ProfileGenre, 
    Mood, 
    SubMood, 
    RecommendationSet, 
    RecommendationItem, 
    ShownHistory, 
    BlacklistedMovie
)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(ProfileGenre)
class ProfileGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'genre', 'created_at')
    autocomplete_fields = ('profile', 'genre')

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(SubMood)
class SubMoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mood')
    list_filter = ('mood',)
    search_fields = ('name',)

@admin.register(RecommendationSet)
class RecommendationSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'is_active')
    list_filter = ('user__username', 'is_active')

@admin.register(RecommendationItem)
class RecommendationItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'mood', 'rank', 'recommendation_set')
    list_filter = ('mood',)
    search_fields = ('title',)

@admin.register(ShownHistory)
class ShownHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'mood', 'shown_at')
    list_filter = ('user__username', 'mood')
    search_fields = ('title',)

@admin.register(BlacklistedMovie)
class BlacklistedMovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    list_filter = ('user__username',)
    search_fields = ('title',)