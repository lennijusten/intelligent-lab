from langgraph.graph import StateGraph, START, END
from langchain_core.messages import ToolMessage

from .nodes import initial_processing_node, concept_finder_node, get_info_node, code_gen_node, simulate_node, code_refinement_node
from .state import AgentState

def create_graph() -> StateGraph:
    """
    Create and configure the StateGraph for the Agent.

    This function sets up the nodes and edges of the graph, defining the
    workflow for processing liquid handling tasks.

    Returns:
        StateGraph: The compiled graph ready for execution.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("initial_processing", initial_processing_node)
    workflow.add_node("get_info", get_info_node)
    workflow.add_node("concept_finder", concept_finder_node)
    workflow.add_node("code_gen", code_gen_node)
    workflow.add_node("simulate", simulate_node)
    workflow.add_node("code_refinement", code_refinement_node)

    workflow.add_edge(START, "initial_processing")
    workflow.add_edge("initial_processing", "get_info")
    workflow.add_conditional_edges(
        "get_info",
        lambda x: "concept_finder" if x["info_gathering_complete"] else "get_info"
    )
    workflow.add_edge("concept_finder", "code_gen")
    workflow.add_edge("code_gen", "simulate")
    workflow.add_conditional_edges(
        "simulate",
        lambda x: "code_refinement" if not x["awaiting_human_input"] else "simulate"
    )
    workflow.add_conditional_edges(
        "code_refinement",
        lambda x: END if x["code_refining_complete"] else "code_refinement"
    )

    return workflow.compile()