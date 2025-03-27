#!/usr/bin/env python3
"""
Simple MCP Client for testing the Python Executor server.

This script directly connects to the MCP server and tests its functionality.
It is useful for debugging and testing without needing to use Claude for Desktop.
"""

import asyncio
import sys
import subprocess
import time
from pathlib import Path

# Try to import the MCP client package
try:
    from mcp.client.stdio import stdio_client, StdioServerParameters
except ImportError:
    print("MCP client package not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "mcp[cli]"], check=True)
    from mcp.client.stdio import stdio_client, StdioServerParameters


async def test_server():
    """Test connecting to the MCP server and using its tools."""
    print("Connecting to the MCP server...")
    
    # Start the process in the background
    server_path = Path(__file__).resolve().parent.parent / "mcp_server.py"
    process = subprocess.Popen(
        [sys.executable, str(server_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )
    
    # Wait for the server to start
    print("Server starting, waiting 2 seconds...")
    time.sleep(2)
    
    # Create server parameters
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)]
    )
    
    # Create a client
    async with stdio_client(server_params) as session:
        try:
            # Get server info
            print("\n1. Getting server info...")
            server_info = await session.info()
            print(f"Server name: {server_info.name}")
            print(f"Tools: {[tool.name for tool in server_info.tools]}")
            
            # Test run_python tool
            print("\n2. Testing run_python tool with basic arithmetic...")
            code = "2 + 2"
            response = await session.tool("run_python", {"code": code})
            print(f"Code: {code}")
            print(f"Result: {response['result']}")
            
            # Test with print statements
            print("\n3. Testing run_python tool with print statements...")
            code = """
print("Hello from Python!")
x = 10
y = 20
print(f"Sum: {x + y}")
"""
            response = await session.tool("run_python", {"code": code})
            print(f"Code: {code}")
            print(f"Logs: {response['logs']}")
            
            # Test with explanation
            print("\n4. Testing run_python tool with explanation...")
            code = "import math\nmath.sqrt(16)"
            response = await session.tool("run_python", {"code": code, "explain": True})
            print(f"Code: {code}")
            print(f"Result: {response['result']}")
            print(f"Explanation: {response.get('explanation', 'No explanation')}")
            
            # Test get_available_modules
            print("\n5. Testing get_available_modules tool...")
            modules = await session.tool("get_available_modules", {})
            print(f"Available modules: {modules}")
            
            # Test set_variables
            print("\n6. Testing set_variables tool...")
            variables = {"a": 100, "b": 200}
            response = await session.tool("set_variables", {"variables": variables})
            print(f"Set variables response: {response}")
            
            # Test using the set variables
            print("\n7. Testing using the set variables...")
            code = "a + b"
            response = await session.tool("run_python", {"code": code})
            print(f"Code: {code}")
            print(f"Result: {response['result']}")
            
            print("\nAll tests completed successfully!")
        
        finally:
            # Terminate the server process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    asyncio.run(test_server()) 