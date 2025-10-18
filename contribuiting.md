# Como Contribuir para o Cinemind

Bem-vindo(a) e obrigado(a) pelo seu interesse em contribuir! Para garantir que o processo seja tranquilo para todos, por favor, siga estas diretrizes.

## Convenções de Commit

Para manter um histórico de versão limpo, legível e fácil de rastrear, pedimos que siga um padrão para as mensagens de commit. Cada mensagem deve ser prefixada com um tipo que descreve a natureza da mudança.

Os principais prefixos que usamos são:

* **`feat:`** (Feature)
    * Adiciona uma nova funcionalidade ao projeto. Deve indicar mudanças perceptíveis para o usuário final ou que ampliem o comportamento do sistema.
    * *Exemplo: `feat: implementar login com Google`*

* **`fix:`** (Bug Fix)
    * Corrige um bug ou comportamento incorreto no código. Serve para restaurar o funcionamento esperado sem adicionar novas funcionalidades.
    * *Exemplo: `fix: corrigir erro de cálculo do desconto`*

Outros prefixos comuns que você pode usar incluem `docs:`, `style:`, `refactor:`, `test:`, e `chore:`.

## Processo de Pull Request (PR)

Antes de abrir um Pull Request para integrar seu código, por favor, revise o checklist abaixo para garantir que sua contribuição está pronta.

### Checklist antes de submeter o código para integração

Antes de abrir um Pull Request, verifique se todos os pontos abaixo estão concluídos:

**1. Qualidade do Código**
* [ ] O código está limpo, legível e segue o padrão de estilo do projeto.
* [ ] As mensagens de commit seguem a convenção (`feat`, `fix`, `docs`, etc.).
* [ ] Nenhum `console.log` ou código de depuração ficou no repositório.

**2. Testes**
* [ ] Todos os testes existentes estão passando.
* [ ] Novas funcionalidades possuem testes cobrindo os principais casos.
* [ ] O projeto executa sem erros ou *warnings*.

**3. Documentação**
* [ ] `README`, comentários e/ou docs foram atualizados conforme as mudanças.
* [ ] Exemplos de uso ou instruções foram revisados, se necessário.

**4. Dependências**
* [ ] Nenhuma dependência desnecessária foi adicionada.
* [ ] Novas dependências são justificáveis e seguras.

## Estrutura de Branches

Nosso fluxo de trabalho utiliza branches específicas para organizar o desenvolvimento:

* **`main`**
    Esta é a branch de produção. Ela contém a versão final, revisada e estável (release) do projeto. *Pushs* diretos são bloqueados; ela só recebe atualizações via *merge* da `develop` após validação completa.

* **`develop`**
    Esta é a branch principal de desenvolvimento e testes. Ela representa a versão mais estável das funcionalidades que estão sendo preparadas para a próxima *release*. Todo código novo deve, eventualmente, ser mesclado aqui após a validação.

* **`develop-hybrid`**
    Esta branch é dedicada a testes de performance e otimização. Especificamente, ela é usada para validar melhorias no tempo de resposta e otimização de chamadas à API, antes que essas mudanças sejam consideradas estáveis o suficiente para a `develop`.

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
