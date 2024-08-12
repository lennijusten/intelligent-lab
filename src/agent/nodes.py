from .state import AgentState
from .models import initial_processing_chain, get_info_chain, code_gen_chain
from .prompts import initial_processing_template, get_info_template, code_gen_template
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage

def initial_processing_node(state: AgentState, name="initial_processing"):
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

def get_info_node(state: AgentState, name="get_info"):
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
            name=tool_call['name']
        )
        tool_message.additional_kwargs["node"] = name
        
        # print(f"\n================================== AI tool call ==================================\n{tool_message.content}\n")
        return {"messages": [response, tool_message], "awaiting_human_input": False}
    elif isinstance(response, AIMessage):
        print(f"\n================================== AI message ==================================\n{response.content}\n")
        user_input = input("User (q/Q to quit): ")
        print(f"\n================================== Human message ==================================\n{user_input}\n")

        return {
            "messages": [response, HumanMessage(content=user_input, additional_kwargs={"node": name})], 
            "awaiting_human_input": False,}
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")
    
def code_gen_node(state: AgentState, name="code_gen"):
    state["node_history"].append(name)

    if state["node_history"].count(name) == 1:
        state["messages"].append(HumanMessage(code_gen_template, additional_kwargs={"node": name}))

    response = code_gen_chain.invoke(state["messages"])
    response.additional_kwargs["node"] = name
    print(f"\n================================== Current code ==================================\n{response.content}\n")
    return {
        "messages": [response],
        "awaiting_human_input": True,
        "current_code": response.content
        }

def code_refinement_node(state: AgentState, name="code_refinement"):
    state["node_history"].append(name)

    user_input = input("Provide feedback on the code (or type 'y' to accept): ")
    
    if user_input.upper() == 'Y':
        return {
            "messages": state["messages"],
            "awaiting_human_input": False,
            "code_to_run": state["current_code"]  # Store the approved code
        }
    
    print(f"\n================================== Human message ==================================\n{user_input}\n")
    
    refined_code = code_gen_chain.invoke(state["messages"])
    refined_code.additional_kwargs["node"] = name
    print(f"\n================================== Current Code ==================================\n{refined_code.content}\n")
    
    return {
        "messages": [HumanMessage(user_input, additional_kwargs={"node": name}), refined_code],
        "awaiting_human_input": True,
        "current_code": refined_code.content  # Update the current code
    }