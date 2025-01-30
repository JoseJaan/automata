from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as automata_router

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Permite requisições do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(automata_router, prefix="/automata", tags=["automata"])

@app.get("/")
def read_root():
    return {"message": "Automata API is running!"}