# Local Executor

A safe Python code executor that allows running Python code in a controlled environment with restricted access to system resources and modules.

## Features

- Safe execution of Python code
- Restricted access to system resources
- Configurable allowed imports
- Support for custom tools and functions
- Print output capture
- Final answer mechanism

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

### Adding Custom Tools

```python
from local_executor import LocalPythonExecutor, Tool

# Define a custom tool
def multiply(a, b):
    return a * b

# Create a Tool instance
multiply_tool = Tool(
    name="multiply",
    func=multiply,
    description="Multiplies two numbers"
)

# Initialize executor with custom tools
executor = LocalPythonExecutor(additional_authorized_imports=[])
executor.send_tools({"multiply": multiply_tool})

# Use the custom tool
code = "result = multiply(4, 5)"
result, logs, is_final_answer = executor(code)
print(f"Result: {result}")  # Output: 20
```

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

## License

This project is licensed under the MIT License - see the LICENSE file for details. 