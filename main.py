import argparse
import json
import uuid
from dotenv import load_dotenv

from src.agent.graph import create_graph
from langgraph.checkpoint.sqlite import SqliteSaver

def load_config(path: str) -> str:
    """Load and parse a JSON configuration file."""
    with open(path, 'r') as f:
        return json.dumps(json.load(f))  # Convert to JSON string

def main():
    # Load environment variables
    load_dotenv()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="PyLabRobot Agent")
    parser.add_argument("--config", type=str, help="Path to the deck configuration file")
    args = parser.parse_args()

    graph = create_graph()
    memory = SqliteSaver.from_conn_string(":memory:")
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    # Load deck configuration
    default_config = load_config(args.config) if args.config else None

    while True:
        print("\nAI: Hello! I'm an intelligent liquid handling assistant. How can I help you today?\n")
        print(f"\n{'=' * 34} Human message {'=' * 34}\n")
        user_input = input("User (q/Q to quit): ")
        if user_input.lower() == 'q':
            # TODO: implement quitting at any time
            print("AI: Goodbye!")
            break
        
        initial_state = {
            "initial_user_message": user_input,
            "messages": [],
            "node_history": [],
            "default_config": default_config,
            "deck_state": {
                "pipettes": {},
                "labware": {},
                "tip_racks": {},
                "modules": {}
            },
            "info_gathering_complete": False,
            "code_refining_complete": False,
            "identified_concepts": [],
            "current_code": "",
            "code_to_run": ""
        }

        # stream the graph without handling intermediate outputs
        list(graph.stream(initial_state, config=config))

        print("\nDone!")
        break

if __name__ == "__main__":
    main()