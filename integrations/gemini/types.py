# integrations/gemini/types.py

from pydantic import BaseModel, Field
from typing import List, Dict

class BlacklistedMovieInput(BaseModel):
    title: str

class Input(BaseModel):
    preferences: List[str] = Field(..., description="Lista de gêneros e temas favoritos do usuário.")
    score: Dict[str, float] = Field(..., description="Dicionário com os scores de personalidade do Big Five.")
    blacklist: List[BlacklistedMovieInput] = Field(default_factory=list, description="Lista de filmes a serem evitados.")
    target_mood: str = Field(..., description="O humor específico para o qual as recomendações devem ser geradas.")

# --- NOVO MODELO DE SAÍDA ---
class Output(BaseModel):
    """
    Define a estrutura da resposta da IA, que agora consiste em
    parâmetros de busca otimizados para o TMDb.
    """
    genres: List[str] = Field(..., description="Uma lista de 2 a 3 nomes de gêneros em inglês que melhor se alinham ao perfil e humor do usuário.")
    keywords: List[str] = Field(..., description="Uma lista de 5 a 10 palavras-chave ou temas específicos (em inglês) para refinar a busca de filmes.")
