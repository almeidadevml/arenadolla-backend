# Arena Dolla — Backend de Replays

API que recebe replays de vídeo gravados numa arena de futevôlei, guarda os vídeos na nuvem e registra as informações num banco de dados.

Faz parte de um sistema maior: uma câmera grava o jogo o tempo todo, e quando alguém aperta um botão na beira da quadra, os últimos 30 segundos viram um replay. Esse replay é enviado automaticamente para esta API, que guarda o vídeo e deixa ele disponível para o site.

## Arquitetura

```mermaid
flowchart LR
    A[Câmera] --> B[ffmpeg - buffer de 5s]
    B --> C[Botão Salvar Replay]
    C --> D[Clipe de 30s]
    D --> E[API Arena Dolla - Render]
    E --> F[(PostgreSQL - Supabase)]
    E --> H[(Storage - vídeos)]
    E --> G[Site - em desenvolvimento]
```

Este repositório é a **API** (a caixa "API Arena Dolla"). A parte da quadra, com a câmera e o botão, fica no repositório [arenadolla-capture](https://github.com/almeidadevml/arenadolla-capture).

## Endpoints

| Método | Endereço | O que faz |
|---|---|---|
| `POST` | `/api/replays` | Recebe um vídeo, envia para o Supabase Storage e registra no banco |
| `GET` | `/api/replays` | Lista todos os replays, do mais recente para o mais antigo |

A API está no ar em: https://arenadolla-backend.onrender.com

A documentação interativa (para testar os endpoints pelo navegador) fica em: https://arenadolla-backend.onrender.com/docs

> O plano gratuito do Render "dorme" depois de 15 minutos sem uso. O primeiro acesso pode levar cerca de 1 minuto.

## Banco de dados

Tabela `replays`:

| Coluna | O que guarda |
|---|---|
| `id` | Identificador único do replay (UUID) |
| `filename` | Nome do arquivo de vídeo no storage |
| `url_video` | Link público do vídeo no Supabase Storage |
| `duracao_segundos` | Duração do replay, em segundos |
| `criado_em` | Data e hora em que o replay foi salvo (em UTC) |

A tabela é criada automaticamente quando a API liga, se ainda não existir.

## Tecnologias

- **Python** — linguagem principal
- **FastAPI** — criação da API e dos endpoints
- **Uvicorn** — servidor que roda a API
- **PostgreSQL (Supabase)** — banco de dados na nuvem
- **Supabase Storage** — armazenamento dos vídeos
- **psycopg2** — conexão do Python com o PostgreSQL
- **supabase** — biblioteca oficial, usada para enviar os vídeos ao storage
- **python-dotenv** — leitura das configurações do arquivo `.env`
- **Render** — hospedagem da API na internet

## Pré-requisitos

- **Python 3.10** ou mais recente
- **Git**, para clonar o repositório
- Um projeto no **[Supabase](https://supabase.com)** (o plano gratuito funciona), com:
  - o banco PostgreSQL (já vem criado)
  - um bucket **público** chamado `replays`, em **Storage**

## Estrutura do projeto

```
arenadolla-backend/
├── main.py              # API: endpoints de upload e listagem de replays
├── database.py          # Conexão com o PostgreSQL, criação da tabela e consultas
├── storage.py           # Envio dos vídeos para o Supabase Storage
├── requirements.txt     # Bibliotecas Python do projeto
├── .gitignore           # Arquivos que não vão para o GitHub
└── README.md            # Este arquivo
```

Você cria manualmente (não vai para o GitHub):

- `.env` — configurações com as senhas e chaves

## Variáveis de ambiente

| Variável | Para que serve |
|---|---|
| `DATABASE_URL` | Endereço de conexão com o banco PostgreSQL, incluindo usuário e senha |
| `SUPABASE_URL` | Endereço do projeto no Supabase (ex.: `https://xxxxx.supabase.co`) |
| `SUPABASE_KEY` | Chave secreta do Supabase (*Secret key*), usada para enviar os vídeos |

No seu PC, elas ficam num arquivo `.env` na raiz do projeto:

```
DATABASE_URL=postgresql://usuario:senha@host:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=sua-chave-secreta
```

O `.env` está no `.gitignore` e **nunca** deve ir para o GitHub. No Render, as mesmas variáveis são configuradas no painel, em **Environment**.

## Como rodar localmente

1. Clone o repositório e entre na pasta:

```bash
git clone https://github.com/almeidadevml/arenadolla-backend.git
cd arenadolla-backend
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo `.env` com as três variáveis (veja a seção acima).

5. Rode o servidor:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

A API vai estar em http://localhost:8001/docs

## Status do projeto

- [x] Endpoint de upload de replays
- [x] Endpoint de listagem de replays
- [x] Banco PostgreSQL na nuvem (Supabase)
- [x] Armazenamento permanente dos vídeos (Supabase Storage)
- [x] API publicada na nuvem (Render)
- [x] Integração com o serviço de captura da quadra

## Próximas melhorias

- Apagar automaticamente os replays antigos, para não passar do limite de 1 GB do plano gratuito
- Proteger o endpoint de upload, para que só o serviço da quadra consiga enviar vídeos
- Testes automatizados
- Site para assistir e compartilhar os replays

## Autor

Feito por **Lucas Almeida** — [github.com/almeidadevml](https://github.com/almeidadevml)