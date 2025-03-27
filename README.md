# Local Executor

A safe Python code executor that allows running Python code in a controlled environment with restricted access to system resources and modules.

## Features

- Safe execution of Python code
- Restricted access to system resources
- Configurable allowed imports
- Support for custom tools and functions
- Print output capture
- Final answer mechanism
- MCP (Model Context Protocol) server integration

## Installation

```bash
pip install local-executor
```

## Usage

Here's a simple example of how to use the LocalExecutor:

```python
from local_executor import LocalPythonExecutor

# Initialize the executor
executor = LocalPythonExecutor(additional_authorized_imports=[])

# Simple code execution
code = "2 + 2"
result, logs, is_final_answer = executor(code)
print(f"Result: {result}")  # Output: 4

# Using print statements
code = """
print("Hello, World!")
x = 10
y = 20
print(f"Sum: {x + y}")
"""
result, logs, is_final_answer = executor(code)
print(f"Logs: {logs}")  # Output: Hello, World!\nSum: 30

# Using final_answer
code = """
def calculate_sum(a, b):
    return a + b

result = calculate_sum(5, 3)
final_answer(result)
"""
result, logs, is_final_answer = executor(code)
print(f"Final answer: {result}")  # Output: 8
```

## Advanced Usage

### Setting Variables

```python
executor = LocalPythonExecutor(additional_authorized_imports=[])

# Set variables in the execution environment
executor.send_variables({
    "x": 10,
    "y": 20
})

# Use the variables in code
code = "result = x + y"
result, logs, is_final_answer = executor(code)
print(f"Result: {result}")  # Output: 30
```

## MCP Server

This package includes an MCP (Model Context Protocol) server that allows you to expose the Python executor as a tool for LLMs like Claude.

### Running the MCP Server

```bash
# Run the MCP server
python mcp_server.py
```

### Configuring Claude for Desktop

1. Make sure you have Claude for Desktop installed (download from [claude.ai](https://claude.ai/desktop))
2. Edit your Claude for Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. Add the following configuration:

```json
{
    "mcpServers": {
        "python-executor": {
            "command": "python",
            "args": [
                "/absolute/path/to/mcp_server.py"
            ]
        }
    }
}
```

4. Restart Claude for Desktop
5. The Python executor tool will now be available in Claude

### Example Prompts

Once configured, you can use prompts like:

- "Calculate the factorial of 5 using Python"
- "Create a list of prime numbers up to 100"
- "Solve this equation: x^2 + 5x + 6 = 0"

### MCP Server Tools

The MCP server exposes the following tools:

- `run_python`: Execute Python code in a secure sandbox
- `get_available_modules`: Get a list of modules that are available for import
- `set_variables`: Set variables in the Python execution environment

### Example Helper Script

You can also use the provided helper script to run the MCP server:

```bash
python examples/run_mcp_server.py
```