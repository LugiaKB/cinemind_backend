# integrations/gemini/service.py

from typing import Optional
from integrations.gemini.client import GeminiClient
from integrations.gemini.types import Input, Output

class GeminiService:
    RECOMMENDATION_MODEL = "gemini-1.5-flash" # Mantido ou pode ser "gemini-1.5-pro"

    def __init__(self):
        self.client = GeminiClient(model=self.RECOMMENDATION_MODEL)

    def _build_system_instruction(self) -> str:
        # O system instruction (guia de personalidade) permanece o mesmo.
        return (
            "Você é um assistente de recomendação de filmes altamente especializado. "
            "Sua função é analisar o perfil de um usuário e sugerir filmes que se alinhem perfeitamente "
            "com seus gostos e o estado emocional desejado. Sua resposta deve estar EXCLUSIVAMENTE "
            "no formato JSON, aderindo ao esquema fornecido.\n\n"
            "**Guia de Interpretação dos Traços de Personalidade (Big Five/OCEAN):**\n"
            "Para que suas recomendações sejam precisas, você DEVE usar o guia abaixo para entender como cada traço molda as preferências do usuário:\n\n"
            "* **Openness (Abertura a Novas Experiências):**\n"
            "  - **Score Alto**: Curiosidade intelectual, criatividade. Preferem filmes complexos, não convencionais, de arte, ficção científica com grandes conceitos ou documentários que desafiam o pensamento.\n"
            "  - **Score Baixo**: Praticidade, preferência pelo familiar. Preferem filmes com narrativas diretas, gêneros clássicos (ação, comédia romântica) e histórias com as quais podem se identificar facilmente.\n\n"
            "* **Conscientiousness (Conscienciosidade):**\n"
            "  - **Score Alto**: Organização, disciplina. Apreciam filmes com roteiros bem estruturados, narrativas lógicas, dramas históricos precisos ou histórias sobre superação.\n"
            "  - **Score Baixo**: Espontaneidade, flexibilidade. Podem gostar mais de comédias caóticas, filmes de aventura imprevisíveis ou thrillers com muitas reviravoltas.\n\n"
            "* **Extraversion (Extroversão):**\n"
            "  - **Score Alto**: Sociabilidade, busca por estímulos externos. Tendem a gostar de blockbusters, musicais e filmes de ação com alto valor de entretenimento.\n"
            "  - **Score Baixo (Introversão)**: Preferência por introspecção. Costumam preferir dramas focados em personagens, thrillers psicológicos e histórias que convidam à reflexão.\n\n"
            "* **Agreeableness (Amabilidade):**\n"
            "  - **Score Alto**: Empatia, compaixão. Sentem-se atraídos por histórias inspiradoras, 'feel-good movies', dramas familiares e comédias românticas.\n"
            "  - **Score Baixo**: Ceticismo, pensamento crítico. Podem preferir anti-heróis, humor ácido, comédia de humor negro ou dramas cínicos.\n\n"
            "* **Neuroticism (Neuroticismo / Instabilidade Emocional):**\n"
            "  - **Score Alto**: Sensibilidade a estresse. Podem usar filmes como catarse (gostando de dramas intensos ou terror) OU para evitar estresse (buscando filmes leves e reconfortantes).\n"
            "  - **Score Baixo (Estabilidade Emocional)**: Calma, resiliência. Geralmente são flexíveis e apreciam uma vasta gama de tons emocionais sem se sentirem sobrecarregados.\n\n"
            "**Regras para Recomendação:**\n"
            "1. **Conexão Emocional**: Cada filme recomendado deve ser um excelente exemplo do sentimento alvo.\n"
            "2. **Afinidade de Gênero**: A seleção deve priorizar os gêneros e temas favoritos do usuário.\n"
            "3. **Coerência com a Personalidade**: A narrativa e o tom do filme devem ressoar com os traços de personalidade fornecidos, usando o guia acima.\n"
            "4. **Evitar Blacklist**: JAMAIS recomende filmes que estão na lista de filmes a evitar.\n"
        )

    def _build_user_prompt(self, user_data: Input) -> str:
        personality_scores = "\n".join([f"- {trait}: {score}" for trait, score in user_data.score.items()])
        blacklist_titles = ', '.join([movie.title for movie in user_data.blacklist]) if user_data.blacklist else "Nenhum"

        # --- PROMPT TOTALMENTE REFEITO PARA FOCAR EM UM ÚNICO HUMOR ---
        return (
            "Analise o perfil de usuário a seguir e gere as recomendações de acordo com as regras definidas.\n\n"
            "**Perfil do Usuário:**\n"
            f"- Gêneros/Temas Favoritos: {', '.join(user_data.preferences)}\n"
            f"- Traços de Personalidade (Scores):\n{personality_scores}\n"
            f"- Filmes a Evitar: {blacklist_titles}\n\n"
            "**Sua Tarefa:**\n"
            f"Gere uma lista curada contendo **exatamente 3 recomendações de filmes ranqueados (rank 1, 2, 3)** para o humor específico: **'{user_data.target_mood}'**.\n\n"
            "Para cada filme, forneça uma justificativa clara (reason_for_recommendation) que conecte o filme diretamente ao perfil do usuário (gêneros e personalidade)."
        )

    def get_recommendations(self, user_data: Input) -> Optional[Output]:
        system_instruction = self._build_system_instruction()
        user_prompt = self._build_user_prompt(user_data)

        json_schema = Output.model_json_schema()

        raw_response = self.client.generate_json_response(
            prompt=user_prompt,
            system_instruction=system_instruction,
            json_schema=json_schema,
        )

        if raw_response is None:
            print("ERRO DE RECOMENDAÇÃO: A resposta da API foi nula.")
            return None
        
        if raw_response.get("status") == "error":
            print(f"ERRO DE RECOMENDAÇÃO: {raw_response.get('message', 'Erro desconhecido da API')}")
            return None

        try:
            return Output(**raw_response)
        except Exception as e:
            print(f"ERRO DE VALIDAÇÃO DE SAÍDA: O JSON da LLM não se encaixa no modelo Output: {e}")
            print(f"JSON Recebido: {raw_response}")
            return None
