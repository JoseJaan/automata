from fastapi import FastAPI
from api.endpoints import router as automata_router

app = FastAPI()

app.include_router(automata_router, prefix="/automata", tags=["automata"])

@app.get("/")
def read_root():
    return {"message": "Automata API is running!"}