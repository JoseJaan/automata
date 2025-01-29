from pydantic import BaseModel
from typing import Dict, Any

class AutomataCreateRequest(BaseModel):
    type: str
    config: Dict[str, Any]

class AutomataResponse(BaseModel):
    id: str
    type: str
    config: Dict[str, Any]