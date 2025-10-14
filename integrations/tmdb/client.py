import os
import requests
from typing import List, Optional

class TMDbClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("A variável de ambiente TMDB_API_KEY não está definida.")

    def _make_request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Função auxiliar para fazer requisições à API do TMDb.
        """
        if params is None:
            params = {}
        
        # Adiciona a chave da API e a linguagem a todas as requisições
        params['api_key'] = self.api_key
        params['language'] = 'pt-BR'
        
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lança um erro para status HTTP 4xx/5xx
        return response.json()

    def search_movie(self, title: str, year: Optional[int] = None) -> List[dict]:
        """
        Busca por um filme pelo título e, opcionalmente, pelo ano.
        """
        params = {"query": title}
        if year:
            params["year"] = year
        
        data = self._make_request("/search/movie", params)
        return data.get("results", [])

    # --- FUNÇÃO ADICIONADA ---
    def get_genres(self) -> dict:
        """
        Busca a lista oficial de géneros de filmes do TMDb.
        """
        return self._make_request("/genre/movie/list")

    # --- FUNÇÃO ADICIONADA ---
    def search_keyword(self, keyword: str) -> List[dict]:
        """
        Busca por uma palavra-chave para obter o seu ID.
        """
        params = {"query": keyword}
        data = self._make_request("/search/keyword", params)
        return data.get("results", [])

    # --- FUNÇÃO ADICIONADA ---
    def discover_movies(self, genres_str: str, keywords_str: str) -> List[dict]:
        """
        Descobre filmes com base numa combinação de géneros e palavras-chave.
        """
        params = {
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "include_video": "false",
            "page": 1,
            "with_genres": genres_str,
            "with_keywords": keywords_str
        }
        data = self._make_request("/discover/movie", params)
        return data.get("results", [])
