# integrations/gemini/service.py

from typing import Optional
from integrations.gemini.client import GeminiClient
from integrations.gemini.types import Input, Output

class GeminiService:
    RECOMMENDATION_MODEL = "gemini-1.5-flash"

    def __init__(self):
        self.client = GeminiClient(model=self.RECOMMENDATION_MODEL)

    def _build_system_instruction(self) -> str:
        # A instrução de personalidade continua a mesma
        return (
            "Você é um assistente de recomendação de filmes altamente especializado. "
            "Sua função é analisar o perfil psicológico e de gostos de um usuário para traduzi-lo "
            "em parâmetros de busca eficazes para uma API de filmes como o TMDb. "
            "Sua resposta deve estar EXCLUSIVAMENTE no formato JSON, aderindo ao esquema fornecido.\n\n"
            "**Guia de Interpretação dos Traços de Personalidade (Big Five/OCEAN):**\n"
            # ... (o resto do guia de personalidade não precisa mudar) ...
            "  - **Score Baixo (Estabilidade Emocional)**: Calma, resiliência. Geralmente são flexíveis e apreciam uma vasta gama de tons emocionais sem se sentirem sobrecarregados.\n\n"
        )

    def _build_user_prompt(self, user_data: Input) -> str:
        personality_scores = "\n".join([f"- {trait}: {score}" for trait, score in user_data.score.items()])
        blacklist_titles = ', '.join([movie.title for movie in user_data.blacklist]) if user_data.blacklist else "Nenhum"

        # --- PROMPT TOTALMENTE REFEITO ---
        return (
            "Analise o perfil de usuário a seguir.\n\n"
            "**Perfil do Usuário:**\n"
            f"- Gêneros/Temas Favoritos: {', '.join(user_data.preferences)}\n"
            f"- Traços de Personalidade (Scores):\n{personality_scores}\n"
            f"- Filmes a Evitar: {blacklist_titles}\n\n"
            "**Sua Tarefa:**\n"
            f"O usuário deseja encontrar filmes que evoquem o sentimento de **'{user_data.target_mood}'**.\n"
            "Com base em todo o perfil do usuário, gere uma lista de **gêneros e palavras-chave em INGLÊS** que seriam mais eficazes para encontrar esses filmes em uma base de dados como o TMDb.\n"
            "Selecione de 2 a 3 gêneros e de 5 a 10 palavras-chave bem específicas. A blacklist deve influenciar na escolha para evitar temas semelhantes."
        )

    def get_search_parameters(self, user_data: Input) -> Optional[Output]:
        system_instruction = self._build_system_instruction()
        user_prompt = self._build_user_prompt(user_data)

        json_schema = Output.model_json_schema()

        raw_response = self.client.generate_json_response(
            prompt=user_prompt,
            system_instruction=system_instruction,
            json_schema=json_schema,
        )

        if raw_response is None:
            print("ERRO DE GERAÇÃO DE PARÂMETROS: A resposta da API foi nula.")
            return None
        
        try:
            return Output(**raw_response)
        except Exception as e:
            print(f"ERRO DE VALIDAÇÃO DE SAÍDA: O JSON da LLM não se encaixa no modelo Output: {e}")
            print(f"JSON Recebido: {raw_response}")
            return None
