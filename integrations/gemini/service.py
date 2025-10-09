# integrations/gemini/service.py

from typing import Optional
from integrations.gemini.client import GeminiClient
from integrations.gemini.types import Input, Output

class GeminiService:

    BASE_SYSTEM_INSTRUCTION = (
        "Você é um assistente virtual especializado em recomendar filmes de forma personalizada. "
        "Seu objetivo é sugerir opções que estejam alinhadas com os gostos, preferências de gênero e "
        "personalidade do usuário. Sua resposta deve estar EXCLUSIVAMENTE no formato JSON, aderindo ao esquema fornecido."
    )

    RECOMMENDATION_MODEL = "gemini-1.5-flash"

    def __init__(self):
        self.client = GeminiClient(model=self.RECOMMENDATION_MODEL)

    def _build_system_instruction(self) -> str:
        return self.BASE_SYSTEM_INSTRUCTION

    def _build_user_prompt(self, user_data: Input) -> str:
        """
        Constrói o prompt que instrui a IA a retornar 15 filmes
        categorizados e ranqueados pelos 5 humores.
        """
        prompt = f"""
        O usuário forneceu as seguintes informações para uma recomendação:

        - Nome: {user_data.name}
        - Gêneros/Temas Favoritos: {', '.join(user_data.preferences)}
        - Traços de Personalidade: {', '.join(user_data.personality)}

        Sua tarefa é gerar uma lista de 15 recomendações de filmes, divididas em 5 categorias de humor.
        Para CADA UMA das seguintes categorias de humor, você deve fornecer EXATAMENTE 3 filmes, ranqueados de 1 a 3 em ordem de relevância para o perfil do usuário.

        As categorias de humor são:
        1.  **Alegria** (Filmes divertidos, otimistas, comédias)
        2.  **Tristeza** (Filmes emotivos, dramas, que provocam reflexão)
        3.  **Medo/Tensão** (Filmes de suspense, terror, thrillers)
        4.  **Curiosidade** (Filmes de mistério, ficção científica, documentários intrigantes)
        5.  **Relaxamento** (Filmes leves, confortáveis, romances tranquilos)

        Para cada um dos 15 filmes, preencha todos os campos do esquema JSON, incluindo o rank (1, 2 ou 3) e uma justificativa clara (reason_for_recommendation) que conecte o filme ao perfil do usuário.
        A resposta DEVE conter a lista completa com os 5 humores.
        """
        return prompt

    def get_recommendations(self, user_data: Input) -> Optional[Output]:
        system_instruction = self._build_system_instruction()
        user_prompt = self._build_user_prompt(user_data)

        json_schema = Output.model_json_schema()

        raw_response = self.client.generate_json_response(
            prompt=user_prompt,
            system_instruction=system_instruction,
            json_schema=json_schema,
        )

        if raw_response.get("status") == "error":
            print(f"ERRO DE RECOMENDAÇÃO: {raw_response['message']}")
            return None

        try:
            return Output(**raw_response)
        except Exception as e:
            print(f"ERRO DE VALIDAÇÃO DE SAÍDA: O JSON da LLM não se encaixa no modelo Output: {e}")
            return None