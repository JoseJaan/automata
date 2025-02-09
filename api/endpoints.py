from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from core.automata import AutomataManager
from utils.visualization import visualize_automata
from models.automata_models import AutomataCreateRequest, AutomataResponse, StringValidationRequest
import os
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter()

automata_manager = AutomataManager()

data_dir = "automata_images"
os.makedirs(data_dir, exist_ok=True) 

last_automata = None  # Armazena o último autômato criado

@router.post("/create", response_model=AutomataResponse)
async def create_automata(request: AutomataCreateRequest):
    try:
        print("Received request:", request.dict())  # Debug log
        
        # Validação adicional
        if not request.config.states:
            raise ValueError("States list cannot be empty")
        if not request.config.input_symbols:
            raise ValueError("Input symbols list cannot be empty")
        if not request.config.transitions:
            raise ValueError("Transitions dictionary cannot be empty")
        if request.config.initial_state not in request.config.states:
            raise ValueError("Initial state must be in states list")
        for final_state in request.config.final_states:
            if final_state not in request.config.states:
                raise ValueError(f"Final state {final_state} must be in states list")
        
        last_automata = automata_manager.create_automata(request.type, request.config.dict())
        return AutomataResponse(
            id=last_automata.id,
            type=last_automata.type,
            config=last_automata.config
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("Error:", str(e))  # Debug log
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        
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

    image_stream = BytesIO()
    try:
        diagram = automata.show_diagram()
        diagram.write_png(image_stream) 
        image_stream.seek(0)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return StreamingResponse(image_stream, media_type="image/png")

@router.post("/validate")
def validate_string(request: StringValidationRequest):
    print("Received request:", request)  # Add this line
    global last_automata
    if not last_automata:
        raise HTTPException(status_code=400, detail="Nenhum autômato criado ainda")
    try:
        result = last_automata.validate_string(request.input_string)
        return {"input": request.input_string, "accepted": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))