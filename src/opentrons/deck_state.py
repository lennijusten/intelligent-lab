from pydantic import BaseModel, Field
from typing import Dict

class OpentronsDeckState(BaseModel):
    pipettes: Dict[str, str] = Field(default_factory=dict, description="Pipettes attached to the robot")
    labware: Dict[str, str] = Field(default_factory=dict, description="Labware on the deck")
    tip_racks: Dict[str, str] = Field(default_factory=dict, description="Tip racks on the deck")
    modules: Dict[str, str] = Field(default_factory=dict, description="Modules attached to the deck")