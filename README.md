# Arena Dolla - Backend de Replays

API que recebe vídeos gravados de uma arena de futevôlei e guarda as informações num banco de dados da nuvem.

Faz parte de um sistema maior: uma câmera grava o jogo, e quando alguém aperta um botão na beira da quadra, os últimos 30 segundos viram um replay. Esse replay é enviado automaticamente para essa API, que guarda o vídeo e deixa ele disponível para o site.

## Tecnologias

- **Python** - linguagem principal
- **FastAPI** - criação da API e dos endpoints
- **Uvicorn** - servidor que roda a API
- **PostgreSQL (Supabase)** - banco de dados na nuvem
- **psycopg2** - conexão do Python com o PostgreSQL
- **Render** - hospedagem da API na internet

## Endpoints

| Método | Endereço | O que faz |
|---|---|---|
| `POST` | `/api/replays` | Recebe um vídeo de replay, salva o arquivo e registra no banco |
| `GET` | `/api/replays` | Lista todos os replays, do mais recente para o mais antigo |

A API está no ar em: https://arenadolla-backend.onrender.com

A documentação interativa (para testar os endpoints pelo navegador) fica em: https://arenadolla-backend.onrender.com/docs

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

4. Crie um arquivo `.env` com o endereço do seu banco PostgreSQL:

```
DATABASE_URL=postgresql://usuario:senha@host:5432/postgres
```

5. Rode o servidor:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

A API vai estar em http://localhost:8001/docs