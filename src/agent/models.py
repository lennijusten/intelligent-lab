from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from ..opentrons.instructions import OpentronsInstructions

initial_processing_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
initial_processing_chain = RunnablePassthrough() | initial_processing_model

get_info_model = ChatOpenAI(model="gpt-4", temperature=0)
get_info_model_with_tool = get_info_model.bind_tools([OpentronsInstructions])
get_info_chain = RunnablePassthrough() | get_info_model_with_tool

code_gen_model = ChatOpenAI(model="gpt-4", temperature=0)
code_gen_chain = RunnablePassthrough() | code_gen_model