from typing import Dict, Any
from .state import AgentState
from .models import initial_processing_chain, concept_finder_chain, get_info_chain, code_gen_chain
from .prompts import initial_processing_template, concept_finder_template, get_info_template, code_gen_template
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from .concept_finder import get_concept_information, AVAILABLE_CONCEPTS

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

def concept_finder_node(state: AgentState, name: str = "concept_finder") -> Dict[str, Any]:
    state["node_history"].append(name)

    concept_finder_prompt = concept_finder_template.format(available_concepts=", ".join(AVAILABLE_CONCEPTS))
    state["messages"].append(HumanMessage(content=concept_finder_prompt, additional_kwargs={"node": name}))

    response = concept_finder_chain.invoke(state["messages"])
    response.additional_kwargs["node"] = name

    if isinstance(response, AIMessage) and response.tool_calls:
        # If the content is empty, add a default message
        if not response.content:
            response.content = "Using the RelevantConcepts tool to list concept keywords."
        
        # Handle tool calls
        if len(response.tool_calls) > 1:
            raise ValueError("Expected only one tool call, but got multiple.")
            
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
            concept_info = get_concept_information(identified_concepts, "src/opentrons/concepts")

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
            response.content = "Using the OpentronsInstructions tool to generate the protocol."
        
        # Handle tool calls
        if len(response.tool_calls) > 1:
            raise ValueError("Expected only one tool call, but got multiple.")
            
        tool_call = response.tool_calls[0]

        if tool_call['name'] != 'OpentronsInstructions':
            raise ValueError(f"Unexpected tool call name: {tool_call['name']}. Expected 'OpentronsInstructions'.")

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
        print(f"\n{'=' * 34} AI message {'=' * 34}\n{response.content}\n")
        user_input = input("User (q/Q to quit): ")
        print(f"\n{'=' * 34} Human message {'=' * 34}\n{user_input}\n")

        return {
            "messages": [response, HumanMessage(content=user_input, additional_kwargs={"node": name})], 
            "awaiting_human_input": False,
        }
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")
    
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
    return {
        "messages": [response],
        "awaiting_human_input": True,
        "current_code": response.content
        }

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