'''

Here are the steps to install and configure NGINX:

1. Update the package manager to ensure you have the latest package list.
2. Install the NGINX package.

The bash commands are as follows:

```bash
echo "Hello, World!"
sudo apt install cowsay
```

'''


'''
import os
import stat
import re
import subprocess
from datetime import datetime
from typing import List, Dict, Union

DEFAULT_SCRIPT_PATH = "scripts/execution.sh"
LOG_FILE_PATH = "scripts/command_execution.log"

SUDO_PASSWORD = "1122"

def setup_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(os.path.dirname(DEFAULT_SCRIPT_PATH), exist_ok=True)

def log_execution(message: str):
    """Log execution details to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def extract_bash_commands(text: str) -> List[str]:
    """Extract bash commands from text enclosed in backticks."""
    pattern = r'`{1,3}(?:bash|shell)?\s*\n?(.*?)`{1,3}'
    commands = []
    matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        command = match.group(1).strip()
        if command:
            command_lines = [line.strip() for line in command.split('\n') if line.strip()]
            commands.extend(command_lines)
    
    return commands

def create_script_content(commands: List[str]) -> str:
    """Create the content for a bash script with sudo password handling."""
    if not commands:
        raise ValueError("No commands provided to create the script.")
    
    script_lines = [
        "#!/bin/bash",
        "",
        f"# Script updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "# Store sudo password",
        f"SUDO_PASSWORD='{SUDO_PASSWORD}'",
        "",
        "# Function to handle sudo commands",
        "sudo_exec() {",
        "    command=\"$@\"",
        "    echo $SUDO_PASSWORD | sudo -S bash -c \"$command\" 2>/dev/null",
        "}",
        "",
        "# Function to handle errors",
        "handle_error() {",
        "    echo \"\\033[0;31mError occurred in command: $BASH_COMMAND\\033[0m\"",
        "    echo \"\\033[0;31mError occurred on line: ${BASH_LINENO[0]}\\033[0m\"",
        "    exit 1",
        "}",
        "",
        "trap 'handle_error' ERR",
        "",
        "# Function to print colored output",
        "print_status() {",
        "    case $1 in",
        "        'executing')",
        "            echo -e \"\\033[0;34m→ Executing: $2\\033[0m\"",
        "            ;;",
        "        'success')",
        "            echo -e \"\\033[0;32m✓ $2\\033[0m\"",
        "            ;;",
        "        'error')",
        "            echo -e \"\\033[0;31m✗ $2\\033[0m\"",
        "            ;;",
        "    esac",
        "}",
        "",
        "# Beginning of commands",
        ""
    ]
    
    for command in commands:
        script_lines.extend([
            f"print_status 'executing' '{command}'",
            command,
            f"print_status 'success' 'Command completed'",
            ""
        ])
    
    script_lines.append("print_status 'success' 'Script completed successfully'")
    return "\n".join(script_lines)

def save_script(content: str) -> str:
    """Save or update the script content to the default script file."""
    setup_directories()
    
    try:
        with open(DEFAULT_SCRIPT_PATH, 'w') as f:
            f.write(content)
        os.chmod(DEFAULT_SCRIPT_PATH, os.stat(DEFAULT_SCRIPT_PATH).st_mode | stat.S_IEXEC)
    except Exception as e:
        log_execution(f"Failed to create or write to script: {str(e)}")
        raise RuntimeError("Error creating or writing to the script file.")
    
    return DEFAULT_SCRIPT_PATH

def execute_bash_script(script_path: str) -> Dict[str, Union[bool, str]]:
    """Execute the specified bash script and return the results."""
    result = {
        'success': False,
        'output': '',
        'error': ''
    }
    
    try:
        process = subprocess.Popen(
            [script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        result['success'] = process.returncode == 0
        result['output'] = stdout.strip()
        result['error'] = stderr.strip()
        
        log_execution(
            f"Script execution {'successful' if result['success'] else 'failed'}\n"
            f"Output: {stdout.strip()}\n"
            f"Error: {stderr.strip()}\n"
            f"{'-'*50}"
        )
        
    except Exception as e:
        result['error'] = str(e)
        log_execution(f"Execution error: {str(e)}")
    
    return result

def process_commands(text: str, execute: bool = False) -> Dict[str, Union[str, bool, List[str]]]:
    """Process commands from text and optionally execute them."""
    result = {
        'commands': [],
        'script_path': '',
        'execution_result': None
    }
    
    try:
        commands = extract_bash_commands(text)
        result['commands'] = commands
        
        if commands:
            content = create_script_content(commands)
            script_path = save_script(content)
            result['script_path'] = script_path
            
            if execute:
                result['execution_result'] = execute_bash_script(script_path)
        else:
            log_execution("No commands found in the provided text.")
            raise ValueError("No commands extracted from input text.")

    except Exception as e:
        log_execution(f"Processing error: {str(e)}")
        result['error'] = str(e)
    
    return result

def main():
    """Main function to handle command processing and execution."""
    
    # Here, we define the input_text directly as a variable.
    input_text = """Here are the steps to install and configure NGINX:

1. Update the package manager to ensure you have the latest package list.
2. Install the NGINX package.

The bash commands are as follows:

```bash
echo "Hello, Meow Meow!"
sudo apt install cowsay
```

    """
    
    # Process the input_text and execute if necessary
    print("\n\033[0;34mProcessing commands...\033[0m")
    result = process_commands(input_text, execute=True)
    
    print("\n\033[0;32mResults:\033[0m")
    print(f"Commands extracted: {len(result['commands'])}")
    print(f"Script saved to: {result['script_path']}")
    
    if result.get('execution_result'):
        print("\n\033[0;34mExecution results:\033[0m")
        if result['execution_result']['success']:
            print("\033[0;32m✓ Script executed successfully!\033[0m")
            if result['execution_result']['output']:
                print("Output:", result['execution_result']['output'])
        else:
            print("\033[0;31m✗ Execution failed!\033[0m")
            print("Error:", result['execution_result']['error'])

if __name__ == "__main__":
    main()
'''

import os
import stat
import subprocess
import re
from datetime import datetime
from typing import List, Dict, Union

# Configuration
DEFAULT_SCRIPT_PATH = "scripts/execution.sh"
LOG_FILE_PATH = "scripts/command_execution.log"
SUDO_PASSWORD = "1122"


def setup_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(os.path.dirname(DEFAULT_SCRIPT_PATH), exist_ok=True)

def log_execution(message: str):
    """Log execution details to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def extract_bash_commands(text: str) -> List[str]:
    """Extract bash commands from text enclosed in backticks."""
    pattern = r'`{1,3}(?:bash|shell)?\s*\n?(.*?)`{1,3}'
    commands = []
    matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        command = match.group(1).strip()
        if command:
            command_lines = [line.strip() for line in command.split('\n') if line.strip()]
            commands.extend(command_lines)
    
    return commands

def create_script_content(commands: List[str]) -> str:
    """Create the content for a bash script with sudo password handling."""
    if not commands:
        raise ValueError("No commands provided to create the script.")
    
    script_lines = [
        "#!/bin/bash",
        "",
        f"# Script updated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "# Store sudo password",
        f"SUDO_PASSWORD='{SUDO_PASSWORD}'",
        "",
        "# Function to handle sudo commands",
        "sudo_exec() {",
        "    command=\"$@\"",
        "    # Validate sudo password upfront to avoid prompts during execution",
        "    echo $SUDO_PASSWORD | sudo -S -v 2>/dev/null",  # Validate sudo and cache the password",
        "    echo $SUDO_PASSWORD | sudo -S bash -c \"$command\" 2>/dev/null",
        "}",
        "",
        "# Function to handle errors",
        "handle_error() {",
        "    echo \"\\033[0;31mError occurred in command: $BASH_COMMAND\\033[0m\"",
        "    echo \"\\033[0;31mError occurred on line: ${BASH_LINENO[0]}\\033[0m\"",
        "    exit 1",
        "}",
        "",
        "trap 'handle_error' ERR",
        "",
        "# Function to print colored output",
        "print_status() {",
        "    case $1 in",
        "        'executing')",
        "            echo -e \"\\033[0;34m→ Executing: $2\\033[0m\"",
        "            ;;",
        "        'success')",
        "            echo -e \"\\033[0;32m✓ $2\\033[0m\"",
        "            ;;",
        "        'error')",
        "            echo -e \"\\033[0;31m✗ $2\\033[0m\"",
        "            ;;",
        "    esac",
        "}",
        "",
        "# Beginning of commands",
        ""
    ]
    
    for command in commands:
        script_lines.extend([
            f"print_status 'executing' '{command}'",
            command,
            f"print_status 'success' 'Command completed'",
            ""
        ])
    
    script_lines.append("print_status 'success' 'Script completed successfully'")
    return "\n".join(script_lines)

def save_script(content: str) -> str:
    """Save or update the script content to the default script file."""
    setup_directories()
    
    try:
        with open(DEFAULT_SCRIPT_PATH, 'w') as f:
            f.write(content)
        os.chmod(DEFAULT_SCRIPT_PATH, os.stat(DEFAULT_SCRIPT_PATH).st_mode | stat.S_IEXEC)
    except Exception as e:
        log_execution(f"Failed to create or write to script: {str(e)}")
        raise RuntimeError("Error creating or writing to the script file.")
    
    return DEFAULT_SCRIPT_PATH

def execute_bash_script(script_path: str) -> Dict[str, Union[bool, str]]:
    """Execute the specified bash script and return the results."""
    result = {
        'success': False,
        'output': '',
        'error': ''
    }
    
    try:
        process = subprocess.Popen(
            [script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        result['success'] = process.returncode == 0
        result['output'] = stdout.strip()
        result['error'] = stderr.strip()
        
        log_execution(
            f"Script execution {'successful' if result['success'] else 'failed'}\n"
            f"Output: {stdout.strip()}\n"
            f"Error: {stderr.strip()}\n"
            f"{'-'*50}"
        )
        
    except Exception as e:
        result['error'] = str(e)
        log_execution(f"Execution error: {str(e)}")
    
    return result

def process_commands(text: str, execute: bool = False) -> Dict[str, Union[str, bool, List[str]]]:
    """Process commands from text and optionally execute them."""
    result = {
        'commands': [],
        'script_path': '',
        'execution_result': None
    }
    
    try:
        commands = extract_bash_commands(text)
        result['commands'] = commands
        
        if commands:
            content = create_script_content(commands)
            script_path = save_script(content)
            result['script_path'] = script_path
            
            if execute:
                result['execution_result'] = execute_bash_script(script_path)
        else:
            log_execution("No commands found in the provided text.")
            raise ValueError("No commands extracted from input text.")

    except Exception as e:
        log_execution(f"Processing error: {str(e)}")
        result['error'] = str(e)
    
    return result

def main(user_input):
    """Main function to handle command processing and execution."""
    
    # Here, we define the input_text directly as a variable.
    input_text = user_input

    # Process the input_text and execute if necessary
    print("\n\033[0;34mProcessing commands...\033[0m")
    result = process_commands(input_text, execute=True)
    
    print("\n\033[0;32mResults:\033[0m")
    print(f"Commands extracted: {len(result['commands'])}")
    print(f"Script saved to: {result['script_path']}")
    
    if result.get('execution_result'):
        print("\n\033[0;34mExecution results:\033[0m")
        if result['execution_result']['success']:
            print("\033[0;32m✓ Script executed successfully!\033[0m")
            if result['execution_result']['output']:
                print("Output:", result['execution_result']['output'])
        else:
            print("\033[0;31m✗ Execution failed!\033[0m")
            print("Error:", result['execution_result']['error'])

if __name__ == "__main__":
    user_input = """Here are the steps to install and configure NGINX:

1. Update the package manager to ensure you have the latest package list.
2. Install the NGINX package.

The bash commands are as follows:

```bash
echo "Hello, Meow Meow!"
```"""
    
    # main(user_input)
