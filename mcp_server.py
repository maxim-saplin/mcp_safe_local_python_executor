#!/usr/bin/env python3
"""
MCP Server for LocalPythonExecutor

This module implements a Model Context Protocol (MCP) server that exposes 
the LocalPythonExecutor as a tool for AI assistants.
"""

import logging
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP
from executor import LocalPythonExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("python-executor")


# Initialize the Python executor with safe defaults
executor = LocalPythonExecutor(additional_authorized_imports=[])


@mcp.tool()
async def run_python(
    code: str
    # additional_imports: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Execute Python code in a secure sandbox environment.
    
    This tool allows running simple Python code for calculations and data manipulations.
    The execution environment is restricted for security purposes.

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
        code: The Python code to execute. Should be valid Python 3 code. The result must be stored in a variable called `result`. E.g.:
        ```python
        result = 2 + 2
        ```
        
    Returns:
        A dictionary with execution results containing:
        - result: The final value or None if no value is returned
        - logs: Any output from print statements
    """
    logger.info(f"Executing Python code: {code}")
    
    # # If additional imports are requested, create a new executor with those imports
    # if additional_imports:

    #     temp_executor = LocalPythonExecutor(additional_authorized_imports=all_imports)
    #     result, logs = temp_executor(code)
    # else:
    #     # Use the default executor
    #     result, logs = executor(code)
    
    result, logs = executor(code)

    response = {
        "result": result,
        "logs": logs
    }
    
    logger.info(f"Execution result: {result}")
    return response


if __name__ == "__main__":
    logger.info("Starting MCP server for Python executor")
    mcp.run(transport='stdio') 