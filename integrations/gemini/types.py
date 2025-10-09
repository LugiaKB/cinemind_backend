# integrations/gemini/types.py

from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel, Field

class Input(BaseModel):
    """
    Dados de entrada para o prompt do Gemini, sem a emoção do usuário.
    """
    name: Annotated[str, Field(description="User's name")]
    preferences: Annotated[List[str], Field(description="User's movie genre preferences")]
    personality: Annotated[List[str], Field(description="User's personality traits based on Big Five")]

class Movie(BaseModel):
    """
    Estrutura de um único filme recomendado, agora com rank.
    """
    rank: Annotated[int, Field(description="Rank of the movie within its mood (1, 2, or 3)")]
    title: Annotated[str, Field(description="Title of the movie to recommend")]
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