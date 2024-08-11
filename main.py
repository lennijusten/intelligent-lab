import argparse
import json
import uuid
from dotenv import load_dotenv
import os

from src.agent.graph import create_graph
from src.agent.state import AgentState
from src.agent.prompts import initial_processing_prompt, get_info_prompt, code_gen_prompt
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
        user = input("User (q/Q to quit): ")
        if user.lower() == 'q':
            print("AI: Goodbye!")
            break

        initial_state = {
            "messages": [HumanMessage(content=user + config_prompt)],
            "default_config": default_config,
            "processed_command": "",
            "awaiting_human_input": False,
            "current_code": "",
            "code_to_run": ""
        }

        for output in graph.stream(initial_state, config=config):
            if "messages" in output:
                output["messages"][-1].pretty_print()
            
            if output.get("awaiting_human_input", False):
                break

        if "code_to_run" in output:
            print("\nFinal Approved Code:")
            print(output["code_to_run"])
        elif "current_code" in output:
            print("\nCurrent Code (not yet approved):")
            print(output["current_code"])

        print("\nDone!")
        break

if __name__ == "__main__":
    main()