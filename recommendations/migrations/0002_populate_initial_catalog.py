# recommendations/migrations/0002_populate_initial_catalog.py
from django.db import migrations

# --- DADOS INICIAIS ---

GENRES = [
    "Ação", "Aventura", "Animação", "Comédia", "Crime", "Documentário", "Drama",
    "Família", "Fantasia", "História", "Terror", "Música", "Mistério",
    "Romance", "Ficção Científica", "Cinema TV", "Suspense", "Guerra", "Faroeste"
]

MOODS_AND_SUBMOODS = {
    "Alegria": ["Comédia", "Sessão da Tarde", "Sátira", "Humor Ácido", "Comédia Romântica", "Paródia"],
    "Tristeza": ["Drama", "Melancolia", "Reflexão", "Emocionante"],
    "Medo/Tensão": ["Terror", "Suspense", "Thriller Psicológico", "Sobrenatural", "Slasher"],
    "Curiosidade": ["Mistério", "Ficção Científica", "Fantasia", "Documentário", "Investigação"],
    "Relaxamento": ["Conforto", "Romance Leve", "Sessão Pipoca", "Nostalgia", "Feel-good"]
}

# --- FUNÇÃO DE POVOAMENTO ---

def populate_data(apps, schema_editor):
    Genre = apps.get_model('recommendations', 'Genre')
    Mood = apps.get_model('recommendations', 'Mood')
    SubMood = apps.get_model('recommendations', 'SubMood')

    for genre_name in GENRES:
        Genre.objects.get_or_create(name=genre_name)

    for mood_name, submood_list in MOODS_AND_SUBMOODS.items():
        mood_obj, created = Mood.objects.get_or_create(name=mood_name)
        for submood_name in submood_list:
            SubMood.objects.get_or_create(mood=mood_obj, name=submood_name)

# --- CLASSE DA MIGRAÇÃO ---

class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]