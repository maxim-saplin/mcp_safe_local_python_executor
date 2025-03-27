#!/usr/bin/env python3
"""
Example script demonstrating how to run the MCP server for LocalPythonExecutor.

This script provides instructions for running the MCP server and configuring it
with Claude for Desktop or other MCP clients.
"""

import sys
import subprocess
import json
from pathlib import Path

def print_instructions():
    """Print instructions for running and configuring the MCP server."""
    print("=" * 80)
    print("MCP LOCAL PYTHON EXECUTOR")
    print("=" * 80)
    print("\nThis example demonstrates how to run the MCP server for LocalPythonExecutor.")
    print("\nTo run the server directly:")
    print("    python ../mcp_server.py")
    print("\nTo configure Claude for Desktop:")
    print("1. Open Claude for Desktop configuration at:")
    print("   macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("   Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
    print("\n2. Add the following to the configuration:")
    
    # Get the absolute path to the project root directory
    project_dir = Path(__file__).resolve().parent.parent
    
    # Create example configuration
    config = {
        "mcpServers": {
            "python-executor": {
                "command": "python",
                "args": [
                    str(project_dir / "mcp_server.py")
                ]
            }
        }
    }
    
    # Print the configuration
    print(json.dumps(config, indent=4))
    
    print("\n3. Restart Claude for Desktop")
    print("\n4. Use the Python executor tool in Claude for Desktop by entering prompts like:")
    print("   - 'Calculate the factorial of 5 using Python'")
    print("   - 'Create a list of prime numbers up to 100'")
    print("   - 'Solve this equation: x^2 + 5x + 6 = 0'")
    print("\n=" * 4)
    print("\nWould you like to run the MCP server now? (y/n)")

def run_server():
    """Run the MCP server."""
    # Get the path to the server script
    server_path = Path(__file__).resolve().parent.parent / "mcp_server.py"
    
    # Run the server
    print(f"Running MCP server: {server_path}")
    try:
        subprocess.run([sys.executable, str(server_path)], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == "__main__":
    print_instructions()
    
    choice = input("> ").strip().lower()
    if choice == 'y':
        run_server()
    else:
        print("Server not started. You can run it manually using the instructions above.") 