from typing import Optional
from integrations.gemini.client import GeminiClient
from integrations.gemini.types import Input, Output


class GeminiService:

    BASE_SYSTEM_INSTRUCTION = (
        "Você é um assistente virtual especializado em recomendar filmes de forma personalizada. "
        "Seu objetivo é sugerir opções que estejam alinhadas com os gostos, preferências de gênero, "
        "personalidade e estado emocional atual do usuário. "
        "Sua resposta deve estar EXCLUSIVAMENTE no formato JSON, aderindo ao esquema fornecido."
    )

    RECOMMENDATION_MODEL = "gemini-2.5-flash"

    def __init__(self):
        self.client = GeminiClient(model=self.RECOMMENDATION_MODEL)

    def _build_system_instruction(self) -> str:
        return self.BASE_SYSTEM_INSTRUCTION

    def _build_user_prompt(self, user_data: Input) -> str:
        prompt = f"""
        O usuário forneceu as seguintes informações para uma recomendação:
        
        - Nome: {user_data.name}
        - Gêneros/Temas Favoritos: {', '.join(user_data.preferences)}
        - Traços de Personalidade: {', '.join(user_data.personality)}
        - Sentimento Atual: {user_data.current_vibe}
        
        Sua tarefa é recomendar 1 ou mais filmes que melhor combinem com este perfil.
        
        As recomendações devem levar em conta:
        1. Afinidade com os gêneros informados.
        2. Coerência com os traços de personalidade.
        3. Adequação ao sentimento atual.
        
        Gere a lista de sugestões, preenchendo todos os campos do esquema JSON, 
        incluindo uma justificativa clara (reason_for_recommendation) para cada filme.
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
            print(
                f"ERRO DE VALIDAÇÃO DE SAÍDA: O JSON da LLM não se encaixa no modelo Output: {e}"
            )
            return None
