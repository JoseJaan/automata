from pydantic import BaseModel
from typing import Dict, List, Union, Any

class AutomataConfig(BaseModel):
    states: List[str]
    input_symbols: List[str]
    transitions: Dict[str, Dict[str, Union[str, List[str]]]]
    initial_state: str
    final_states: List[str]

class AutomataCreateRequest(BaseModel):
    type: str
    config: AutomataConfig

class AutomataResponse(BaseModel):
    id: str
    type: str
    config: Dict[str, Any]
    image_url: str  # Nova chave para a URL da imagem
class StringValidationRequest(BaseModel):
    input_string: str