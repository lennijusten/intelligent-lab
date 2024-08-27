from typing import Dict, Any
from ..state import AgentState
from ..models import get_info_chain
from ..prompts import get_info_template
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage

def get_info_node(state: AgentState, name: str = "get_info") -> Dict[str, Any]:
    """
    Information gathering node for the Agent.

    This node determines if more information is needed and either asks questions or generates instructions.

    Args:
        state (AgentState): The current state of the agent.
        name (str, optional): The name of the node. Defaults to "get_info".

    Returns:
        Dict[str, Any]: Updated state information.
    """
    state["node_history"].append(name)
    
    # Only add the system message the first time entering the node
    if state["node_history"].count(name) == 1:
        state["messages"].append(SystemMessage(get_info_template, additional_kwargs={"node": name}))

    response = get_info_chain.invoke(state["messages"])
    response.additional_kwargs["node"] = name

    if not response.tool_calls:
        raise Warning(f"Expected tool call in response but got {response}")

    tool_call = response.tool_calls[0]
    tool_message = ToolMessage(
        content=str(tool_call['args']),
        tool_call_id=tool_call['id'],
        name=tool_call['name'],
        additional_kwargs={"node": name}
    )
    print(f"\n{'=' * 34} AI tool call {'=' * 34}\n{tool_message.content}\n")

    tool_output = tool_call["args"]
    state["deck_state"] = tool_output["deck_state"]
    
    if tool_output["info_complete"]:
        print(f"\n{'=' * 34} AI message {'=' * 34}\nAll necessary information has been gathered.\n")
        return {"messages": [response, tool_message], "info_gathering_complete": True}
    else:
        if tool_output["questions"]:
            print(f"\n{'=' * 34} AI message {'=' * 34}\n{tool_output['questions']}\n")
            print(f"\n{'=' * 34} Human message {'=' * 34}\n")
            user_input = input("User (q/Q to quit): ")

            if user_input.lower() == 'q':
                raise KeyboardInterrupt("User requested to quit.")
            
            return {"messages": [response, tool_message, HumanMessage(content=user_input, additional_kwargs={"node": name})]}
        else:
            raise Warning("Model responded info_complete=False but no questions were generated for the user.")
            return {"messages": [response, tool_message]}
        