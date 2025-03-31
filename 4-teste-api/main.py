from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Configurar CORS para permitir requisições do frontend Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para o domínio do frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar os dados
df = pd.read_csv("Relatorio_cadop.csv", sep=";", encoding="utf-8")

@app.get("/empresa/{nome}")
def buscar_empresa(nome: str):
    nome = nome.strip().lower()  # Remover espaços extras e padronizar para minúsculas
    empresas = df[df["Razao_Social"].str.lower().str.contains(nome, na=False, regex=False)]  # Busca parcial
    
    if empresas.empty:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    return empresas.fillna("N/A").to_dict(orient="records")  # Retorna todas as correspondências
