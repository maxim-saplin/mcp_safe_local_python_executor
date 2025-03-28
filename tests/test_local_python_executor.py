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


def test_filesystem_access_fails():
    """Test that filesystem access is blocked"""
    print("\nTest: Filesystem access attempt")
    code = """
import os
files = os.listdir('.')
files
"""
    executor = LocalPythonExecutor(additional_authorized_imports=[])
    with pytest.raises(Exception) as exc_info:
        executor(code)
    assert 'InterpreterError: Import of os is not allowed' in str(exc_info.value)



if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke":
        run_smoke_tests()
    else:
        pytest.main(["-v", __file__]) 