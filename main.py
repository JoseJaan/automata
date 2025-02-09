from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.endpoints import router as automata_router
import os

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Permite requisições do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir os endpoints do automata
app.include_router(automata_router, prefix="/automata", tags=["automata"])

# Servindo arquivos estáticos da pasta 'frontend'
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Rota para carregar a página inicial (index.html)
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")
