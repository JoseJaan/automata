from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from core.automata import AutomataManager
from utils.visualization import visualize_automata
from models.automata_models import AutomataCreateRequest, AutomataResponse
import os
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter()

automata_manager = AutomataManager()

data_dir = "automata_images"
os.makedirs(data_dir, exist_ok=True) 

@router.post("/create", response_model=AutomataResponse)
def create_automata(request: AutomataCreateRequest):
    try:
        automata = automata_manager.create_automata(request.type, request.config)
        return AutomataResponse(id=automata.id, type=automata.type, config=automata.config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{automata_id}", response_model=AutomataResponse)
def get_automata(automata_id: str):
    automata = automata_manager.get_automata(automata_id)
    if not automata:
        raise HTTPException(status_code=404, detail="Automata not found")
    return AutomataResponse(id=automata.id, type=automata.type, config=automata.config)

@router.get("/{automata_id}/image")
def get_automata_image(automata_id: str):
    automata = automata_manager.get_automata(automata_id)
    if not automata:
        raise HTTPException(status_code=404, detail="Automata not found")

    # Gerar imagem em memória
    image_stream = BytesIO()
    try:
        diagram = automata.show_diagram()
        diagram.write_png(image_stream)  # Escreve a imagem no stream
        image_stream.seek(0)  # Volta o cursor para o início do stream
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Retorna a imagem como resposta de streaming
    return StreamingResponse(image_stream, media_type="image/png")

