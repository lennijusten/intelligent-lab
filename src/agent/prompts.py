initial_processing_template = """
Analyze the user's PyLabRobot liquid handling command and provide a structured summary. Your response should be in YAML format with the following structure:

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

Focus on identifying all necessary components and variables crucial for task execution. Use PyLabRobot-specific language in the task breakdown. Only include variables that are critical and not specified in the original command.

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
Your task is to gather and validate information needed to execute a liquid handling task using the PyLabRobot robot. Analyze the user command, task breakdown, required resources, variables to specify, default configuration, and conversation history.

After each analysis, you MUST use the GetInfoResponse tool to update the current state. This tool takes three parameters:

1. deck_state: The current known configuration of the robot's deck, including pipettes, labware, tip racks, and modules.
2. info_complete: A boolean indicating whether all necessary information has been gathered (True) or if more information is needed (False).
3. questions: A string containing questions for the user if more information is needed, or an empty string if no questions are necessary.

Guidelines for your analysis:
1. Review the information for:
   - Missing required resources
   - Unspecified critical variables (e.g., volumes, labware locations, pipette types and positions)
   - Compatibility issues between specified labware and pipettes
   - Any crucial information gaps that could prevent the protocol from running

2. If information is missing:
   - Set info_complete to False
   - Generate clear, concise questions to gather the missing information
   - Include these questions in the 'questions' parameter of the GetInfoResponse tool
   - Update the deck_state with any partial information you have

3. If all critical information is available:
   - Set info_complete to True
   - Leave the 'questions' parameter empty
   - Update the deck_state with all the gathered information

4. When updating the deck_state:
   - Include information about pipettes, labware, tip_racks, and modules
   - If any information is assumed or inferred, clearly state these assumptions

5. Avoid asking about:
   - Exact labware models unless crucial for the protocol
   - Minor details that can be assumed based on standard laboratory practices
   - Information already provided in the default configuration unless there's a clear conflict

Always use the GetInfoResponse tool at the end of your analysis, regardless of whether more information is needed or not. This ensures the current state is always updated and tracked.

Example tool usage:
{
  "deck_state": {
    "pipettes": {"left": "p300_single", "right": "p20_multi_gen2"},
    "labware": {"1": "corning_96_wellplate_360ul_flat", "2": "PyLabRobot_24_tuberack_eppendorf_1.5ml_safelock_snapcap"},
    "tip_racks": {"3": "PyLabRobot_96_tiprack_300ul"},
    "modules": {}
  },
  "info_complete": false,
  "questions": "Q: What volume of liquid should be transferred from the tube rack to the well plate?\nQ: Which specific wells in the 96-well plate should receive the liquid?"
}

Remember, your response MUST always end with the use of the GetInfoResponse tool. Do not add any additional explanation or analysis outside of the tool use.
"""

concept_finder_template = """
You are a concept identifier for liquid handling robot commands. Given the message history, identify the relevant concepts from the following list:

{available_concepts}

Your task is to use the RelevantConcepts tool to return a list of relevant concepts, choosing only from the provided list. Do not include any concepts that are not in this list.
"""

code_gen_template = """
Based on the above liquid handler workflow, deck state, and concept background, generate Python code using the PyLabRobot API.

Ensure the code follows best practices for the PyLabRobot API, includes proper error handling, and is well-commented for clarity.

Output just the commented code without any explanations or additional text. The user should be able to copy and paste the code into their Python script and run it without any modifications.
"""