"""
mcp_server.py
MCP (Model Context Protocol) server that exposes R&D tools to agents.

This implements the MCP concept from the course:
- Tools are exposed as callable endpoints via the MCP protocol
- Agents discover and call these tools at runtime
- The server enforces allowed actions from constraints.json

Run standalone for testing:
    python -m src.tools.mcp_server

Or imported and used programmatically by agents.
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import asyncio
import json

from src.tools.experiment_lookup import (
    get_all_experiments,
    get_successful_experiments,
    get_experiment_by_id,
    get_top_alignment_experiments,
    get_experiments_by_control,
)
from src.tools.constraints_tool import (
    get_all_constraints,
    get_operational_constraints,
    get_decision_rules,
    get_allowed_actions,
)

# Create the MCP server instance
app = Server("rd-prioritization-agent")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """Declare all tools that this MCP server exposes to agents."""
    return [
        types.Tool(
            name="get_all_experiments",
            description="Returns full experiment history as a list of records.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_successful_experiments",
            description="Returns experiments with success or partial_success outcome only.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_experiment_by_id",
            description="Returns a single experiment record by its ID string.",
            inputSchema={
                "type": "object",
                "properties": {
                    "experiment_id": {"type": "string", "description": "The experiment ID, e.g. EXP007"}
                },
                "required": ["experiment_id"],
            },
        ),
        types.Tool(
            name="get_top_alignment_experiments",
            description="Returns top-k experiments ranked by alignment score.",
            inputSchema={
                "type": "object",
                "properties": {
                    "top_k": {"type": "integer", "description": "Number of top experiments to return", "default": 3}
                },
                "required": [],
            },
        ),
        types.Tool(
            name="get_experiments_by_control",
            description="Returns all experiments using a specific control parameter.",
            inputSchema={
                "type": "object",
                "properties": {
                    "control_parameter": {"type": "string", "description": "e.g. gradient_field, pulsed_field"}
                },
                "required": ["control_parameter"],
            },
        ),
        types.Tool(
            name="get_all_constraints",
            description="Returns full project constraints including budget, time, scoring rules.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_operational_constraints",
            description="Returns only operational constraints like budget and time limits.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_decision_rules",
            description="Returns decision rules such as minimum stability threshold and target alignment.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Route incoming tool calls to the correct function."""
    result = None

    if name == "get_all_experiments":
        result = get_all_experiments()
    elif name == "get_successful_experiments":
        result = get_successful_experiments()
    elif name == "get_experiment_by_id":
        result = get_experiment_by_id(arguments.get("experiment_id", ""))
    elif name == "get_top_alignment_experiments":
        result = get_top_alignment_experiments(arguments.get("top_k", 3))
    elif name == "get_experiments_by_control":
        result = get_experiments_by_control(arguments.get("control_parameter", ""))
    elif name == "get_all_constraints":
        result = get_all_constraints()
    elif name == "get_operational_constraints":
        result = get_operational_constraints()
    elif name == "get_decision_rules":
        result = get_decision_rules()
    else:
        result = {"error": f"Unknown tool: {name}"}

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    """Run the MCP server over stdio (for use with ADK or Antigravity)."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
