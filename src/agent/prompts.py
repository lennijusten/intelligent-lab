initial_processing_template = """
Analyze the user's Opentrons liquid handling command and provide a structured summary. Your response should be in YAML format with the following structure:

command: "A clear, specific restatement of the user's command"
task_breakdown:
  - "Step 1: ..."
  - "Step 2: ..."
  - ...
required_resources:
  pipettes: []
  labware: []
  modules: []
  reagents: []
variables_to_specify:
  - "Variable 1: ..."
  - "Variable 2: ..."
  - ...

Focus on identifying all necessary components and variables crucial for task execution. Use Opentrons-specific language in the task breakdown. Only include variables that are critical and not specified in the original command.

Examples:

User input: "Dilute all of the wells on the 96-well plate on deck slot 3 with 10 uL of water from a water container in well 1a of the 24-well metal block on top of the temperature controller. 20 uL tip rack is on deck slot 2 and the 20 uL pipette is mounted on the left side."

Output:
command: "Dilute each well of a 96-well plate with 10 µL of water, using a 20 µL pipette and a temperature-controlled water source"
task_breakdown:
  - "1. Load labware onto the deck: 96-well plate, 24-well aluminum block, and 20 µL tip rack"
  - "2. Load 20 µL single-channel pipette on the left mount"
  - "3. Load temperature module and place 24-well metal block on it"
  - "4. Load liquid (water) to well A1 of the 24-well metal block"
  - "5. For each well in the 96-well plate:"
  - "   a. Pick up a 20 µL tip"
  - "   b. Aspirate 10 µL of water from well A1 of the 24-well block"
  - "   c. Dispense 10 µL into the current well of the 96-well plate"
  - "   d. Drop the used tip"
required_resources:
  pipettes:
    - "20 µL single-channel (left)"
  labware:
    - "96-well plate"
    - "24-well aluminum block"
    - "20 µL tip rack"
  modules:
    - "Temperature module"
  reagents:
    - "Water"
variables_to_specify:
  - "Total volume of water needed for dilution"

User input: "Transfer 5 uL from well A1 to B1 in the same plate and dispose of the tip"

Output:
command: "Transfer 5 µL from well A1 to well B1 within a single plate using a single-channel pipette, then dispose of the tip"
task_breakdown:
  - "1. Load labware onto the deck: plate and tip rack"
  - "2. Load single-channel pipette (≤10 µL capacity)"
  - "3. Pick up a pipette tip"
  - "4. Aspirate 5 µL from well A1 of the plate"
  - "5. Dispense 5 µL into well B1 of the same plate"
  - "6. Drop the used tip in the trash"
required_resources:
  pipettes:
    - "Single-channel pipette (≤10 µL capacity)"
  labware:
    - "Plate"
    - "Tip rack"
  modules: []
  reagents: []
variables_to_specify:
  - "Plate location on deck"
  - "Tip rack location on deck"
  - "Pipette mount position (left or right)"

Provide a similar structured output for the given user input.
"""

get_info_template = """
Your task is to determine if more information is needed to execute the Opentrons liquid handling task. Review the rephrased command, task breakdown, required resources, variables to specify, default configuration, and conversation history.

Analyze the information for:
- Missing required resources
- Unspecified critical variables (e.g., volumes, labware locations, pipette types and positions)
- Compatibility issues between specified labware and pipettes
- Any crucial information gaps that could prevent the protocol from running

If critical information is missing, formulate 1-3 clear, concise questions to gather this information from the user. Focus only on what's absolutely necessary for the protocol to run correctly.

If all critical information is available, use the LiquidHandlerInstructions tool to generate instructions.

Your response should be in one of these two formats:
1. A list of questions, each on a new line, starting with "Q: ". For example:
   Q: What is the specific model of the 96-well plate?
   Q: What is the configuration of the thermocycler plate?

2. Or, if all information is complete, use the LiquidHandlerInstructions tool to structure the information. Here's how to use the tool:

1. Only use the tool when you have gathered ALL necessary information for the task.
2. Structure the information into 'workflow' and 'deck_state' as defined by the tool.
3. For 'workflow', provide a list of discrete steps, each with an 'operation' and relevant parameters.
4. For 'deck_state', include information about pipettes, labware, tip_racks, and modules.
5. If any information is assumed or inferred, clearly state these assumptions before using the tool.
6. Do not include any fields or structures not defined in the LiquidHandlerInstructions tool.

Avoid asking about:
- Exact labware models unless crucial for the protocol
- Minor details that can be assumed based on standard laboratory practices
- Information already provided in the default configuration unless there's a clear conflict

Remember, output ONLY the questions or the tool use instruction, without any additional explanation or analysis.
"""

concept_finder_template = """
You are a concept identifier for liquid handling robot commands. Given the message history, identify the relevant concepts from the following list:

{available_concepts}

Your task is to use the RelevantConcepts tool to return a list of relevant concepts, choosing only from the provided list. Do not include any concepts that are not in this list.
"""

code_gen_template = """
Based on the above liquid handler workflow, deck state, and concept background, generate Python code using the Opentrons API.

Ensure the code follows best practices for the Opentrons API, includes proper error handling, and is well-commented for clarity.

Output just the commented code without any explanations or additional text. The user should be able to copy and paste the code into their Python script and run it without any modifications.
"""