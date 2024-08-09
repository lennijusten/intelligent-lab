from langchain_openai import ChatOpenAI
from .prompts import initial_processing_prompt, get_info_prompt, code_gen_prompt
from ..opentrons.instructions import OpentronsInstructions

initial_processing_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
initial_processing_chain = initial_processing_prompt | initial_processing_model

get_info_model = ChatOpenAI(model="gpt-4", temperature=0)
get_info_model_with_tool = get_info_model.bind_tools([OpentronsInstructions])
get_info_chain = (
    {
        "initial_user_command": lambda x: x["initial_user_command"],
        "processed_command": lambda x: x["processed_command"],
        "default_config": lambda x: x["default_config"],
        "follow_up_messages": lambda x: x["follow_up_messages"]
    }
    | get_info_prompt
    | get_info_model_with_tool
)

code_gen_model = ChatOpenAI(model="gpt-4", temperature=0)
code_gen_chain = code_gen_prompt | code_gen_model