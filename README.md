# Intelligent Lab Assistant

An AI-powered assistant for controlling liquid handling robots through natural language commands.

## Installation

1. Clone the repository:
```
git clone https://github.com/lennijusten/intelligent-lab.git
cd intelligent-lab
```
2. Create and activate a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Copy the `.env.example` file to `.env` and fill in the required environment variables.
5. Set up a [LangSmith](https://smith.langchain.com/) account for debugging assistance.

## Project Structure

- `main.py`: Entry point for the application.
- `src/agent/`: Contains the core agent logic.
- `state.py`: Defines the agent's state structure, including message history, deck state, and code to run.
- `prompts.py`: Contains prompt templates for various stages of processing.
- `models.py`: Sets up language models and processing chains.
- `tools.py`: Defines custom tools like [Pydantic](https://docs.pydantic.dev/latest/) classes used by the agent. E.g., defines output schemas for [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling).
- `graph.py`: Configures the agent's workflow as a graph.
- `nodes/`: Contains individual processing nodes for the agent.
- `src/opentrons/`: Opentrons-specific implementations.
- `src/opentrons/concepts/`: Markdown files describing Opentrons-specific concepts.
- `configs/`: Contains configuration files for the system; currently just the default deck state. 

## Nodes
- `initial_processing`: This node processes the user's initial input and generates a structured summary.
- `get_info`: This node generates a deck state, determines if more information is needed, and either asks the user questions or passes to the next node. The `get_info` model output conforms to the `GetInfoResponse` Pydantic class:
    ```
    class GetInfoResponse(BaseModel):
        deck_state: DeckState
        info_complete: bool
        questions: str
    ```
    `DeckState` is also a Pydantic class with the following structure:  
      
    ```
    class DeckState(BaseModel):
        pipettes: Dict[str, str]
        labware: Dict[str, str]
        tip_racks: Dict[str, str]
        modules: Dict[str, str]
    ```
- `concept_finder`: This node identifies relevant concepts from a predefined list based on the current message history. For each identified concept, it retrieves associated information from markdown files in `/src/opentrons/concepts/`. Current concepts include `thermocycler_module`, `temperature_controller_module`, `transfer`, `blow_out`, `discard_tip`. The model response follows the `RelevantConcepts` Pydantic class:
    ```
    class RelevantConcepts(BaseModel):
        concepts: List[str]
    ```
- `code_gen`: This node generates Python code for the Opentrons API based on the message history.
- `code_refinement`: This node allows for user feedback and the code output by the `code_gen` node. Once the user accepts the code, the program finishes.

## Dependencies and related projects

- [LangChain](https://www.langchain.com/): Framework for developing applications powered by language models.
- [LangGraph](https://langchain-ai.github.io/langgraph/): Library for building language agents as graphs.
- [Opentrons API](https://docs.opentrons.com/v2/): API for controlling Opentrons robots.
- [PyLabRobot](https://docs.pylabrobot.org/): (Potential future integration) Hardware-agnostic Python package for controlling liquid handling robots.

## Usage
Run the main script:
```
python main.py --config CONFIG_FILE
```

To create a summary of the project codebase for an LLM, create a .txt files of filepaths to include and run the `create_code_summary.py` script:
```
python create_code_summary.py files_to_include.txt
```