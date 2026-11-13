
import json
import re

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from mcp_client.client import list_mcp_tools, call_mcp_tool
from agents.response_formatter import ResponseFormatter


SYSTEM_PROMPT = """
You are Trip Buddy, a careful travel-planning assistant for trips in India.

You have access to two MCP servers:
1. Travel MCP: destination lists, trip cost calculations and budget comparisons.
2. Knowledge MCP: travel knowledge and seasonal travel advice using RAG.

Rules:
- Use MCP tools for destination rates and budget calculations.
- Use MCP tools for travel knowledge and seasonal advice.
- Never invent database rates, live prices, hotel availability,
  weather or bookings.
- The database contains DEMO estimates, not live quotes.
- Estimates include the sample stay rate multiplied by nights plus
  10% for food, local transport and activities.
- Intercity travel, shopping and personal expenses are excluded
  unless stated otherwise.
- This demo does not have a live weather feed.
- Recommend checking official local advisories before travelling.
- Explain assumptions and give per-person and group totals when relevant.
- Keep answers clear and friendly.
"""


class TravelAgent:

    def __init__(self):

        self.client = (
            OpenAI(api_key=OPENAI_API_KEY)
            if OPENAI_API_KEY
            else None
        )

        self.server_mapping = {
            "travel": "travel",
            "knowledge": "knowledge"
        }
        
        self.formatter = ResponseFormatter()

    # ========================================================
    # 1. MAIN ENTRY POINT
    # ========================================================

    def ask(self, message):

        if not message or not message.strip():
            return "Please enter a travel question."

        message = message.strip()

        try:

            # ==========================================
            # 1. OPENAI + MCP ORCHESTRATION
            # ==========================================

            if self.client:

                try:
                    response = self._ask_with_openai(message)

                except Exception as exc:

                    print(
                        f"OpenAI/MCP orchestration failed: "
                        f"{type(exc).__name__}: {exc}"
                    )

                    # ==================================
                    # 2. MCP FALLBACK
                    # ==================================

                    try:
                        response = self._fallback(message)

                        if isinstance(response, str):
                            response += (
                                "\n\n_Used MCP fallback mode._"
                            )

                    except Exception as fallback_exc:

                        print(
                            f"Fallback failed: "
                            f"{type(fallback_exc).__name__}: "
                            f"{fallback_exc}"
                        )

                        return (
                            "I encountered an error while processing "
                            "your request.\n\n"
                            f"OpenAI error: {exc}\n"
                            f"Fallback error: {fallback_exc}"
                        )

            # ==========================================
            # 3. NO OPENAI API KEY
            # ==========================================

            else:
                response = self._fallback(message)

            # ==========================================
            # 4. FORMAT FINAL RESPONSE
            # ==========================================

            return self.formatter.format_response(response)

        except Exception as exc:

            print(
                f"TravelAgent error: "
                f"{type(exc).__name__}: {exc}"
            )

            return (
                "Unable to process your travel request.\n\n"
                f"Error: {type(exc).__name__}: {exc}"
            )

    # ========================================================
    # 2. MCP TOOL DISCOVERY
    # ========================================================

    def get_mcp_tool_definitions(self):

        definitions = []

        for server_name in self.server_mapping:

            discovered_tools = list_mcp_tools(server_name)

            for tool in discovered_tools:

                definitions.append({
                    "type": "function",
                    "function": {
                        "name": (
                            f"{server_name}__{tool['name']}"
                        ),
                        "description": tool.get("description") or "",
                        "parameters": tool["inputSchema"]
                    }
                })

        return definitions

    # ========================================================
    # 3. MCP TOOL EXECUTION
    # ========================================================

    def execute_mcp_tool(self, tool_name, arguments):

        if "__" not in tool_name:
            raise ValueError(
                f"Invalid MCP tool name: {tool_name}"
            )

        server_name, actual_tool_name = tool_name.split(
            "__", 1
        )

        if server_name not in self.server_mapping:
            raise ValueError(
                f"Unknown MCP server: {server_name}"
            )

        result = call_mcp_tool(
            server_name=server_name,
            tool_name=actual_tool_name,
            arguments=arguments
        )

        return self._normalize_mcp_result(result)

    # ========================================================
    # 4. NORMALIZE MCP RESPONSE
    # ========================================================

    def _normalize_mcp_result(self, result):

        if isinstance(result, list):

            normalized = []

            for item in result:

                if (
                    isinstance(item, dict)
                    and item.get("type") == "text"
                ):

                    text = item.get("text", "")

                    try:
                        parsed = json.loads(text)

                        if isinstance(parsed, list):
                            normalized.extend(parsed)
                        else:
                            normalized.append(parsed)

                    except json.JSONDecodeError:
                        normalized.append(text)

                else:
                    normalized.append(item)

            return normalized

        return result

    # ========================================================
    # 5. OPENAI + MCP TOOL ORCHESTRATION
    # ========================================================

    def _ask_with_openai(self, message):

        tools = self.get_mcp_tool_definitions()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ]

        for iteration in range(5):

            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.2
            )

            choice = response.choices[0].message

            # LLM has generated its final answer.
            if not choice.tool_calls:

                return (
                    choice.content
                    or "I couldn't generate a response."
                )

            # Append assistant tool-call message.
            messages.append(
                choice.model_dump(exclude_none=True)
            )

            # Execute all requested MCP tools.
            for tool_call in choice.tool_calls:

                tool_name = tool_call.function.name

                try:

                    arguments = json.loads(
                        tool_call.function.arguments or "{}"
                    )

                    print(
                        f"Executing MCP tool: {tool_name}"
                    )

                    result = self.execute_mcp_tool(
                        tool_name,
                        arguments
                    )

                except Exception as exc:

                    result = {
                        "error": str(exc),
                        "tool": tool_name
                    }

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str
                    )
                })

        return (
            "Unable to complete the request within "
            "the tool-call limit."
        )

    # ========================================================
    # 6. FALLBACK MODE USING MCP
    # ========================================================

    def _fallback(self, message):

        text = message.lower()

        # Get destinations through Travel MCP.
        destinations = self.execute_mcp_tool(
            "travel__get_destinations",
            {}
        )

        if not isinstance(destinations, list):
            destinations = []

        # ----------------------------------------------------
        # A. LIST DESTINATIONS
        # ----------------------------------------------------

        if text.strip() in {
            "list",
            "list destinations",
            "show destinations",
            "show me destinations"
        }:

            return self._format_destinations(destinations)

        # Extract travel details.
        friends = self._number(
            r"(\d+)\s*(?:friends|people|persons|travellers|travelers)",
            message,
            1
        )

        nights = self._number(
            r"(\d+)\s*nights?",
            message,
            2
        )

        budget = self._money(message)

        # ----------------------------------------------------
        # B. BUDGET COMPARISON
        # ----------------------------------------------------

        budget_keywords = [
            "which trips",
            "which trip",
            "fit",
            "within budget",
            "under budget",
            "destinations within"
        ]

        if any(word in text for word in budget_keywords):

            if budget is None:

                return (
                    "What is your budget per person?\n\n"
                    "Example: ₹8,000 each for 3 friends, 2 nights."
                )

            results = self.execute_mcp_tool(
                "travel__find_destinations_by_budget",
                {
                    "budget_per_person": budget,
                    "friends": friends,
                    "nights": nights
                }
            )

            if not results:

                return (
                    f"I couldn't find destinations within "
                    f"₹{budget:,.0f} per person for "
                    f"{friends} friends and {nights} nights "
                    "using the sample rates."
                )

            lines = [
                f"### Trips within ₹{budget:,.0f} per person"
            ]

            for item in results:

                if not isinstance(item, dict):
                    continue

                lines.append(
                    f"- **{item.get('destination', 'Destination')}** "
                    f"— ₹{item.get('estimated_per_person', 0):,.0f} "
                    f"per person "
                    f"(₹{item.get('estimated_group_total', 0):,.0f} "
                    f"group total)."
                )

            lines.append(
                "\nDemo estimates only. Intercity travel is excluded."
            )

            return "\n".join(lines)

        # ----------------------------------------------------
        # C. FIND DESTINATION
        # ----------------------------------------------------

        destination = next(
            (
                item.get("name")
                for item in destinations
                if isinstance(item, dict)
                and item.get("name")
                and item["name"].lower() in text
            ),
            None
        )

        seasonal_keywords = [
            "good idea",
            "july",
            "season",
            "best time",
            "weather",
            "monsoon",
            "winter",
            "summer"
        ]

        # ----------------------------------------------------
        # D. SEASONAL KNOWLEDGE THROUGH RAG MCP
        # ----------------------------------------------------

        if destination and any(
            word in text for word in seasonal_keywords
        ):

            tips = self.execute_mcp_tool(
                "knowledge__search_travel_knowledge",
                {
                    "query": (
                        f"{destination} weather season "
                        f"travel advice {message}"
                    ),
                    "top_k": 3
                }
            )

            lines = [
                f"### {destination}: seasonal travel guidance"
            ]

            for item in tips:

                if isinstance(item, dict):

                    lines.append(
                        f"- **{item.get('topic', 'Travel advice')}**: "
                        f"{item.get('content', '')}"
                    )

                elif isinstance(item, str):
                    lines.append(f"- {item}")

            lines.append(
                "\nThis is general travel guidance, not a live "
                "weather forecast. Check official local advisories."
            )

            return "\n".join(lines)

        # ----------------------------------------------------
        # E. CALCULATE TRIP COST
        # ----------------------------------------------------

        if destination:

            result = self.execute_mcp_tool(
                "travel__calculate_trip_cost",
                {
                    "destination": destination,
                    "friends": friends,
                    "nights": nights,
                    "budget_per_person": budget
                }
            )

            if isinstance(result, dict) and result.get("error"):
                return result["error"]

            if not isinstance(result, dict):
                return str(result)

            return (
                f"### {destination} trip estimate\n\n"
                f"- Friends: **{friends}**\n"
                f"- Nights: **{nights}**\n"
                f"- Estimated per person: "
                f"**₹{result.get('estimated_per_person', 0):,.0f}**\n"
                f"- Estimated group total: "
                f"**₹{result.get('estimated_group_total', 0):,.0f}**\n\n"
                f"**Assumption:** "
                f"{result.get('assumption', 'Sample database estimate')}\n\n"
                "These are demo estimates, not live quotes. "
                "Intercity travel is excluded."
            )

        # ----------------------------------------------------
        # F. GENERAL TRAVEL KNOWLEDGE
        # ----------------------------------------------------

        tips = self.execute_mcp_tool(
            "knowledge__search_travel_knowledge",
            {
                "query": message,
                "top_k": 3
            }
        )

        if tips:

            lines = ["### Travel knowledge"]

            for item in tips:

                if isinstance(item, dict):

                    lines.append(
                        f"- **{item.get('topic', 'Travel tip')}**: "
                        f"{item.get('content', '')}"
                    )

                elif isinstance(item, str):
                    lines.append(f"- {item}")

            return "\n".join(lines)

        return (
            "I can help you with:\n\n"
            "- Available destinations\n"
            "- Group trip cost calculations\n"
            "- Budget comparisons\n"
            "- Seasonal travel advice\n\n"
            "Example: How much is Goa for 4 friends, 3 nights?"
        )

    # ========================================================
    # 7. FORMAT DESTINATIONS
    # ========================================================

    def _format_destinations(self, destinations):

        if not destinations:
            return "No destinations found in the database."

        lines = [
            "### Destinations in the sample database"
        ]

        for item in destinations:

            if not isinstance(item, dict):
                continue

            lines.append(
                f"- **{item.get('name', 'Unknown')}**, "
                f"{item.get('state', '')} "
                f"({item.get('category', '')}) — "
                f"₹{item.get('cost_per_person_per_night', 0):,.0f}"
                f"/person/night; "
                f"recommended {item.get('recommended_nights', 0)} nights."
            )

        lines.append(
            "\nThese are demo estimates, not live quotes."
        )

        return "\n".join(lines)

    # ========================================================
    # 8. EXTRACT NUMBERS
    # ========================================================

    @staticmethod
    def _number(pattern, text, default):

        match = re.search(pattern, text, re.IGNORECASE)

        return int(match.group(1)) if match else default

    # ========================================================
    # 9. EXTRACT BUDGET
    # ========================================================

    @staticmethod
    def _money(text):

        match = re.search(
            r"(?:₹|rs\.?\s*)([\d,]+)",
            text,
            re.IGNORECASE
        )

        if not match:

            match = re.search(
                r"([\d,]+)\s*(?:rupees|inr)",
                text,
                re.IGNORECASE
            )

        if match:
            return int(match.group(1).replace(",", ""))

        return None