# integrations/gemini/types.py

from pydantic import BaseModel, Field
from typing import List, Dict
from typing_extensions import Annotated

class BlacklistedMovieInput(BaseModel):
    title: str

class Input(BaseModel):
    preferences: List[str] = Field(..., description="Lista de gêneros e temas favoritos do usuário.")
    score: Dict[str, float] = Field(..., description="Dicionário com os scores de personalidade do Big Five.")
    blacklist: List[BlacklistedMovieInput] = Field(default_factory=list, description="Lista de filmes a serem evitados.")
    # --- NOVO CAMPO ADICIONADO ---
    target_mood: str = Field(..., description="O humor específico para o qual as recomendações devem ser geradas.")

class Movie(BaseModel):
    # --- DESCRIÇÃO ATUALIZADA ---
    rank: Annotated[int, Field(description="Rank do filme dentro de seu humor (1, 2, ou 3)")]
    title: Annotated[str, Field(description="Título do filme recomendado")]
    year: Annotated[int, Field(description="Ano de lançamento do filme")]
    synopsis: Annotated[str, Field(description="Breve sinopse do filme")]
    reason_for_recommendation: Annotated[
        str, Field(description="Justificativa da recomendação baseada no perfil do usuário")
    ]
    tags: Annotated[List[str], Field(description="Palavras-chave que descrevem o filme")]

class MoodRecommendations(BaseModel):
    mood: Annotated[str, Field(description="A categoria de humor para estas recomendações")]
    # --- DESCRIÇÃO ATUALIZADA ---
    movies: Annotated[List[Movie], Field(description="Uma lista de exatamente 3 filmes ranqueados para este humor")]

class Output(BaseModel):
    # O output agora é uma única recomendação de humor, não mais uma lista
    recommendations: Annotated[
        MoodRecommendations, 
        Field(description="Recomendações para o humor solicitado.")
    ]
