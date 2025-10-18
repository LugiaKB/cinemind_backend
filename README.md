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

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### Pré-requisitos

* Python 3.11
* Pipenv
* PostgreSQL

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/cinemind_backend.git](https://github.com/seu-usuario/cinemind_backend.git)
    cd cinemind_backend
    ```
2.  **Instale as dependências:**
    ```bash
    pipenv install
    ```
3.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
    ```
    DJANGO_SECRET_KEY='sua_chave_secreta_aqui'
    GEMINI_API_KEY='sua_api_key_do_gemini'

    # Configurações do Banco de Dados PostgreSQL
    DB_NAME='cinemind_db'
    DB_USER='seu_usuario'
    DB_PASSWORD='sua_senha'
    DB_HOST='localhost'
    DB_PORT='5432'
    ```
4.  **Aplique as migrações do banco de dados:**
    ```bash
    pipenv run python manage.py migrate
    ```
5.  **Crie um superusuário (opcional):**
    ```bash
    pipenv run python manage.py createsuperuser
    ```

## Executando a Aplicação

Para iniciar o servidor de desenvolvimento, execute:

```bash
pipenv run python manage.py runserver
