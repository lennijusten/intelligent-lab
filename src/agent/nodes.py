from .state import AgentState
from .models import initial_processing_chain, get_info_chain, code_gen_chain, code_gen_model
from .prompts import initial_processing_template, get_info_template, code_gen_template
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage

def initial_processing_node(state: AgentState):
    processed_command = initial_processing_chain({
        "input": state["messages"][-1].content,
    })
    return {
        "processed_command": processed_command.content,
        "messages": [AIMessage(content=processed_command.content)],
    }

def get_info_node(state: AgentState):
    initial_processing_message = HumanMessage(initial_processing_template)
    initial_user_message = state["messages"][0]
    initial_ai_response = state["messages"][1] # response from initial_processing_node
    get_info_message = HumanMessage(get_info_template)
    follow_up_messages = state["messages"][2:]  # messages from the user and ai after the initial response
    
    message_package = [initial_processing_message, initial_user_message, initial_ai_response, get_info_message,*follow_up_messages]

    result = get_info_chain.invoke({
        "message_package": message_package
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
        # new_message = result if isinstance(result, AIMessage) else AIMessage(content=result)
        print(f"\n================================== AI message ==================================\n{result.content}\n")
        user_input = input("User (q/Q to quit): ")
        print(f"\n================================== Human message ==================================\n{user_input}\n")

        return {
            "messages": [AIMessage(result.content), HumanMessage(content=user_input)],
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