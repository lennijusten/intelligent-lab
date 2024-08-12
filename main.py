import argparse
import json
import uuid
from dotenv import load_dotenv

from src.agent.graph import create_graph
from src.agent.prompts import initial_processing_template
from langchain_core.messages import HumanMessage, SystemMessage 
from langgraph.checkpoint.sqlite import SqliteSaver

def load_config(path: str) -> str:
    with open(path, 'r') as f:
        return json.dumps(json.load(f))  # Convert to JSON string

def main():
    # Load environment variables
    load_dotenv()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Opentrons Agent")
    parser.add_argument("--config", type=str, help="Path to the deck configuration file")
    args = parser.parse_args()

    graph = create_graph()
    memory = SqliteSaver.from_conn_string(":memory:")
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    # Load deck configuration
    if args.config:
        default_config = load_config(args.config)
        config_prompt = f"\n\nDefault Opentrons config:\n{default_config}"
    else:
        default_config = None
        config_prompt = "\n\nNo default Opentrons config provided."

    while True:
        print("\nAI: Hello! I'm an intelligent liquid handling assistant. How can I help you today?\n")
        user_input = input("User (q/Q to quit): ")
        if user_input.lower() == 'q':
            # TODO: implement quitting at any time
            print("AI: Goodbye!")
            break
        
        initial_state = {
            "messages": [SystemMessage(initial_processing_template), HumanMessage(user_input + config_prompt)],
            "node_history": [],
            "default_config": default_config,
            "awaiting_human_input": False,
            "current_code": "",
            "code_to_run": ""
        }

        # stream the graph without handling intermediate outputs
        list(graph.stream(initial_state, config=config))

        print("\nDone!")
        break

if __name__ == "__main__":
    main()