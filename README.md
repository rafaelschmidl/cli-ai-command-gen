# CLI AI Command Generator

CLI AI Command Generator is a Python-based tool that uses AI to generate and suggest command-line prompts for various operating systems. It leverages the Ollama AI model to create commands based on user descriptions and keeps a history of generated commands for future suggestions.

## Features

- Generate command-line prompts for Mac, Windows, and Linux
- Suggest commonly used commands based on history
- Customizable AI model selection
- Simple and intuitive command-line interface

## Prerequisites

- Python 3.6+
- [Ollama](https://ollama.ai/download) installed and running on your system

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cli_ai_command_gen.git
   cd cli_ai_command_gen
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Generating a Command

To generate a command, use the `generate` subcommand followed by your task description:

```
python cli_gen.py generate "Create a new directory called 'project' and navigate into it"
```

### Suggesting Commands

To suggest commonly used commands, use the `suggest` subcommand:

```
python cli_gen.py suggest
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


