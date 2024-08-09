from .state import AgentState
from .models import initial_processing_chain, get_info_chain, code_gen_chain, code_gen_model
from .prompts import code_gen_template
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage

def initial_processing_node(state: AgentState):
    processed_command = initial_processing_chain.invoke({
        "input": state["messages"][-1].content,
        "default_config": state["default_config"]
    })
    return {
        "processed_command": processed_command.content,
        "messages": state["messages"] + [AIMessage(content=processed_command.content)]
    }

def get_info_node(state: AgentState):
    initial_user_command = state["messages"][0].content if state["messages"] else ""
    follow_up_messages = state["messages"][2:] if len(state["messages"]) > 2 else []
    
    result = get_info_chain.invoke({
        "initial_user_command": initial_user_command,
        "processed_command": state["processed_command"],
        "default_config": state["default_config"],
        "follow_up_messages": follow_up_messages
    })

    if isinstance(result, AIMessage) and result.tool_calls:
        # If the content is empty, add a default message
        if not result.content:
            result.content = "Using the OpentronsInstructions tool to generate the protocol."
        
        # Handle tool calls
        tool_messages = []
        for tool_call in result.tool_calls:
            if tool_call['name'] == "OpentronsInstructions":
                # Execute the OpentronsInstructions tool
                # tool_result = OpentronsInstructions(**tool_call['args'])
                tool_message = ToolMessage(
                    content=str(tool_call['args']),
                    tool_call_id=tool_call['id'],
                    name="OpentronsInstructions"
                )
                tool_messages.append(tool_message)
        
        print(f"\n================================== AI tool call ==================================\n{[msg.content for msg in tool_messages]}\n")
        return {"messages": state["messages"] + [result] + tool_messages, "awaiting_human_input": False}
    elif isinstance(result, (str, AIMessage)):
        new_message = result if isinstance(result, AIMessage) else AIMessage(content=result)
        print(f"\n================================== AI message ==================================\n{new_message.content}\n")
        user_input = input("User (q/Q to quit): ")
        print(f"\n================================== Human message ==================================\n{user_input}\n")
        return {
            "messages": state["messages"] + [new_message, HumanMessage(content=user_input)],
            "awaiting_human_input": False
        }
    else:
        raise ValueError(f"Unexpected result type: {type(result)}")
    
def code_gen_node(state: AgentState):
    # TODO make sure the code_gen module has access to the initial user command or just generally optimize this.

    instructions = next(msg.content for msg in reversed(state["messages"]) if isinstance(msg, ToolMessage))
    code = code_gen_chain.invoke({"instructions": instructions})
    print(f"\n================================== Current code ==================================\n{code.content}\n")
    return {
        "messages": state["messages"] + [AIMessage(content=code.content)],
        "awaiting_human_input": True,
        "current_code": code.content
        }

def code_refinement_node(state: AgentState):
    # Find the index of the OpentronsInstructions tool message
    # start_index = next((i for i, msg in enumerate(state["messages"]) 
    #                     if isinstance(msg, ToolMessage) and msg.name == "OpentronsInstructions"), None)
    
    # if start_index is None:
    #     return {"messages": state["messages"], "awaiting_human_input": False}
    start_index = 0

    relevant_messages = state["messages"][start_index:]
    
    # Get the current code from the state
    current_code = state.get("current_code")
    
    user_input = input("Provide feedback on the code (or type 'ACCEPT' to finish): ")
    
    if user_input.upper() == 'ACCEPT':
        return {
            "messages": state["messages"],
            "awaiting_human_input": False,
            "code_to_run": current_code  # Store the approved code
        }
    
    print(f"\n================================== Human message ==================================\n{user_input}\n")

    # Use the existing code_gen_model for refinement, including all relevant messages
    system_message = SystemMessage(content=code_gen_template)
    refined_code = code_gen_model.invoke([system_message] + relevant_messages + [HumanMessage(content=user_input)])
    
    print(f"\n================================== Current Code ==================================\n{refined_code.content}\n")
    
    return {
        "messages": state["messages"] + [HumanMessage(content=user_input), refined_code],
        "awaiting_human_input": True,
        "current_code": refined_code.content  # Update the current code
    }