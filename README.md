# LangGraph Projects

A collection of agent-based applications built with LangGraph, featuring MCP (Model Control Protocol) servers and research agents.

## Features

- **MCP Agent**: Orchestrates multiple MCP servers including calculator and weather services
- **Research Agent**: Combines calculator and web search capabilities for research tasks
- **MCP Servers**:
  - Calculator server with basic arithmetic operations
  - Weather server (implementation in progress)

## Prerequisites

- Python 3.12+
- OpenAI API key (set in `.env` file)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### MCP Agent
Run the MCP agent with calculator and weather services:
```bash
python mcp_agent.py
```

Run tests for MCP agent:
```bash
python mcp_agent.py --test
```

```bash
uv run pytest test_mcp_agent.py -v
```

Or to run all tests in the project:
```bash
uv run pytest -v
```

### Research Agent
Run the research agent with calculator and web search capabilities:
```bash
python research_agent.py
```

### MCP Servers
Start individual MCP servers:
```bash
# Calculator server
python mcp_servers/calc_server.py

# Weather server (if available)
python mcp_servers/weather_server.py
```

## Project Structure

- `mcp_agent.py`: Main MCP agent implementation
- `research_agent.py`: Research agent with calculator and web search
- `mcp_servers/`: Directory containing MCP server implementations
  - `calc_server.py`: Calculator MCP server
  - `weather_server.py`: Weather MCP server (in development)

## Dependencies

- langgraph
- langchain
- langchain-openai
- mcp
- duckduckgo-search
- python-dotenv

