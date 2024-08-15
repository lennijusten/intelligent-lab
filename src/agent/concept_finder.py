# src/agent/concept_finder.py

import os
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage

AVAILABLE_CONCEPTS = [
    "thermocycler", "transfer", "blow_out", "discard_tip"
]

def load_concept_content(concept: str, concepts_dir: str) -> str:
    file_path = os.path.join(concepts_dir, f"{concept}.md")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""

concept_finder_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def find_concepts(messages: List[BaseMessage]) -> List[str]:
    response = concept_finder_model.invoke(messages)
    concepts = [concept.strip() for concept in response.content.split(',')]
    return [concept for concept in concepts if concept in AVAILABLE_CONCEPTS] # TODO enforce JSON output

def get_concept_information(concepts: List[str], concepts_dir: str) -> Dict[str, str]:
    return {concept: load_concept_content(concept, concepts_dir) for concept in concepts}