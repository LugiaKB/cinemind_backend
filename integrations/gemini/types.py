# integrations/gemini/types.py

from pydantic import BaseModel, Field
from typing import List, Dict
from typing_extensions import Annotated

# --- CÓDIGO TEMPORÁRIO PARA CORRIGIR O BUILD ---
# As classes 'Movie' e 'MoodRecommendations' foram removidas na nova arquitetura,
# mas um arquivo antigo (provavelmente um teste ou script) ainda está tentando
# importá-las, causando a falha no build. Adicioná-las de volta temporariamente
# permitirá que o build seja concluído. Elas não são usadas pela aplicação principal.

class Movie(BaseModel):
    """
    [CLASSE TEMPORÁRIA/DEPRECIADA]
    Representa um único filme. Usado apenas para compatibilidade durante o build.
    """
    rank: int
    title: str
    year: int
    synopsis: str
    reason_for_recommendation: str
    tags: List[str]

class MoodRecommendations(BaseModel):
    """
    [CLASSE TEMPORÁRIA/DEPRECIADA]
    Representa recomendações para um único humor.
    """
    mood: str
    movies: List[Movie]

# --- FIM DO CÓDIGO TEMPORÁRIO ---


class BlacklistedMovieInput(BaseModel):
    title: str

class Input(BaseModel):
    preferences: List[str] = Field(..., description="Lista de gêneros e temas favoritos do usuário.")
    score: Dict[str, float] = Field(..., description="Dicionário com os scores de personalidade do Big Five.")
    blacklist: List[BlacklistedMovieInput] = Field(default_factory=list, description="Lista de filmes a serem evitados.")
    target_mood: str = Field(..., description="O humor específico para o qual as recomendações devem ser geradas.")

class Output(BaseModel):
    """
    Define a estrutura da resposta da IA, que agora consiste em
    parâmetros de busca otimizados para o TMDb.
    """
    genres: List[str] = Field(..., description="Uma lista de 2 a 3 nomes de gêneros em inglês que melhor se alinham ao perfil e humor do usuário.")
    keywords: List[str] = Field(..., description="Uma lista de 5 a 10 palavras-chave ou temas específicos (em inglês) para refinar a busca de filmes.")
