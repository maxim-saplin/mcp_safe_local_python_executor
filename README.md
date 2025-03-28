# Safe Local Python Executor

An MCP server (stdio transport) that wraps Hugging Face's [`LocalPythonExecutor`](https://github.com/huggingface/smolagents/blob/main/src/smolagents/local_python_executor.py)
(from the [`smolagents`](https://huggingface.co/docs/smolagents/en/index) framework). It is a custom Python runtime that 
provides basic isolation/security when running Python code generated by LLMs locally. It does not require Docker or VM.
This package allows to expose the Python executor via MCP (Model Context Protocol) as a tool for LLM apps like Claude Desktop, Cursor or any other MCP compatible client.
In case of Claude Desktop this tool is an easy way to add a missing Code Interpreter (available as a pluginn in ChatGPT for quite a while already).

<img width="1032" alt="image" src="https://github.com/user-attachments/assets/3b820bfc-970a-4315-8f2d-970591c6fdae" />

## Features

- Exposes `run_python` tool
- Safer execution of Python code compared to direct use of Python `eva()l`
- Ran via uv in Python venv
- No file I/O ops are allowed
- Restricted list of imports
    - collections
    - datetime
    - itertools
    - math
    - queue
    - random
    - re
    - stat
    - statistics
    - time
    - unicodedata

## Security

Be careful with execution of code produced by LLM on your machine, stay away from MCP servers that run Python via command line or using `eval()`. The safest option is using a VM or a docker container, though it requires some effort to set-up, consumes resources/slower. There're 3rd party servcices providing Python runtime, though they require registration, API keys etc.

`LocalPythonExecutor` provides a good balance between direct use of local Python environment (which is easier to set-up) AND remote execution in Dokcer container or a VM/3rd party service (which is safe). Hugginng Face team has invested time creating a quick and safe option to run LLM generated code used by their code agents. This MCP server builds upon it:

>To add a first layer of security, code execution in smolagents is not performed by the vanilla Python interpreter. We have re-built a more secure LocalPythonExecutor from the ground up.

Read more [here](https://huggingface.co/docs/smolagents/en/tutorials/secure_code_execution#local-code-execution).

## Installation and Execution

1. Install `uv` (e.h. `brew install uv` on macOS or use [official docs](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2))
2. Clone the repo, change the directory `cd mcp_safe_local_python_executor`
3. The server can be started via command line `uv run mcp_server.py`, venv will be created automatically, depedencies (smollagents, mcp) will be installed


## Configuring Claude Desktop

1. Make sure you have Claude for Desktop installed (download from [claude.ai](https://claude.ai/desktop))
2. Edit your Claude for Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Or open Claude Desktop -> Settings -> Developer -> click "Edit Config" button

3. Add the following configuration:

```json
{
    "mcpServers": {
        "safe-local-python-executor": {
            "command": "uv",
            "args": [
                "--directory", 
                "/path/to/mcp_local_python_executor/",
                "run",
                "mcp_server.py"
            ]
        }
    }
}
```

4. Restart Claude for Desktop
5. The Python executor tool will now be available in Claude (you'll see hammer icon in the message input field)

## Example Prompts

Once configured, you can use prompts like:

- "Calculate the factorial of 5 using Python"
- "Create a list of prime numbers up to 100"
- "Solve this equation (use Python): x^2 + 5x + 6 = 0"


## Development

Clone the repo. Use `uv` to create venv, install dev dependencies, run tests:

```
uv venv .venv
uv sync --group dev
python -m pytest tests/
```
