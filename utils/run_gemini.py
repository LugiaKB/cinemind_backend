import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")


from integrations.gemini.service import GeminiService
from integrations.gemini.types import Input


gemini_service = GeminiService()


recommendations = gemini_service.get_recommendations(
    Input(
        name="Alice",
        preferences=["Ação", "Ficção Científica"],
        personality=["Curiosa", "Aventureira"],
        current_vibe="Depressiva",
    )
)

if recommendations:
    for movie in recommendations.movies:
        print(f"Título: {movie.title}")
        print(f"Sinopse: {movie.synopsis}")
        print(f"Motivo da Recomendação: {movie.reason_for_recommendation}")
        print(f"Tags: {', '.join(movie.tags)}")
        print("-" * 40)
