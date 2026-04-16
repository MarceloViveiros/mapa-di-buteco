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

# Puxa a variável de ambiente
URL_BANCO = os.getenv("DATABASE_URL")

# 1. Função blindada com Programação Defensiva
def inicializar_banco():
    if not URL_BANCO:
        print("🚨 ERRO CRÍTICO: Variável DATABASE_URL não foi encontrada pelo sistema!")
        return # Sai da função antes de tentar conectar e travar o app
        
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
        print("✅ Banco de dados conectado e inicializado com sucesso!")
    except Exception as e:
        print(f"🚨 Erro ao conectar no banco: {e}")

# Só roda se o arquivo for executado
inicializar_banco()

class Avaliacao(BaseModel):
    nome_bar: str
    nota: int
    comentario: str = ""

# =======================================================
# 🚀 ROTAS DA NOSSA API 
# =======================================================

@app.post("/avaliar")
def salvar_avaliacao(dados: Avaliacao):
    conexao = psycopg2.connect(URL_BANCO)
    cursor = conexao.cursor()
    
    # No PostgreSQL usamos %s em vez de ?
    cursor.execute(
        "INSERT INTO avaliacoes (nome_bar, nota, comentario) VALUES (%s, %s, %s)", 
        (dados.nome_bar, dados.nota, dados.comentario)
    )
    conexao.commit()
    conexao.close() 
    
    return {"mensagem": "Avaliação salva com sucesso e persistida na nuvem!"}

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