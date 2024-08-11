from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from .prompts import initial_processing_prompt, get_info_prompt, code_gen_prompt
from ..opentrons.instructions import OpentronsInstructions

def create_initial_processing_chain(model):
    def chain(x):
        messages = initial_processing_prompt.format_messages(input=x["input"])
        response = model.invoke(messages)
        return response
    return chain

initial_processing_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
initial_processing_chain = create_initial_processing_chain(initial_processing_model)

get_info_model = ChatOpenAI(model="gpt-4", temperature=0)
get_info_model_with_tool = get_info_model.bind_tools([OpentronsInstructions])
get_info_chain = (
    RunnablePassthrough.assign(
        message_package=lambda x: x["message_package"]
    )
    | get_info_prompt
    | get_info_model_with_tool
)

code_gen_model = ChatOpenAI(model="gpt-4", temperature=0)
code_gen_chain = code_gen_prompt | code_gen_model