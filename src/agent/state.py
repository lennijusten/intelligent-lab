from typing import List, TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    default_config: str
    processed_command: str
    awaiting_human_input: bool
    current_code: str
    code_to_run: str