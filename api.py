import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI(title="API Mapa di Buteco")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

URL_BANCO = os.getenv("DATABASE_URL")

# --- ROTA DE PING (ADICIONADA AQUI) ---
@app.get("/ping")
def ping():
    return {"status": "viva!", "banco_configurado": URL_BANCO is not None}

def inicializar_banco():
    if not URL_BANCO:
        print("🚨 ERRO CRÍTICO: Variável DATABASE_URL não encontrada!")
        return 
        
    try:
        conexao = psycopg2.connect(URL_BANCO)
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id SERIAL PRIMARY KEY,
                nome_bar TEXT,
                nota INTEGER,
                comentario TEXT
            )
        ''')
        conexao.commit()
        conexao.close()
        print("✅ Banco de dados conectado com sucesso!")
    except Exception as e:
        print(f"🚨 Erro ao conectar no banco: {e}")

inicializar_banco()

class Avaliacao(BaseModel):
    nome_bar: str
    nota: int
    comentario: str = ""

# =======================================================
# 🚀 ROTAS DE AVALIAÇÃO
# =======================================================

@app.post("/avaliar")
def salvar_avaliacao(dados: Avaliacao):
    conexao = psycopg2.connect(URL_BANCO)
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO avaliacoes (nome_bar, nota, comentario) VALUES (%s, %s, %s)", 
        (dados.nome_bar, dados.nota, dados.comentario)
    )
    conexao.commit()
    conexao.close() 
    return {"mensagem": "Avaliação salva com sucesso!"}

@app.get("/avaliacoes/{nome_bar}")
def ler_avaliacoes(nome_bar: str):
    conexao = psycopg2.connect(URL_BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT nota, comentario FROM avaliacoes WHERE nome_bar = %s", (nome_bar,))
    resultados = cursor.fetchall()
    conexao.close() 
    
    if not resultados:
        return {"media": 0, "total_avaliacoes": 0, "comentarios": []}
    
    soma_notas = sum([linha[0] for linha in resultados])
    media = soma_notas / len(resultados)
    comentarios = [linha[1] for linha in resultados if linha[1] != ""]
    
    return {
        "media": round(media, 1),
        "total_avaliacoes": len(resultados),
        "comentarios": comentarios
    }