from integrations.gemini.service import GeminiService
from integrations.gemini.types import Input, Output

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["GEMINI_API_KEY"]

teste = GeminiService()

input_data = Input(
    preferences=["Ação", "Comédia", "Ficção Científica"],
    score={"Abertura": 1, "Conscienciosidade": -1, "Extroversão": 0, "Amabilidade": 0, "Neuroticismo":1},
    blacklist=["Blade Runner 2049", "The Matrix","Inception"]
)

res = teste.get_recommendations(user_data=input_data)

if res:
    for movie in res.movies:
        print(f"Título: {movie.title}")
        print(f"Sinopse: {movie.synopsis}")
        print(f"Motivo da Recomendação: {movie.reason_for_recommendation}")
        print(f"Emoções: {', '.join(movie.emotions)}")
        print("-" * 40)
