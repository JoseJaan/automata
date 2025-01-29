from fastapi import APIRouter, HTTPException
from core.automata import AutomataManager
from models.automata_models import AutomataCreateRequest, AutomataResponse

router = APIRouter()

automata_manager = AutomataManager()

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