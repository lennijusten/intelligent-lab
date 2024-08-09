from langgraph.graph import StateGraph, START, END
from langchain_core.messages import ToolMessage
from .nodes import initial_processing_node, get_info_node, code_gen_node, code_refinement_node
from .state import AgentState

def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("initial_processing", initial_processing_node)
    workflow.add_node("get_info", get_info_node)
    workflow.add_node("code_gen", code_gen_node)
    workflow.add_node("code_refinement", code_refinement_node)

    workflow.add_edge(START, "initial_processing")
    workflow.add_edge("initial_processing", "get_info")
    workflow.add_conditional_edges(
        "get_info",
        lambda x: "code_gen" if any(isinstance(m, ToolMessage) for m in x["messages"]) else "get_info"
    )
    workflow.add_edge("code_gen", "code_refinement")
    workflow.add_conditional_edges(
        "code_refinement",
        lambda x: "code_refinement" if x["awaiting_human_input"] else END
    )

    return workflow.compile()