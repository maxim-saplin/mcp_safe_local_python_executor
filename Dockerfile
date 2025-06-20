# Generated by https://smithery.ai. See: https://smithery.ai/docs/build/project-config
FROM ghcr.io/astral-sh/uv:alpine

# Install build dependencies
WORKDIR /app

# Copy project files
COPY . .

# Pre-create virtual environment and install dependencies to avoid runtime downloads
RUN uv venv .venv \
    && uv sync --no-dev

# Default command to run the MCP server
CMD ["uv", "run", "mcp_server.py"]
