
import sys
import logging
from pathlib import Path

# --------------------------------------------------
# Logging: STDIO protocol uses stdout.
# All application logs must go to stderr.
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(levelname)s: %(message)s",
    force=True
)

# --------------------------------------------------
# Add project root to Python import path
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# --------------------------------------------------
# Imports
# --------------------------------------------------

from mcp.server.fastmcp import FastMCP
from rag.retriever import search_knowledge

# --------------------------------------------------
# MCP Server
# --------------------------------------------------

mcp = FastMCP("Trip Buddy Knowledge Server")


@mcp.tool()
def search_travel_knowledge(
    query: str,
    top_k: int = 3
) -> list:
    """
    Search travel knowledge documents using RAG.

    Args:
        query: Travel-related question.
        top_k: Maximum number of relevant documents.
    """

    logging.info("Searching travel knowledge: %s", query)

    return search_knowledge(
        query=query,
        top_k=top_k
    )


# --------------------------------------------------
# Start Server
# --------------------------------------------------

if __name__ == "__main__":
    logging.info("Starting Knowledge MCP Server")
    mcp.run(transport="stdio")
