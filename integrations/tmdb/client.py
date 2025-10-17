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
        Busca por um filme específico pelo título e ano, com fallback para uma busca mais ampla.
        """
        search_url = f"{self.BASE_URL}/search/movie"
        
        # Tentativa 1: Busca específica com título e ano
        params_with_year = {
            "api_key": self.api_key,
            "query": title,
            "language": "pt-BR",
            "year": year,
            "include_adult": "false"
        }
        
        try:
            response = requests.get(search_url, params=params_with_year, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                return data
        except requests.RequestException:
            # Ignora erros para tentar a busca mais ampla
            pass

        # Tentativa 2: Busca ampla apenas com o título, e depois filtra pelo ano
        params_without_year = {
            "api_key": self.api_key,
            "query": title,
            "language": "pt-BR",
            "include_adult": "false"
        }

        try:
            response = requests.get(search_url, params=params_without_year, timeout=5)
            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                return None

            # Filtra os resultados para encontrar a melhor correspondência pelo ano
            best_match = None
            for movie in data["results"]:
                release_date = movie.get("release_date")
                if release_date and str(year) in release_date:
                    best_match = movie
                    break
            
            # Se não encontrar uma correspondência exata do ano, retorna o primeiro resultado
            if not best_match and data["results"]:
                best_match = data["results"][0]

            if best_match:
                return {"results": [best_match]}
            
            return None

        except requests.RequestException as e:
            print(f"Erro ao chamar a API do TMDb para '{title}': {e}")
            return None
