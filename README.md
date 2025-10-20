# Cinemind Backend

## Visão Geral

O Cinemind é um sistema de recomendação de filmes personalizado que utiliza o modelo de personalidade "Big Five" para sugerir filmes que se alinhem com os traços de personalidade e preferências de gênero do usuário. A plataforma oferece um questionário para avaliar o perfil do usuário e, com base nisso, gera recomendações de filmes categorizadas por humor.

## Recursos

* **Autenticação de Usuário**: Sistema completo de registro e login com tokens JWT.
* **Questionário de Personalidade**: Um questionário baseado no modelo "Big Five" para avaliar a personalidade do usuário.
* **Recomendações com IA**: Utiliza a API Gemini do Google para gerar recomendações de filmes personalizadas e inteligentes.
* **Categorização por Humor**: As recomendações são agrupadas em cinco categorias de humor: Alegria, Tristeza, Medo/Tensão, Curiosidade e Relaxamento.
* **Preferências de Gênero**: Os usuários podem selecionar seus gêneros de filmes favoritos para refinar ainda mais as recomendações.
* **Documentação da API**: A API é autodocumentada usando drf-spectacular, com Swagger UI e ReDoc.

## Tecnologias Utilizadas

* **Backend**:
    * Python 3.11
    * Django & Django REST Framework
    * PostgreSQL
    * Gunicorn & WhiteNoise (para produção)
* **Inteligência Artificial**:
    * Google Gemini
* **Gerenciamento de Dependências**:
    * Pipenv

## Endpoints da API

A seguir estão os principais endpoints da API. Para uma documentação completa e interativa, acesse a URL da sua API: `https://cinemind-api-mj06.onrender.com/api/docs`

### Contas (`/api/accounts/`)

* `POST /api/accounts/register/`: Registra um novo usuário.
* `POST /api/accounts/token/`: Obtém um par de tokens (acesso e atualização).
* `POST /api/accounts/token/refresh/`: Atualiza um token de acesso expirado.
* `GET /api/accounts/questions/`: Lista todas as perguntas do questionário de personalidade.
* `POST /api/accounts/answers/submit/`: Envia as respostas do questionário.
* `GET /api/accounts/answers/check/`: Verifica se o usuário já respondeu ao questionário.

### Recomendações (`/api/recommendations/`)

* `GET /api/recommendations/genres/`: Lista todos os gêneros de filmes disponíveis.
* `POST /api/recommendations/genres/set-favorites/`: Define os gêneros de filmes favoritos do usuário.
* `GET /api/recommendations/genres/check-favorites/`: Verifica os gêneros favoritos definidos pelo usuário.
* `GET /api/recommendations/moods/`: Lista os humores disponíveis para recomendação.
* `POST /api/recommendations/sets/`: Gera um novo conjunto de recomendações personalizadas (endpoint principal da IA).
* `GET /api/recommendations/active-set/`: Retorna o conjunto de recomendações ativo mais recente para o usuário.
* `POST /api/recommendations/sets/{set_id}/generate-for-mood/`: Gera recomendações para um humor específico dentro de um conjunto existente.

### Schema (`/api/schema/`)

* `GET /api/schema/`: Obtém o schema OpenAPI (usado pelo Swagger/ReDoc).

## Instalação, configuração e execução

Fluxo mínimo e reproduzível para desenvolvimento local. Use este bloco como padrão também no repositório frontend.

## Pré-requisitos

- Python 3.11
- pipenv (recomendado) ou virtualenv + pip
- PostgreSQL (ou `DATABASE_URL` configurada)

## Passos rápidos

1. Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/seu-usuario/cinemind_backend.git
cd cinemind_backend
```

2. Instale dependências e ative o ambiente (pipenv):

```bash
pipenv install --dev
pipenv shell
```

### Alternativa com virtualenv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias (sem aspas). Exemplo mínimo:

```env
DJANGO_SECRET_KEY=troque_por_sua_chave
GEMINI_API_KEY=AIzaSyEXEMPLO
DB_NAME=cinemind_db
DB_USER=cinemind_user
DB_PASSWORD=senha_segura
DB_HOST=localhost
DB_PORT=5432
```

4. Aplique migrations e (opcional) crie um superusuário:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Rode o servidor local:

```bash
python manage.py runserver
```

## Utilitários / Gemini

Confirme que `GEMINI_API_KEY` está disponível antes de executar utilitários que chamam a API Gemini:

```bash
python -c "import os; print(os.getenv('GEMINI_API_KEY'))"
python utils/run_gemini.py
```

## Cheatsheet (comandos rápidos)

```bash
pipenv install
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python utils/run_gemini.py
```

## Dicas rápidas

- Não use aspas no `.env` (use `KEY=value`).
- Se a variável aparecer vazia, ative o virtualenv/pipenv shell antes de rodar.
- Para garantir que scripts carreguem o `.env` explicitamente, use `load_dotenv` com o caminho absoluto para a raiz do projeto.

---
