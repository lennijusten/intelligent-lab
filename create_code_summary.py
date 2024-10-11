import os
import datetime
import argparse

def generate_architecture_summary(files_to_include):
    # Extract unique directories from files_to_include
    directories = set(os.path.dirname(file) for file in files_to_include)
    
    # Create a dictionary to represent the directory structure
    structure = {}
    for directory in directories:
        parts = directory.split(os.sep)
        current = structure
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
    
    # Function to recursively build the architecture string
    def build_architecture_string(struct, indent=0):
        result = ""
        for key, value in struct.items():
            result += "  " * indent + f"- {key}/\n"
            result += build_architecture_string(value, indent + 1)
        return result
    
    # Generate the architecture summary
    architecture_summary = "# Project Architecture\n\n"
    architecture_summary += build_architecture_string(structure)
    
    # Add list of included files
    architecture_summary += "\n# Included Files\n\n"
    for file in files_to_include:
        architecture_summary += f"- {file}\n"
    
    return architecture_summary

def create_code_summary_txt(input_file, output_path=None):
    if output_path is None:
        # Default to Downloads folder with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.expanduser(f"~/Downloads/code_summary_{timestamp}.txt")

    # Read files from input text file
    with open(input_file, "r") as f:
        files_to_include = [line.strip() for line in f.readlines()]

    # Generate architecture summary
    architecture_summary = generate_architecture_summary(files_to_include)

    # Create text content
    text_content = f"Code Summary\n\n{architecture_summary}\n"

    # Add code for each file
    for file_path in files_to_include:
        try:
            with open(file_path, 'r') as file:
                code = file.read()
                text_content += f"\n\n# {file_path}\n\n{code}\n"
        except FileNotFoundError:
            print(f"Warning: File not found - {file_path}")

    # Write to text file
    with open(output_path, 'w') as output_file:
        output_file.write(text_content)
    
    print(f"Text file saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a code summary text file.")
    parser.add_argument("input_file", help="Path to the text file containing list of files to include")
    parser.add_argument("-o", "--output", help="Path to the output text file (optional)")
    args = parser.parse_args()

    create_code_summary_txt(args.input_file, args.output)