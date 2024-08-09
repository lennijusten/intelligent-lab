from pydantic import BaseModel
from typing import List, Dict, Any
from .deck_state import OpentronsDeckState

class OpentronsInstructions(BaseModel):
    workflow: List[Dict[str, Any]]
    deck_state: OpentronsDeckState