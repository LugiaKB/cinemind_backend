# integrations/tmdb/client.py

import os
import requests
from typing import Optional, Dict, Any

class TMDbClient:
    """
    Cliente de baixo nível para interagir com a API do The Movie Database (TMDb).
    """
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB_API_KEY não encontrado nas variáveis de ambiente.")

    def search_movie(self, title: str, year: int) -> Optional[Dict[str, Any]]:
        """
        Busca por um filme específico pelo título e ano.
        """
        search_url = f"{self.BASE_URL}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": title,
            "year": year,
            "language": "pt-BR"
        }
        try:
            response = requests.get(search_url, params=params, timeout=5)
            response.raise_for_status() # Lança um erro para status HTTP 4xx/5xx
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao chamar a API do TMDb para '{title}': {e}")
            return None