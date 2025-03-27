"""
Tests for the MCP server.
"""

import asyncio
import os
import sys
import unittest

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the MCP server module
import mcp_server


class TestMCPServer(unittest.TestCase):
    """Test cases for the MCP server."""
    
    def test_run_python(self):
        """Test that the run_python tool works correctly."""
        # Create a coroutine to call the run_python tool
        async def test_coroutine():
            # Test basic arithmetic
            # result = await mcp_server.run_python("result = 2 + 2")
            # self.assertEqual(result["result"], 4)

            # Test math module functionality
            result = await mcp_server.run_python("import math\nresult = math.sqrt(16)")
            self.assertEqual(result["result"], 4.0)
            
            
        # Run the coroutine
        asyncio.run(test_coroutine())


if __name__ == '__main__':
    unittest.main() 