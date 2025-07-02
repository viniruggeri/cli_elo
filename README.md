## Visão Geral

Um CRUD de “Eventos Extremos” para gerenciar usuários, bairros e ocorrências (alagamentos, deslizamentos etc.) rodando em Oracle e com UI de terminal estilosa. Feito pra quem curte CLI power user: entradas por *prompt*, logs coloridos com Rich e dados seguros criptografados.

### Por que “Eventos Extremos”?

Porque aqui não é só “criar-ler-atualizar-deletar”—é sobre monitorar áreas de risco (bairros), registrar quem cuida de cada ocorrência e exportar tudo pra JSON. É um sistema leve, mas feito com cuidado: Oracle no backend, SQLModel/Pydantic para modelos, Rich pro front e Typer (se quiser evoluir).

---

## Tecnologias e Dependências

Lista enxuta, mas potente:

* **Python 3.10+**
* **SQLModel** (modelagem Pydantic + SQLAlchemy)
* **oracledb** (conexão Oracle)
* **Pydantic** (validação de dados)
* **Typer** (CLI caseiro, opcional/expandível)
* **Tabulate** (tabelas bonitas no terminal)
* **Cryptography** (criptografia de credenciais)
* **Rich** (UI de terminal estilosa)

**requirements.txt**:

```
sqlmodel
oracledb
pydantic
typer
tabulate
cryptography
rich
```

---

## Estrutura de Pastas

```
backend/
├── database/
│   ├── connection.py      # Conexão segura Oracle + criptografia de credenciais
│   └── models.py          # SQLModel: Usuario, Bairro, Ocorrencia
├── services/
│   ├── crud_usuario.py    # Lógica CRUD (DDL, INSERT, SELECT, UPDATE, DELETE)
│   └── utils.py           # Função de validação de data
├── ui.py              # Funções de interface com Rich (painéis, menus, loading fake) 
├── logger.py              # Logger customizado (arquivo + Rich no terminal)
├── main.py                # Entrypoint: menu principal, loop de opções, chamadas de serviço
└── create_tables.py       # Script standalone para criar as tabelas no Oracle
requirements.txt
```

* **database/connection.py**

  * Gera e lê uma `key.key` para criptografar credenciais (usuário, senha, DSN).
  * Se não encontrar `db_config.json`, solicita usuário e senha no terminal (`getpass`), criptografa e salva.
  * `get_connection()` retorna uma conexão Oracle válida (ou loop de cadastro se falhar).
* **database/models.py**

  * `Usuario`: id, nome, papel, email.
  * `Bairro`: id, nome, proporção de área de risco, densidade populacional.
  * `Ocorrencia`: id, título, descrição (CLOB), categoria, data (DATE), status, localização, referências a `usuario_id` e `bairro_id`.
* **services/crud\_usuario.py**

  * DDL declarados como strings para criar tabelas (`usuario`, `bairro`, `ocorrencia`).
  * Funções:

    * `criar_tabelas()`: executa DDLs (ignora se já existe).
    * `criar_usuario`, `listar_usuarios`.
    * `criar_bairro`, `listar_bairros`.
    * `criar_ocorrencia`, `listar_ocorrencias` (faz JOIN com usuário e bairro, converte LOB para string).
    * `buscar_ocorrencias_por_categoria`.
    * `atualizar_ocorrencia` (constrói UPDATE dinâmico; cuida do campo `data`).
    * `deletar_ocorrencia`.
    * `exportar_ocorrencias_json`: salva todas as ocorrências em `backend/export/ocorrencias_export.json`.
* **services/utils.py**

  * `validar_data(formato: str, data_str: str)`: usa `datetime.strptime` pra checar formato `YYYY-MM-DD`.
* **ui/ui.py**

  * Funções com Rich:

    * `loading_fake(texto)`: spinner + barra de progresso fake pra dar sensação de “carregando”.
    * `linha(texto)`: rule estilizada.
    * `sucesso(msg)`, `erro(msg)`, `alerta(msg)`, `info(msg)`: prints coloridos com ícones.
    * `painel(texto, titulo)`: painel de Rich com borda colorida.
    * `menu(titulo, opcoes: list)`: exibe opções numeradas, retorno como string.
    * `input_pastel(texto)`: input estilizado.
    * `pause()`: “Pressione Enter para continuar…”.
* **logger.py**

  * `elo_logger`: captura todos os níveis (`DEBUG` pra cima).
  * `FileHandler` grava em `elo.log` com formato `[DD/MM/YYYY HH:MM:SS] [NÍVEL] Mensagem`.
  * Funções de log customizadas:

    * `log_info(msg)`: grava `INFO` e imprime num tom azul pastel.
    * `log_sucesso(msg)`: grava `INFO` com tag `[SUCESSO]` e printa com ícone de check.
    * `log_erro(msg)`: grava `ERROR` e printa em vermelho.
    * `log_alerta(msg)`: `WARNING` e printa em cor pastel.
    * `log_critico(msg)`: `CRITICAL` e painel vermelho no terminal.
* **main.py**

  * Loop principal: limpa a tela (`cls`/`clear`), exibe painel “Bem-vindo ao ELO!” e mostra menu com 10 opções (0 pra sair).
  * Cada opção mapeia pra uma função CRUD do `services/crud_usuario`.

    1. Listar usuários → usa `tabulate` para exibir.
    2. Criar usuário → valida inputs; faz `criar_usuario(...)`; log e mensagem de sucesso/erro.
    3. Listar bairros.
    4. Criar bairro → converte strings numéricas (área de risco, densidade); valida `float`.
    5. Listar ocorrências (com JOIN de nomes).
    6. Criar ocorrência → valida data (`validar_data`); converte `usuario_id` e `bairro_id` pra `int`; chama `criar_ocorrencia(...)`.
    7. Buscar ocorrências por categoria → retorna lista e exibe com `tabulate`.
    8. Atualizar ocorrência → lê `id`, lê `campo` (título, descrição, categoria, data, status, localizacao); valida; chama `atualizar_ocorrencia`.
    9. Deletar ocorrência.
    10. Exportar ocorrências para JSON (`exportar_ocorrencias_json`).
  * Em cada fluxo, logs de ações do usuário e logs de erros.
  * Ao final, imprime “Programa encerrado” e finaliza.
* **create\_tables.py**

  * Simples: executa `criar_tabelas()` e imprime “Tabelas criadas com sucesso!” (ponto único de entrada para criar DDL via CLI).

---

## Como Rodar (Setup)


1. **Crie e ative um virtualenv**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate     # macOS/Linux
   .venv\Scripts\activate        # Windows
   ```

2. **Instale as dependências**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configurar credenciais Oracle**

   * Ao rodar pela primeira vez qualquer script que invoque `get_connection()` (por exemplo, `python create_tables.py`), a aplicação vai pedir:

     ```
     Usuário:
     Senha (não aparece ao digitar):
     ```
   * Insira suas credenciais. Isso gera:

     * `key.key`: chave Fernet para criptografia.
     * `db_config.json`: contendo usuário, senha, DSN criptografados.
   * **Importante**: **NUNCA** compartilhe `key.key` e `db_config.json` publicamente.

4. **Criar as tabelas**

   ```bash
   python create_tables.py
   ```

   Deve exibir:

   ```
   🟢 Conexão com Oracle realizada com sucesso!
   Tabelas criadas com sucesso!
   ```

   Se a tabela já existir, o script ignora e segue em frente (com DDL dentro de `crud_usuario.py`).

5. **Executar a aplicação**

   ```bash
   python main.py
   ```

   Você verá o menu principal no terminal. Basta digitar o número da ação desejada (0–10).

---

## Exemplos de Uso

> **Listar Bairros**
>
> 1. Selecione “3” no menu.
> 2. Aguarde o loading fake.
> 3. Se houver bairros cadastrados, aparece tabela como:
>
>    ```
>    ┏━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
>    ┃ id  ┃ nome           ┃ area_risco_prop   ┃ pop_densidade ┃
>    ┡━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
>    │ 1   │ Vila Linda     │ 0.35              │ 12000.0       │
>    │ 2   │ Alto da Serra  │ 0.80              │ 5000.0        │
>    └─────┴────────────────┴───────────────────┴───────────────┘
>    ```

> **Criar Ocorrência**
>
> 1. Selecione “6” no menu.
> 2. Preencha título, descrição, categoria (ex: `alagamento`), data (`YYYY-MM-DD`), status, local de referência, IDs de `usuario` e `bairro`.
> 3. Se data estiver no formato errado, avisa com `erro(...)` e volta para o menu.
> 4. Ao sucesso:
>
>    ```
>    :white_check_mark: Ocorrência criada com ID 5
>    ```

> **Exportar para JSON**
>
> 1. Selecione “10” no menu.
> 2. A pasta `backend/export` será criada (se não existir) e o arquivo `ocorrencias_export.json` salvo lá.
> 3. Mensagem de sucesso:
>
>    ```
>    :white_check_mark: Exportado para ./export/ocorrencias_export.json
>    ```

---

## Detalhes Técnicos e Dicas de Desenvolvimento

1. **Conexão + Segurança**

   * `get_connection()` primeiro busca `db_config.json`; se não existe, chama `cadastrar_login()` pra criptografar e salvar credenciais com `cryptography.Fernet`.
   * O DSN padrão é vazio, mas você pode mudar no código ou inserir outro DSN no cadastro.
   * Em caso de falha no `ping()`, solicita recadastro automático.

2. **Modelos SQLModel**

   * `Usuario`, `Bairro` e `Ocorrencia` são classes que herdam de `SQLModel, table=True`.
   * Chaves primárias geradas automaticamente (`IDENTITY`).
   * `Ocorrencia.data` é uma string no modelo, mas convertida para `DATE` no SQL via `TO_DATE(:data, 'YYYY-MM-DD')`.

3. **CRUD e DDL**

   * O DDL (CREATE TABLE) fica em `crud_usuario.py`. No `criar_tabelas()`, cada DDL é executado (= “IF NOT EXISTS” manual).
   * Métodos de inserção usam `RETURNING id INTO :id_out` pra retornar o PK gerado.
   * `listar_ocorrencias()` faz JOIN com `usuario` e `bairro`, converte eventual LOB (`CLOB`) pra string Python.

4. **Validação de Data**

   * `validar_data("%Y-%m-%d", data)` retorna `True/False`. Se `False`, não deixa inserir ou atualizar.

5. **Logger Customizado**

   * Qualquer ação (criar, listar, erro, etc.) faz `log_info`, `log_sucesso`, `log_erro` ou `log_alerta`.
   * O arquivo `elo.log` recebe registros no formato `25/04/2025 14:35:12 INFO    Usuário criou bairro: ID 3, Nome: Centro`.
   * No terminal, as mensagens aparecem coloridas com Rich, painel em caso de `log_critico`.

6. **Interface de Terminal (Rich)**

   * `ui.menu()`: exibe número + descrição, além de opção “0 – Sair”.
   * `loading_fake()`: spinner + barra de progresso, só pra zoeira visual.
   * Funções de arte (painel, linha) deixam a CLI com cara de dashboard.

---

## Resumo Rápido para Devs

1. **venv**, **pip install -r requirements.txt**.
2. **python create\_tables.py** (cadastre credenciais FIAP quando solicitado).
3. **python main.py** e interaja com o menu.
4. Logs → `elo.log`; exportações → `backend/export/ocorrencias_export.json`.

> Pronto! Agora você tem um CRUD de “Eventos Extremos” bala, com backend Oracle, modelos SQLModel, validação Pydantic, CLI Rich pastel, logs profissa e export JSON. Sem frescura.
