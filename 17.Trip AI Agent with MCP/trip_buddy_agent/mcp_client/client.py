import os
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parent.parent


SERVERS = {
    "travel": BASE_DIR / "mcp_servers" / "travel_mcp_server.py",
    "knowledge": BASE_DIR / "mcp_servers" / "knowledge_mcp_server.py"
}


async def discover_and_call(server_name, tool_name=None, arguments=None):

    server_path = SERVERS[server_name]

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        env=None
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP connection
            await session.initialize()

            # Discover available tools
            tools_response = await session.list_tools()

            discovered_tools = tools_response.tools

            if tool_name is None:
                return [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema
                    }
                    for tool in discovered_tools
                ]

            available_names = {
                tool.name for tool in discovered_tools
            }

            if tool_name not in available_names:
                raise ValueError(
                    f"Tool {tool_name} not found on {server_name}"
                )

            # Execute MCP tool
            result = await session.call_tool(
                tool_name,
                arguments=arguments or {}
            )

            if result.isError:
                raise RuntimeError(
                    f"MCP tool failed: {result.content}"
                )

            if result.structuredContent is not None:
                return result.structuredContent

            return [
                item.model_dump(mode="json")
                for item in result.content
            ]


def list_mcp_tools(server_name):
    return asyncio.run(
        discover_and_call(server_name)
    )


def call_mcp_tool(server_name, tool_name, arguments):
    return asyncio.run(
        discover_and_call(
            server_name,
            tool_name,
            arguments
        )
    )


if __name__ == "__main__":

    print("Travel tools:")
    print(json.dumps(
        list_mcp_tools("travel"),
        indent=2
    ))

    print("\nKnowledge tools:")
    print(json.dumps(
        list_mcp_tools("knowledge"),
        indent=2
    ))
