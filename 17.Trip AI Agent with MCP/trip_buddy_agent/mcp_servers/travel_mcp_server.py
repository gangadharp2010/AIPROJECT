
import sys
import logging
from pathlib import Path

# --------------------------------------------------
# Logging: keep stdout reserved for MCP messages
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

from tools.travel_tools import (
    list_destinations,
    estimate_trip,
    compare_budget
)

# --------------------------------------------------
# MCP Server
# --------------------------------------------------

mcp = FastMCP("Trip Buddy Travel Server")


@mcp.tool()
def get_destinations() -> list:
    """Retrieve all available travel destinations."""
    logging.info("Retrieving travel destinations")
    return list_destinations()


@mcp.tool()
def calculate_trip_cost(
    destination: str,
    friends: int,
    nights: int,
    budget_per_person: float = None
) -> dict:
    """Calculate estimated trip cost."""

    logging.info(
        "Calculating trip cost for %s, %s friends, %s nights",
        destination,
        friends,
        nights
    )

    return estimate_trip(
        destination=destination,
        friends=friends,
        nights=nights,
        budget_per_person=budget_per_person
    )


@mcp.tool()
def find_destinations_by_budget(
    budget_per_person: float,
    friends: int,
    nights: int
) -> list:
    """Find destinations within the specified budget."""

    logging.info(
        "Finding destinations within budget %s",
        budget_per_person
    )

    return compare_budget(
        budget_per_person=budget_per_person,
        friends=friends,
        nights=nights
    )


# --------------------------------------------------
# Start Server
# --------------------------------------------------

if __name__ == "__main__":
    logging.info("Starting Travel MCP Server")
    mcp.run(transport="stdio")
