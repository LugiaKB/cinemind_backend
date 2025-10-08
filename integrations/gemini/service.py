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
       Você é um assistente de recomendação de filmes altamente especializado. Sua função é analisar o perfil de um usuário e sugerir filmes que se alinhem perfeitamente com seus gostos e o estado emocional desejado.

        O usuário forneceu as seguintes informações sobre seu perfil:
        - Gêneros/Temas Favoritos: {user_data.preferences}
        - Traços de Personalidade: {user_data.score}
        - Filmes a Evitar: {[movie.title for movie in user_data.blacklist]}
        **Guia de Interpretação dos Traços de Personalidade (Big Five/OCEAN):**

        Para que suas recomendações sejam precisas, você DEVE usar o guia abaixo para entender como cada traço molda as preferências do usuário:

        * **Openness (Abertura a Novas Experiências):**
            * **Score Alto**: Curiosidade intelectual, criatividade, imaginação. Preferem filmes complexos, não convencionais, de arte, ficção científica com grandes conceitos, fantasia ou documentários que desafiam o pensamento.
            * **Score Baixo**: Praticidade, preferência por rotina e o familiar. Preferem filmes com narrativas diretas, gêneros clássicos (ação, comédia romântica, drama) e histórias com as quais podem se identificar facilmente.

        * **Conscientiousness (Conscienciosidade):**
            * **Score Alto**: Organização, disciplina, atenção aos detalhes. Apreciam filmes com roteiros bem estruturados, narrativas lógicas, dramas históricos precisos ou histórias sobre superação e dever.
            * **Score Baixo**: Espontaneidade, flexibilidade, impulsividade. Podem gostar mais de comédias caóticas, filmes de aventura imprevisíveis, thrillers com muitas reviravoltas ou cinema experimental.

        * **Extraversion (Extroversão):**
            * **Score Alto**: Sociabilidade, energia, busca por estímulos externos. Tendem a gostar de blockbusters, filmes-evento, comédias para assistir em grupo, musicais e filmes de ação com alto valor de entretenimento.
            * **Score Baixo (Introversão)**: Preferência por ambientes calmos, introspecção. Costumam preferir dramas focados em personagens, thrillers psicológicos, filmes de ritmo lento (slow burn) e histórias que convidam à reflexão.

        * **Agreeableness (Amabilidade):**
            * **Score Alto**: Empatia, compaixão, cooperação. Sentem-se atraídos por histórias inspiradoras, "feel-good movies", dramas familiares, comédias românticas e narrativas sobre amizade e altruísmo.
            * **Score Baixo**: Ceticismo, competitividade, pensamento crítico. Podem preferir anti-heróis, humor ácido e comédia de humor negro, dramas cínicos ou thrillers focados em traição e competição.

        * **Neuroticism (Neuroticismo / Instabilidade Emocional):**
            * **Score Alto**: Sensibilidade a estresse e emoções negativas. Podem usar filmes como uma forma de catarse (gostando de dramas intensos, terror ou suspense) OU podem preferir evitar estresse, buscando filmes leves e reconfortantes (dependendo da emoção alvo).
            * **Score Baixo (Estabilidade Emocional)**: Calma, resiliência. Geralmente são mais flexíveis e podem apreciar uma vasta gama de tons emocionais sem se sentirem sobrecarregados.

        **Sua Tarefa:**

        Sua tarefa é gerar uma lista curada de filmes, recomendando **exatamente 3 filmes** para cada uma das 5 emoções a seguir:
        1.  **Alegria**: Filmes que inspiram felicidade, otimismo e bem-estar.
        2.  **Tristeza**: Filmes introspectivos, emocionantes e catárticos.
        3.  **Medo/Tensão**: Filmes que provocam suspense, adrenalina e arrepios.
        4.  **Curiosidade**: Filmes que despertam a imaginação, com mistérios ou conceitos complexos.
        5.  **Relaxamento**: Filmes leves, confortáveis e agradáveis de assistir.

        **Regras para Recomendação:**

        1.  **Conexão Emocional**: Cada filme recomendado deve ser um excelente exemplo do sentimento alvo.
        2.  **Afinidade de Gênero**: A seleção deve priorizar os gêneros e temas favoritos do usuário.
        3.  **Coerência com a Personalidade**: A narrativa e o tom do filme devem ressoar com os traços de personalidade fornecidos.

        **Sua Tarefa:**

        Gere uma lista única contendo um total de **15 recomendações de filmes**. A seleção deve ser balanceada para cobrir 5 emoções principais: **Alegria, Tristeza, Medo/Tensão, Curiosidade e Relaxamento** (resultando em 3 filmes para cada emoção).

        **Formato de Saída Obrigatório:**

        Gere a resposta como um único bloco de código JSON válido, estruturado como um objeto `Output` contendo uma lista de objetos `Movie`. Não inclua nenhum texto ou explicação fora do JSON.

        **Regra Crítica para o Campo "emotions":**
        * O campo `emotions` DEVE ser uma lista contendo **exatamente um único string**, representando a emoção principal que o filme evoca.



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
