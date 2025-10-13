# integrations/tmdb/service.py

from typing import Optional
from .client import TMDbClient

class TMDbService:
    """
    Serviço de alto nível para buscar metadados de filmes no TMDb.
    """
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    def __init__(self):
        self.client = TMDbClient()

    def get_poster_url(self, title: str, year: int) -> Optional[str]:
        """
        Busca um filme e retorna a URL completa do seu pôster, se encontrado.
        """
        data = self.client.search_movie(title=title, year=year)

        if data and data.get("results"):
            # Pega o primeiro resultado, que geralmente é o mais relevante
            movie_data = data["results"][0]
            poster_path = movie_data.get("poster_path")
            
            if poster_path:
                return f"{self.IMAGE_BASE_URL}{poster_path}"
        
        return None