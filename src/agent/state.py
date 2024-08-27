from typing import List, TypedDict, Annotated
from .tools import DeckState
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    Represents the state of the Agent.

    This class defines the structure of the agent's state, including message history,
    node execution history, and current code status.
    """
    initial_user_message: str
    messages: Annotated[List[BaseMessage], operator.add]
    node_history: Annotated[List[str], operator.add]
    default_config: str
    deck_state: DeckState
    info_gathering_complete: bool
    code_refining_complete: bool
    identified_concepts: List[str]
    current_code: str
    code_to_run: str