from typing import Dict, Any
from ..state import AgentState
from ..models import code_gen_chain
from langchain_core.messages import HumanMessage

def code_refinement_node(state: AgentState, name: str = "code_refinement") -> Dict[str, Any]:
    """
    Code refinement node for the Agent.

    This node allows for user feedback and code refinement.

    Args:
        state (AgentState): The current state of the agent.
        name (str, optional): The name of the node. Defaults to "code_refinement".

    Returns:
        Dict[str, Any]: Updated state information.
    """
    state["node_history"].append(name)

    print(f"\n{'=' * 34} Human message {'=' * 34}\n")
    user_input = input("Provide feedback on the code (or type 'y' to accept): ")
    
    if user_input.upper() == 'Y':
        return {
            "messages": state["messages"],
            "awaiting_human_input": False,
            "code_to_run": state["current_code"]  # Store the approved code
        }
    
    print(f"\n{'=' * 34} Human message {'=' * 34}\n{user_input}\n")
    
    refined_code = code_gen_chain.invoke(state["messages"])
    refined_code.additional_kwargs["node"] = name
    print(f"\n{'=' * 34} Current Code {'=' * 34}\n{refined_code.content}\n")
    
    return {
        "messages": [HumanMessage(content=user_input, additional_kwargs={"node": name}), refined_code],
        "awaiting_human_input": True,
        "current_code": refined_code.content
    }