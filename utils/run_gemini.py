# utils/run_gemini.py

import os
import sys
import django
from dotenv import load_dotenv

# Configure o ambiente do Django
# Adiciona o diretório raiz do projeto ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinemind.settings')
django.setup()

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Imports após a configuração do Django
from integrations.gemini.service import GeminiService
from integrations.gemini.types import Input as GeminiInput, BlacklistedMovieInput

def main():
    """
    Função principal para executar um teste de ponta a ponta do serviço Gemini,
    agora adaptado para o novo fluxo de obtenção de parâmetros de busca.
    """
    print("🚀 Iniciando teste do serviço Gemini para obter parâmetros de busca...")

    # 1. Crie um exemplo de entrada (Input)
    # Simula o perfil de um usuário que será enviado para a IA
    gemini_input = GeminiInput(
        preferences=["Science Fiction", "Mystery"],
        score={
            "openness": 0.8,
            "conscientiousness": 0.4,
            "extraversion": 0.6,
            "agreeableness": 0.3,
            "neuroticism": 0.7,
        },
        blacklist=[
            BlacklistedMovieInput(title="Inception"),
            BlacklistedMovieInput(title="The Matrix"),
        ],
        target_mood="Suspense" # O humor que o usuário selecionou
    )

    print(f"\n👤 Perfil de usuário enviado para a IA (para o humor '{gemini_input.target_mood}'):")
    print(f"   - Preferências: {gemini_input.preferences}")
    print(f"   - Blacklist: {[b.title for b in gemini_input.blacklist]}")

    # 2. Instancie e chame o serviço
    gemini_service = GeminiService()
    
    # Chama o método que agora busca parâmetros de busca, não filmes
    search_parameters = gemini_service.get_search_parameters(gemini_input)

    # 3. Exiba o resultado
    if search_parameters:
        print("\n✅ Sucesso! Gemini retornou os seguintes parâmetros de busca:")
        print(f"   - Gêneros sugeridos: {search_parameters.genres}")
        print(f"   - Palavras-chave sugeridas: {search_parameters.keywords}")
        print("\nEstes parâmetros seriam agora usados para fazer uma busca na API do TMDb.")
    else:
        print("\n❌ Falha! Não foi possível obter os parâmetros de busca do serviço Gemini.")
        print("   Verifique os logs de erro acima para mais detalhes.")

if __name__ == "__main__":
    main()
