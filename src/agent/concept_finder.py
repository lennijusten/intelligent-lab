# src/agent/concept_finder.py

import os
from pydantic import BaseModel, Field
from typing import List, Dict

AVAILABLE_CONCEPTS = [
    "thermocycler_module", "temperature_controller_module", "transfer", "blow_out", "discard_tip"
]

class RelevantConcepts(BaseModel):
    concepts: List[str] = Field(default_factory=list, description="A list of relevant concepts to complete the user command")

def load_concept_content(concept: str, concepts_dir: str) -> str:
    file_path = os.path.join(concepts_dir, f"{concept}.md")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""

def get_concept_information(concepts: List[str], concepts_dir: str) -> Dict[str, str]:
    return {concept: load_concept_content(concept, concepts_dir) for concept in concepts}