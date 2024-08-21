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

    if isinstance(response, AIMessage) and response.tool_calls:
        # If the content is empty, add a default message
        if not response.content:
            response.content = "Using the LiquidHandlerInstructions tool to generate the protocol."
            
        tool_call = response.tool_calls[0]

        if tool_call['name'] != 'LiquidHandlerInstructions':
            raise ValueError(f"Unexpected tool call name: {tool_call['name']}. Expected 'LiquidHandlerInstructions'.")

        tool_message = ToolMessage(
            # todo: may be better way to convert tool_call to ToolMessage
            content=str(tool_call['args']),
            tool_call_id=tool_call['id'],
            name=tool_call['name'],
            additional_kwargs = {"node": name}
            )
        
        print(f"\n{'=' * 34} AI tool call {'=' * 34}\n{tool_message.content}\n")
        return {"messages": [response, tool_message], "awaiting_human_input": False}
    elif isinstance(response, AIMessage):
        # TODO implement check for failed tool calls where the model outputs string version of tool call
        print(f"\n{'=' * 34} AI message {'=' * 34}\n{response.content}\n")
        print(f"\n{'=' * 34} Human message {'=' * 34}\n")
        user_input = input("User (q/Q to quit): ")

        return {
            "messages": [response, HumanMessage(content=user_input, additional_kwargs={"node": name})], 
            "awaiting_human_input": False,
        }
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")