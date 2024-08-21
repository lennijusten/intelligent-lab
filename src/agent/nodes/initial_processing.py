from typing import Dict, Any
from ..state import AgentState
from ..models import initial_processing_chain
from ..prompts import initial_processing_template
from langchain_core.messages import SystemMessage, HumanMessage


def initial_processing_node(state: AgentState, name: str = "initial_processing") -> Dict[str, Any]:
    """
    Initial processing node for the Agent.

    This node processes the user's initial input and generates a structured summary.

    Args:
        state (AgentState): The current state of the agent.
        name (str, optional): The name of the node. Defaults to "initial_processing".

    Returns:
        Dict[str, Any]: Updated state information.
    """
    state["node_history"].append(name)

    if state["default_config"]:
        config_prompt = f"\n\nDefault Opentrons config:\n{state['default_config']}"
    else:
        config_prompt = "\n\nNo default Opentrons config provided."

    state["messages"].extend(
        [SystemMessage(initial_processing_template, additional_kwargs={"node": name}), 
         HumanMessage(state["initial_user_message"] + config_prompt, additional_kwargs={"node": name})])
    response = initial_processing_chain.invoke(state["messages"])
    response.additional_kwargs["node"] = name
    return {"messages": [response]}