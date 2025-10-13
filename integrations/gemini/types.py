# integrations/gemini/types.py

from typing import List, Dict
from typing_extensions import Annotated
from pydantic import BaseModel, Field

# --- CLASSE ADICIONADA ---
class BlacklistedMovieInput(BaseModel):
    title: str

class Input(BaseModel):
    """
    Dados de entrada para o prompt do Gemini, sem a emoção do usuário.
    """
    preferences: List[str] = Field(..., description="Lista de gêneros e temas favoritos do usuário.")
    score: Dict[str, float] = Field(..., description="Dicionário com os scores de personalidade do Big Five.")
    blacklist: List[BlacklistedMovieInput] = Field(default_factory=list, description="Lista de filmes a serem evitados.")

class Movie(BaseModel):
    """
    Estrutura de um único filme recomendado, agora com rank.
    """
    rank: Annotated[int, Field(description="Rank of the movie within its mood (1, 2, or 3)")]
    title: Annotated[str, Field(description="Title of the movie to recommend")]
    year: Annotated[int, Field(description="Year the movie was released")]
    synopsis: Annotated[str, Field(description="Short description without spoilers")]
    reason_for_recommendation: Annotated[
        str, Field(description="Reason why the movie was recommended to the user based on their profile")
    ]
    tags: Annotated[List[str], Field(description="Keywords that describe the movie, including its mood")]

class MoodRecommendations(BaseModel):
    """
    Agrupa as recomendações para um único humor.
    """
    mood: Annotated[str, Field(description="The mood category for these recommendations (e.g., Alegria, Tristeza)")]
    movies: Annotated[List[Movie], Field(description="A list of exactly 3 ranked movies for this mood")]

class Output(BaseModel):
    """
    A estrutura de saída completa que a IA deve retornar.
    """
    recommendations: Annotated[
        List[MoodRecommendations], 
        Field(description="A list containing recommendations for each of the 5 required moods.")
    ]