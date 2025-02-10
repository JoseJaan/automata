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

last_automata = None 

@router.post("/create", response_model=AutomataResponse)
async def create_automata(request: AutomataCreateRequest):
    global last_automata  

    try:
        print("Received request:", request.dict())  

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

        image_path = os.path.join(data_dir, f"{last_automata.id}")
        image_file = last_automata.generate_image(image_path)

        return {
            "id": last_automata.id,
            "type": last_automata.type,
            "config": last_automata.config,
            "image_url": f"http://localhost:8000/automata/image/{last_automata.id}"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/image/{automata_id}")
async def get_automata_image(automata_id: str):
    print("get_automata_image",automata_id)
    image_path = os.path.join(data_dir, f"{automata_id}.png")
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    return FileResponse(image_path, media_type="image/png")

@router.post("/validate")
def validate_string(request: StringValidationRequest):
    print("Received request:", request) 
    global last_automata
    if not last_automata:
        raise HTTPException(status_code=400, detail="Nenhum autômato criado ainda")
    try:
        result = last_automata.validate_string(request.input_string)
        return {"input": request.input_string, "accepted": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))