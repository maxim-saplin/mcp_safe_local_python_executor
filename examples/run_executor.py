# Add the parent directory to the path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from executor import LocalPythonExecutor


def main():
    # Initialize the executor
    executor = LocalPythonExecutor(additional_authorized_imports=[])

    # Example 1: Simple arithmetic
    print("\nExample 1: Simple arithmetic")
    code = "2 + 2"
    result, logs = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")

    # Example 2: Using print statements
    print("\nExample 2: Using print statements")
    code = """
x = 10
y = 20
result = x + y
"""
    result, logs = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")


if __name__ == "__main__":
    main()
