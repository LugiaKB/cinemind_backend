from functools import lru_cache
from typing import List
# --- IMPORTAÇÃO ADICIONADA ---
from concurrent.futures import ThreadPoolExecutor
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
        """
        Busca o ID para uma lista de palavras-chave em paralelo para otimizar o tempo.
        """
        keyword_ids = []
        
        # Função que será executada em cada thread
        def fetch_keyword_id(keyword):
            try:
                results = self.client.search_keyword(keyword)
                if results:
                    return results[0]['id'] # Retorna o ID do resultado mais relevante
            except Exception as e:
                print(f"Erro ao buscar ID da keyword '{keyword}': {e}")
            return None

        # --- LÓGICA DE OTIMIZAÇÃO APLICADA AQUI ---
        with ThreadPoolExecutor(max_workers=len(keywords)) as executor:
            # Submete todas as buscas de ID ao mesmo tempo
            results = list(executor.map(fetch_keyword_id, keywords))

        # Filtra os resultados que falharam (None)
        keyword_ids = [kid for kid in results if kid is not None]
        return keyword_ids

    def discover_movies(self, genre_ids: List[int], keyword_ids: List[int]) -> List[dict]:
        genres_str = ",".join(map(str, genre_ids))
        keywords_str = "|".join(map(str, keyword_ids))
        
        try:
            return self.client.discover_movies(genres_str, keywords_str)
        except Exception as e:
            print(f"Erro na descoberta de filmes: {e}")
            return []
