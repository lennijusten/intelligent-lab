from typing import Dict, Any
import subprocess
import os
from ..state import AgentState
from langchain_core.messages import HumanMessage

def simulate_node(state: AgentState, name: str = "simulate") -> Dict[str, Any]:
    """
    Simulation node for the Agent.

    This node simulates the Opentrons protocol, saves the log, and re-generates the code if needed.

    Args:
        state (AgentState): The current state of the agent.
        name (str, optional): The name of the node. Defaults to "simulate".

    Returns:
        Dict[str, Any]: Updated state information.
    """
    state["node_history"].append(name)

    # Save the current code to a .py file
    protocol_file = "my_protocol.py"
    with open(protocol_file, "w") as f:
        f.write(state["current_code"])

    # Run the simulation
    try:
        result = subprocess.run(
            ["opentrons_simulate", protocol_file],
            capture_output=True,
            text=True,
            check=True
        )
        simulation_log = result.stdout
        state["simulation_log"] = simulation_log
        print(f"\n{'=' * 34} Simulation Log {'=' * 34}\n{simulation_log}\n")

        # Check for errors in the simulation log
        if "error" in simulation_log.lower():
            # Re-generate the code using the code_refinement node
            return {
                "messages": state["messages"],
                "simulation_log": simulation_log,
                "awaiting_human_input": True
            }
        else:
            # Pass to code_refinement node for user feedback
            return {
                "messages": state["messages"],
                "simulation_log": simulation_log,
                "awaiting_human_input": False
            }

    except subprocess.CalledProcessError as e:
        print(f"Simulation failed: {e.stderr}")
        return {
            "messages": state["messages"],
            "simulation_log": e.stderr,
            "awaiting_human_input": True
        }
    finally:
        # Clean up the protocol file
        os.remove(protocol_file)

