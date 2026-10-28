import os  # para ler as variáveis de ambiente
from dotenv import load_dotenv  # para carregar o arquivo .env
from supabase import create_client  # função que cria a conexão com o Supabase

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET = "replays"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def enviar_video(filename, conteudo):
    """Envia o vídeo para o bucket e devolve o link público dele."""
    supabase.storage.from_(BUCKET).upload(
        path=filename,
        file=conteudo,
        file_options={"content-type": "video/mp4"},
    )
    return supabase.storage.from_(BUCKET).get_public_url(filename)