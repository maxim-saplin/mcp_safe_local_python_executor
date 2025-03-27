#!/usr/bin/env python3
"""
MCP Server for LocalPythonExecutor

This module implements a Model Context Protocol (MCP) server that exposes 
the LocalPythonExecutor as a tool for AI assistants.
"""

import logging
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP
# from executor import LocalPythonExecutor
from smolagents.local_python_executor import LocalPythonExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

mcp = FastMCP("python-executor")

executor = LocalPythonExecutor(additional_authorized_imports=[])
executor.send_tools({})


@mcp.tool()
async def run_python(
    code: str
) -> Dict[str, Any]:
    """Execute Python code in a secure sandbox environment.
    
    This tool allows running simple Python code for calculations and data manipulations.
    The execution environment is restricted for security purposes. Make sure you create a single file
    that can be executed in one go and it returns a result.

    Default allowed imports:
    - math
    - random 
    - datetime
    - time
    - json
    - re
    - string
    - collections
    - itertools
    - functools
    - operator
    
    Args:
        code: The Python code to execute. Must be valid Python 3 code. The result must be stored in a variable called `result`. E.g.:
        ```python
        import math
        result = math.sqrt(16)
        ```
        
    Returns:
        A dictionary with execution results containing:
        - result: The final value or None if no value is returned
        - logs: Any output from print statements
    """
    logger.info(f"Executing Python code: {code}")
    
    result, logs, _ = executor(code)

    response = {
        "result": result,
        "logs": logs
    }
    
    logger.info(f"Execution result: {result}")
    return response


if __name__ == "__main__":
    logger.info("Starting MCP server for Python executor")
    mcp.run(transport='stdio') 