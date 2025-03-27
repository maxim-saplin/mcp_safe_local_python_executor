"""
Smoke tests for the LocalPythonExecutor.
"""

import os
import sys
import pytest

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the executor
from smolagents.local_python_executor import LocalPythonExecutor


def test_simple_arithmetic():
    """Test that simple arithmetic works correctly."""
    executor = LocalPythonExecutor(additional_authorized_imports=[])
    
    code = "2 + 2"
    result, logs, _ = executor(code)
    
    assert result == 4
    assert logs == ""


def test_variable_assignment():
    """Test that variable assignment works correctly."""
    executor = LocalPythonExecutor(additional_authorized_imports=[])
    
    code = """
x = 10
y = 20
result = x + y
"""
    result, logs, _ = executor(code)
    
    assert result == 30
    assert logs == ""


def test_expression_result():
    """Test that the last expression is returned as result."""
    executor = LocalPythonExecutor(additional_authorized_imports=[])
    
    code = """
x = 5
x * 2
"""
    result, logs, _ = executor(code)
    
    assert result == 10
    assert logs == ""


def test_array_operations():
    """Test that array operations work correctly."""
    executor = LocalPythonExecutor(additional_authorized_imports=[])
    
    code = """
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
total
"""
    result, logs, _ = executor(code)
    
    assert result == 15
    assert logs == ""


def run_smoke_tests():
    """Run the smoke tests manually with output."""
    # Initialize the executor
    executor = LocalPythonExecutor(additional_authorized_imports=[])

    # Test 1: Simple arithmetic
    print("\nTest 1: Simple arithmetic")
    code = "2 + 2"
    result, logs, _ = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")
    print(f"Test passed: {result == 4}")

    # Test 2: Variable assignment
    print("\nTest 2: Variable assignment")
    code = """
x = 10
y = 20
result = x + y
"""
    result, logs, _ = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")
    print(f"Test passed: {result == 30}")

    # Test 3: Expression result
    print("\nTest 3: Expression result")
    code = """
x = 5
x * 2
"""
    result, logs, _ = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")
    print(f"Test passed: {result == 10}")

    # Test 4: Array operations
    print("\nTest 4: Array operations")
    code = """
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
total
"""
    result, logs, _ = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")
    print(f"Test passed: {result == 15}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke":
        run_smoke_tests()
    else:
        pytest.main(["-v", __file__]) 