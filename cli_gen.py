import argparse  # For parsing command-line arguments
import json  # For reading and writing JSON files
import os  # For file and directory operations
import subprocess  # For running shell commands

# Constants
HISTORY_FILE = 'command_history.json'  # File to store command history
MODEL_NAME = 'llama3'  # Changed default model to llama3

def load_history():
    """Load command history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []  # Return empty list if file doesn't exist

def save_history(history):
    """Save command history to JSON file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def add_to_history(command):
    """Add a new command to history, keeping only the last 100."""
    history = load_history()
    history.append(command)
    history = history[-100:]  # Keep only the last 100 commands
    save_history(history)

def suggest_commands():
    """Suggest the top 5 most used commands from history."""
    history = load_history()
    if not history:
        print("No commands in history. Try generating some commands first!")
        print("Example: python cli_gen.py generate 'how to list files in a directory' -f mac")
        return

    # Count command occurrences
    suggestions = {}
    for command in history:
        suggestions[command] = suggestions.get(command, 0) + 1
    
    # Sort commands by usage count
    sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    
    print("Suggested Commands:")
    for command, count in sorted_suggestions[:5]:
        print(f"- {command} (used {count} times)")

def generate_command(prompt, model, flavor):
    """Generate a command using the AI model based on the given prompt and OS flavor."""
    try:
        # Prepare the full prompt for the AI model, including OS flavor
        full_prompt = f"Generate a command line prompt for the following task on {flavor} OS: {prompt}. Only provide the command, no explanations."
        
        # Run the Ollama command
        result = subprocess.run(['ollama', 'run', model, full_prompt], capture_output=True, text=True, check=True)
        
        # Extract and print the generated command
        command = result.stdout.strip()
        print(f"Generated Command for {flavor}:")
        print(command)
        
        # Add the generated command to history
        add_to_history(command)
    except subprocess.CalledProcessError as e:
        # Handle errors (e.g., Ollama not installed or running)
        print(f"Error generating command: {e.stderr.strip()}")
        print("Make sure Ollama is installed and running on your system.")
        print("You can download Ollama from: https://ollama.ai/download")

def main():
    """Main function to handle command-line arguments and execute commands."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='CLI tool for command line prompt suggestions and generation using Ollama.')
    subparsers = parser.add_subparsers(dest='command')

    # Set up 'generate' command
    gen_parser = subparsers.add_parser('generate', help='Generate a command line prompt for a given task.')
    gen_parser.add_argument('prompt', type=str, nargs='?', help='The task description to generate a command for.')
    gen_parser.add_argument('-m', '--model', type=str, default=MODEL_NAME, help='The model to use for generation.')
    gen_parser.add_argument('-f', '--flavor', type=str, choices=['mac', 'windows', 'linux'], default='mac', 
                            help='The OS flavor to generate the command for (mac, windows, or linux).')

    # Set up 'suggest' command
    subparsers.add_parser('suggest', help='Suggest common command line prompts based on history.')

    # Parse arguments
    args = parser.parse_args()

    # Execute appropriate function based on command
    if args.command == 'generate':
        if args.prompt:
            generate_command(args.prompt, args.model, args.flavor)
        else:
            print("Please provide a task description. Example: python cli_gen.py generate 'how to list files in a directory' -f mac")
    elif args.command == 'suggest':
        suggest_commands()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()