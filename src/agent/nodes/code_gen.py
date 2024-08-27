from typing import Dict, Any
from ..state import AgentState
from ..models import code_gen_chain
from ..prompts import code_gen_template
from langchain_core.messages import HumanMessage

def code_gen_node(state: AgentState, name: str = "code_gen") -> Dict[str, Any]:
    """
    Code generation node for the Agent.

    This node generates Python code for the Opentrons API based on the processed information.

    Args:
        state (AgentState): The current state of the agent.
        name (str, optional): The name of the node. Defaults to "code_gen".

    Returns:
        Dict[str, Any]: Updated state information.
    """
    state["node_history"].append(name)

    if state["node_history"].count(name) == 1:
        state["messages"].append(HumanMessage(code_gen_template, additional_kwargs={"node": name}))

    response = code_gen_chain.invoke(state["messages"])
    response.additional_kwargs["node"] = name
    print(f"\n{'=' * 34} Current code {'=' * 34}\n{response.content}\n")
    return {"messages": [response], "current_code": response.content}
