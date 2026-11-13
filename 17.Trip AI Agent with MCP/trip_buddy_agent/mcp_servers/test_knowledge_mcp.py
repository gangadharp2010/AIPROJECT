print("1. Starting Knowledge MCP test...", flush=True)

from mcp_client.client import call_mcp_tool

print("2. MCP client imported.", flush=True)

result = call_mcp_tool(
    server_name="knowledge",
    tool_name="search_travel_knowledge",
    arguments={
        "query": "Manali weather in July",
        "top_k": 3
    }
)

print("3. MCP call completed.", flush=True)
print("Knowledge MCP Result:", flush=True)
print(result, flush=True)