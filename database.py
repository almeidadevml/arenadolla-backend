import os
import psycopg2  #a biblioteca que faz o python conversar com o PostgreeSQL
from psycopg2.extras import RealDictCursor  #devolve cada linha de dados como um dicionario 
from dotenv import load_dotenv  #a função que vai ler o arquivo .env 

load_dotenv() #executa a leitura, carregando as variáveis do .env pro ambiente do programa (precisa ser chamado antes de tentar usar os.environ.get)

DATABASE_URL = os.environ.get("DATABASE_URL")  #pega o valor colocado no .env, guardando na variável DATABASE_URL 


def get_connection(): 
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)  


def init_db():  #função que vai ser chamada uma vez, quando o servidor ligar, pra garantir que a tabela existe
        conn = get_connection()  #abre uma conexão nova, usando a função
        cur = conn.cursor()  #um cursor é o "objeto" que é usado pra executar comandos SQL

        cur.execute("""   
                CREATE TABLE IF NOT EXISTS replays (
                        id TEXT PRIMARY KEY,
                        filename  TEXT NOT NULL,
                        url_video TEXT NOT NULL,
                        duracao_segundos INTEGER,
                        criado_em TIMESTAMP DEFAULT NOW()
                )
        """) 

        conn.commit()  #confirma as mudanças no banco. No PostgreSQL
        cur.close()  
        conn.close()


def salvar_replay(replay_id, filename, url_video, duracao_segundos):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO replays (id, filename, url_video, duracao_segundos)
        VALUES (%s, %s, %s, %s)
        """,
        (replay_id, filename, url_video, duracao_segundos),
    )

    conn.commit()
    cur.close()
    conn.close()


def listar_replays():
       conn = get_connection()
       cur = conn.cursor()

       cur.execute(
       """
       SELECT id, filename, url_video, duracao_segundos, criado_em
       FROM replays
       ORDER BY criado_em DESC
       """      
        )

       rows = cur.fetchall()

       cur.close()
       conn.close()

       return rows
