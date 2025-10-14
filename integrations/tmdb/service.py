from functools import lru_cache
from typing import List, Optional
from integrations.tmdb.client import TMDbClient

class TMDbService:
    def __init__(self):
        self.client = TMDbClient()

    def get_poster_url(self, title: str, year: int) -> str:
        try:
            results = self.client.search_movie(title, year)
            if results and results[0].get('poster_path'):
                return f"https://image.tmdb.org/t/p/w500{results[0]['poster_path']}"
        except Exception as e:
            print(f"Erro ao buscar pôster para '{title}': {e}")
        return "https://via.placeholder.com/500x750.png?text=No+Image"

    @lru_cache(maxsize=1)
    def get_genre_map(self) -> dict:
        try:
            data = self.client.get_genres()
            return {genre['name']: genre['id'] for genre in data['genres']}
        except Exception as e:
            print(f"Erro ao buscar mapa de géneros: {e}")
            return {}

    def get_keyword_ids(self, keywords: List[str]) -> List[int]:
        keyword_ids = []
        for keyword in keywords:
            try:
                results = self.client.search_keyword(keyword)
                if results:
                    keyword_ids.append(results[0]['id'])
            except Exception as e:
                print(f"Erro ao buscar ID da keyword '{keyword}': {e}")
        return keyword_ids

    def discover_movies(self, genre_ids: List[int], keyword_ids: List[int]) -> List[dict]:
        """
        Busca filmes no TMDb usando uma combinação de IDs de género e palavra-chave.
        """
        genres_str = ",".join(map(str, genre_ids))
        
        # --- CORREÇÃO APLICADA AQUI ---
        # Para keywords, a vírgula (,) funciona como um 'AND' (muito restritivo).
        # Usaremos o pipe (|) para funcionar como um 'OR', o que nos dará mais resultados.
        keywords_str = "|".join(map(str, keyword_ids))
        
        try:
            return self.client.discover_movies(genres_str, keywords_str)
        except Exception as e:
            print(f"Erro na descoberta de filmes: {e}")
            return []
