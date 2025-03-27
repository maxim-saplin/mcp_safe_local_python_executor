"""
Tests for the MCP server.
"""

import os
import sys
import pytest

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the MCP server module
import mcp_server


@pytest.mark.asyncio
async def test_run_python():
    """Test that the run_python tool works correctly."""
    # Test basic arithmetic
    result = await mcp_server.run_python("result = 2 + 2")
    assert result["result"] == 4

    # Test math module functionality
    result = await mcp_server.run_python("import math\nresult = math.sqrt(16)")
    assert result["result"] == 4.0


@pytest.mark.asyncio
async def test_prime_numbers():
    """Test generating a list of prime numbers."""
    code = """
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [num for num in range(2, 101) if is_prime(num)]
result = primes"""
    
    result = await mcp_server.run_python(code)
    expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 
                     43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    assert result["result"] == expected_primes 