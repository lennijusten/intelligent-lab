import os
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from ..state import AgentState
from ..models import concept_finder_chain
from ..prompts import concept_finder_template
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

AVAILABLE_CONCEPTS = [
    "plate_reading", "centrifuge", "transfer", "blow_out", "discard_tip" # instead, add a node that retrieves the different robots being used, this will narrow down AVAILABLE_CONCEPTS
]

def load_concept_content(concept: str, concepts_dir: str) -> str:
    file_path = os.path.join(concepts_dir, f"{concept}.md")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""

def get_concept_information(concepts: List[str], concepts_dir: str) -> Dict[str, str]:
    return {concept: load_concept_content(concept, concepts_dir) for concept in concepts}

def concept_finder_node(state: AgentState, name: str = "concept_finder") -> Dict[str, Any]:
    """
    Concept finder node for the Agent.

    This node identifies relevant concepts from a predefined list based on the current message history.
    It utilizes a language model with a Pydantic RelevantConcepts tool to select applicable concepts.
    For each identified concept, it retrieves and compiles associated information.

    Args:
        state (AgentState): The current state of the agent.
        name (str, optional): The name of the node. Defaults to "concept_finder".

    Returns:
        Dict[str, Any]: Updated state information including identified concepts and their associated information.
    """
    state["node_history"].append(name)

    concept_finder_prompt = concept_finder_template.format(available_concepts=", ".join(AVAILABLE_CONCEPTS))
    state["messages"].append(HumanMessage(content=concept_finder_prompt, additional_kwargs={"node": name}))

    response = concept_finder_chain.invoke(state["messages"])
    response.additional_kwargs["node"] = name

    if isinstance(response, AIMessage) and response.tool_calls:
        # If the content is empty, add a default message
        if not response.content:
            response.content = "Using the RelevantConcepts tool to list concept keywords."
            
        tool_call = response.tool_calls[0]
        if tool_call['name'] == 'RelevantConcepts':
            
            tool_message = ToolMessage(
                # todo: may be better way to convert tool_call to ToolMessage
                content=str(tool_call['args']),
                tool_call_id=tool_call['id'],
                name=tool_call['name'],
                additional_kwargs = {"node": name}
            )
            
            identified_concepts = tool_call['args']['concepts']
            concept_info = get_concept_information(identified_concepts, "src/plr/concepts")

            concept_summary = "Identified concepts and their information:\n"
            for _, info in concept_info.items():
                concept_summary += f"{info}\n"

            concept_message = AIMessage(content=concept_summary, additional_kwargs={"node": name})

            print(f"\n{'=' * 34} AI tool call {'=' * 34}\n{tool_message.content}\n")
            return {
                "messages": [response, tool_message, concept_message],
                "identified_concepts": identified_concepts,
            }
        else:
            raise ValueError(f"Unexpected tool call: {tool_call['name']}. Expected 'RelevantConcepts'.")
    else:
        raise ValueError("Model did not use the tool as instructed")