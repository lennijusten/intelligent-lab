from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DeckState(BaseModel):
    pipettes: Dict[str, str] = Field(default_factory=dict, description="Pipettes attached to the robot")
    labware: Dict[str, str] = Field(default_factory=dict, description="Labware on the deck")
    tip_racks: Dict[str, str] = Field(default_factory=dict, description="Tip racks on the deck")
    modules: Dict[str, str] = Field(default_factory=dict, description="Modules attached to the deck")

class RelevantConcepts(BaseModel):
    concepts: List[str] = Field(default_factory=list, description="A list of relevant concepts to complete the user command")

class UpdateDeckState(BaseModel):
    """Update the current deck state based on the information gathered."""
    deck_state: DeckState
