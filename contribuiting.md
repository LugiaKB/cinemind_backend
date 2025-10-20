# Como Contribuir para o Cinemind

Bem-vindo(a) e obrigado(a) pelo seu interesse em contribuir! Para garantir que o processo seja tranquilo para todos, por favor, siga estas diretrizes.

## Configurando o Ambiente Local

Para começar a desenvolver, siga estes passos para configurar o projeto na sua máquina.

1.  **Faça um Fork e Clone o repositório:**
    * Primeiro, faça um *fork* do repositório para a sua conta no GitHub.
    * Depois, clone o *seu fork* localmente:
    ```bash
    git clone [https://github.com/SEU-USUARIO/cinemind.git](https://github.com/SEU-USUARIO/cinemind.git)
    cd cinemind
    ```

2.  **Instale as Dependências:**
    *(Assumindo que o projeto usa Node.js/npm)*
    ```bash
    npm install
    ```

3.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto, copiando o arquivo de exemplo.
    ```bash
    cp .env.example .env
    ```
    *Obs: Edite o arquivo `.env` com as chaves de API e configurações locais necessárias para rodar o projeto.*

4.  **Comandos Úteis:**
    * Para rodar o projeto em modo de desenvolvimento:
        ```bash
        npm run dev
        ```
    * Para rodar os testes:
        ```bash
        npm test
        ```

---

## Nosso Fluxo de Colaboração

Nosso processo é baseado em *Issues* e *Pull Requests* (PRs).

1.  **Encontre ou crie uma Issue:**
    * Antes de começar, verifique no [quadro de Issues](https://github.com/USUARIO-DO-PROJETO/cinemind/issues) se já não existe uma *issue* para o que você quer fazer.
    * Se for um bug ou uma *feature* nova, crie uma *issue* detalhada para que o time possa discuti-la.

2.  **Crie sua Branch:**
    * A partir da branch `develop` do seu *fork*, crie uma nova *branch* seguindo nossas convenções de nomenclatura (veja abaixo).

3.  **Desenvolva e Faça Commits:**
    * Faça suas alterações.
    * Faça commits atômicos (pequenos e focados) usando as nossas [Convenções de Commit](#convenções-de-commit).

4.  **Abra um Pull Request (PR):**
    * Quando terminar, envie (push) sua *branch* para o seu *fork* no GitHub.
    * Abra um *Pull Request* (PR) da sua *branch* para a branch `develop` do repositório principal.
    * Preencha o *template* do PR, detalhando o que foi feito e vinculando a *issue* que você está resolvendo (ex: `Resolves #42`).
    * Certifique-se de que seu PR passa em todos os *checks* (testes, lint, etc.).

5.  **Revisão:**
    * Aguarde a revisão do seu código. O time poderá solicitar alterações antes de aprovar e fazer o *merge*.

---

## Convenções de Nomenclatura

### 1. Estrutura de Branches

Usamos branches específicas para organizar o desenvolvimento:

* **`main`**
    Esta é a branch de produção. Ela contém a versão final, revisada e estável (release). *Pushs* diretos são bloqueados.

* **`develop`**
    Esta é a branch principal de desenvolvimento. Todo código novo deve ser mesclado aqui (via PR) para testes antes de ir para a `main`. **Sua branch deve ser criada a partir desta.**

* **`develop-hybrid`**
    Branch dedicada a testes de performance e otimização de chamadas à API.

* **Branches de Trabalho (Sua Branch)**
    Ao criar uma branch para uma *feature* ou *fix*, siga este padrão:

    * **Features:** `feat/<nome-da-feature>`
        * *Exemplo: `feat/login-com-google`*
    * **Correções (Fixes):** `fix/<descricao-do-bug>`
        * *Exemplo: `fix/calculo-incorreto-desconto`*
    * **Documentação:** `docs/<topico-documentado>`
        * *Exemplo: `docs/atualiza-contributing`*

### 2. Convenções de Commit

Para manter um histórico de versão limpo e legível, cada mensagem de commit deve ser prefixada com um tipo:

* **`feat:`** (Feature)
    * Adiciona uma nova funcionalidade ao projeto.
    * *Exemplo: `feat: implementar login com Google`*

* **`fix:`** (Bug Fix)
    * Corrige um bug ou comportamento incorreto no código.
    * *Exemplo: `fix: corrigir erro de cálculo do desconto`*

* **Outros prefixos comuns:**
    * `docs:` (Atualizações na documentação)
    * `style:` (Ajustes de formatação, sem mudança lógica)
    * `refactor:` (Refatoração de código sem alterar comportamento)
    * `test:` (Adição ou correção de testes)
    * `chore:` (Manutenção de build, scripts, dependências)

---

## Checklist antes de submeter o código para integração

Antes de abrir um Pull Request, revise e marque os seguintes pontos:

**1. Qualidade do Código**
* [ ] O código está limpo, legível e segue o padrão de estilo do projeto.
* [ ] As mensagens de commit seguem a convenção (`feat`, `fix`, `docs`, etc.).
* [ ] Nenhum `console.log` ou código de depuração ficou no repositório.

**2. Testes**
* [ ] Todos os testes existentes estão passando (`npm test`).
* [ ] Novas funcionalidades possuem testes cobrindo os principais casos.
* [ ] O projeto executa sem erros ou *warnings*.

**3. Documentação**
* [ ] `README`, comentários e/ou docs foram atualizados conforme as mudanças.
* [ ] Exemplos de uso ou instruções foram revisados, se necessário.

**4. Dependências**
* [ ] Nenhuma dependência desnecessária foi adicionada.
* [ ] Novas dependências são justificáveis e seguras.

---

## Manual de Endpoints para Frontend (Fluxo de Usuário)

Este é o guia organizado com o fluxo de chamadas da API, mostrando o método, a URL e as notas de fluxo necessárias para o frontend.

### 1. Cadastro (Register)

* **Método:** `POST`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/accounts/register/`
* **Autenticação:** Nenhuma
* **Corpo (Body) Exemplo:**
    ```json
    {
      "username": "Z@R0kIgVteGlmZ+i168Z.ME",
      "email": "user@example.com",
      "password": "string"
    }
    ```

### 2. Login (Obter Token de Acesso)

* **Método:** `POST`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/accounts/token/`
* **Autenticação:** Nenhuma
* **Corpo (Body) Exemplo:**
    ```json
    {
      "username": "lucas",
      "password": "cinemind"
    }
    ```
* **Notas:** Salve o valor da chave `access` recebida na resposta. Ele será usado em todas as chamadas autenticadas seguintes, no cabeçalho `Authorization` como `Bearer <access_token>`.

### 3. Verificar Questionário (Answers Check)

* **Método:** `GET`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/accounts/answers/check/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Notas de Fluxo:**
    * **Se a resposta for `{"has_submitted": true}`:** O usuário já respondeu. Pule o formulário e vá para a **Etapa 6 (Verificar Gêneros)**.
    * **Se a resposta for `{"has_submitted": false}`:** O usuário precisa responder. Siga para a **Etapa 4 (Obter Perguntas)**.

### 4. Obter Perguntas do Questionário

*(Executar apenas se `has_submitted` for `false`)*

* **Método:** `GET`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/accounts/questions/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Notas:** Use o JSON array recebido para montar a tela de 10 questões para o usuário.

### 5. Enviar Respostas do Questionário

*(Executar após o usuário preencher as 10 questões da Etapa 4)*

* **Método:** `POST`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/accounts/answers/submit/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Corpo (Body) Exemplo:** (Envie todas as respostas em um array)
    ```json
    {
      "answers": [
        {
          "question_id": "3f512c82-3c67-4693-baf4-d289ebf27120",
          "selected_value": 1
        },
        {
          "question_id": "f4f00fa2-8642-4399-b588-65b594b59d56",
          "selected_value": 0
        }
      ]
    }
    ```

### 6. Verificar Gêneros Favoritos

* **Método:** `GET`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/recommendations/genres/check-favorites/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Notas de Fluxo:**
    * **Se a resposta for `{"has_genres": true}`:** O usuário já selecionou. Pule a seleção de gêneros e vá para a **Etapa 9 (Tela Inicial - Obter Humores)**.
    * **Se a resposta for `{"has_genres": false}`:** O usuário precisa selecionar. Siga para a **Etapa 7 (Obter Gêneros)**.

### 7. Obter Lista de Gêneros

*(Executar apenas se `has_genres` for `false`)*

* **Método:** `GET`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/recommendations/genres/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Notas:** Use o JSON array recebido para montar a tela de seleção de gêneros.

### 8. Definir Gêneros Favoritos

*(Executar após o usuário selecionar os gêneros da Etapa 7)*

* **Método:** `POST`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/recommendations/genres/set-favorites/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Corpo (Body) Exemplo:** (Envie os IDs dos gêneros selecionados)
    ```json
    {
      "genre_ids": [
        "9f0ce012-6845-4c7e-b63d-6476695de4ae",
        "ae045d69-33a0-42e5-b9d2-91691e7add1f"
      ]
    }
    ```

### 9. Tela Inicial: Obter Humores (Moods)

* **Método:** `GET`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/recommendations/moods/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Notas:** Use o JSON array recebido (Alegria, Tristeza, etc.) para popular a circunferência de 5 emoções na tela inicial.

### 10. Obter "Set" de Recomendação Ativo

* **Método:** `GET`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/recommendations/active-set/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Notas:** Salve o `id` (ex: `"084d0eba-d3c1-4cc7-be55-7973e5560223"`) recebido na resposta. Ele será o `<set_id>` da próxima etapa.

### 11. Gerar Recomendações para um Humor

*(Executar quando o usuário clicar em uma emoção da Etapa 9)*

* **Método:** `POST`
* **URL:** `https://cinemind-api-mj06.onrender.com/api/recommendations/sets/<set_id>/generate-for-mood/`
* **Autenticação:** `Authorization: Bearer <access_token>`
* **Corpo (Body) Exemplo:**
    ```json
    {
      "mood_id": "5ce37bae-28ef-4fbf-91e8-769857cea79e"
    }
    ```
* **Notas:**
    * Substitua `<set_id>` na URL pelo ID obtido na **Etapa 10**.
    * Use o `mood_id` da emoção que o usuário clicou (obtido na **Etapa 9**).
    * A resposta será um array de 3 filmes.
    * Exiba o filme `rank: 1` (título, thumbnail, sinopse). Ao clicar no botão "próximo", mostre `rank: 2`, depois `rank: 3`, e então volte para o `rank: 1` (ciclo).
