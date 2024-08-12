from typing import List, TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    node_history: Annotated[List[str], operator.add]
    default_config: str
    awaiting_human_input: bool
    current_code: str
    code_to_run: str