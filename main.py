import os  #funções do sistema operacional (criar pastas, etc.)
import uuid  #gera identificadores únicos (tipo a1b2c3d4-...)
from datetime import datetime  #guardar a data/hora de quando o replay foi enviado

from fastapi import FastAPI, UploadFile, File  
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, salvar_replay, listar_replays
from storage import enviar_video # envia o vídeo para o bucket do Supabase

# --- Configuração ---

init_db()

app = FastAPI(title="Arena Dolla - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.post("/api/replays")
async def upload_replay(video: UploadFile = File(...), duracao_segundos: int = 30):
    replay_id = str(uuid.uuid4())
    extension = os.path.splitext(video.filename)[1]
    filename =  f"{replay_id}{extension}"

    conteudo = await video.read()
    url_video = enviar_video(filename, conteudo)

    salvar_replay(replay_id, filename, url_video, duracao_segundos)

    return {
        "ok": True,
        "id": replay_id,
        "filename": filename,
        "url": url_video, 
    }

@app.get("/api/replays")
def get_replays():
    replays = listar_replays()
    return {"replays": replays}