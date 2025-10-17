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

A seguir estão os principais endpoints da API. Para uma documentação completa e interativa, acesse `/api/docs/` após iniciar o servidor.

### Contas (`/api/accounts/`)

* `POST /register/`: Registra um novo usuário.
* `POST /token/`: Obtém um par de tokens (acesso e atualização).
* `POST /token/refresh/`: Atualiza um token de acesso expirado.
* `GET /questions/`: Lista todas as perguntas do questionário de personalidade.
* `POST /answers/submit/`: Envia as respostas do questionário.

### Recomendações (`/api/recommendations/`)

* `GET /genres/`: Lista todos os gêneros de filmes disponíveis.
* `POST /genres/set-favorites/`: Define os gêneros de filmes favoritos do usuário.
* `GET /active-set/`: Retorna o conjunto de recomendações ativo mais recente para o usuário.
* `POST /generate/`: Gera um novo conjunto de recomendações personalizadas.

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
