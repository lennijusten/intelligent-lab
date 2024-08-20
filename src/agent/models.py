from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from .tools import LiquidHandlerInstructions, RelevantConcepts

initial_processing_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
initial_processing_chain = RunnablePassthrough() | initial_processing_model

get_info_model = ChatOpenAI(model="gpt-4", temperature=0)
get_info_model_with_tool = get_info_model.bind_tools([LiquidHandlerInstructions])
get_info_chain = RunnablePassthrough() | get_info_model_with_tool

concept_finder_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
concept_finder_model_with_tool = concept_finder_model.bind_tools([RelevantConcepts])
concept_finder_chain = RunnablePassthrough() | concept_finder_model_with_tool

code_gen_model = ChatOpenAI(model="gpt-4", temperature=0)
code_gen_chain = RunnablePassthrough() | code_gen_model