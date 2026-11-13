
import re
import json
from typing import Any


class ResponseFormatter:
    """
    Formats Trip Buddy responses into user-friendly Markdown.

    Supports:
    - Trip cost estimates
    - Budget comparisons
    - Destination lists
    - Itineraries
    - Seasonal travel advice
    - General responses
    """

    def format_response(self, response: Any) -> str:
        """
        Main formatting entry point.
        """

        if response is None:
            return "Sorry, I couldn't generate a travel recommendation."

        if isinstance(response, dict):
            return self._format_dict(response)

        if isinstance(response, list):
            return self._format_list(response)

        if not isinstance(response, str):
            response = str(response)

        text = response.strip()

        if not text:
            return "I couldn't find a useful response. Please try again."

        # Try to parse JSON returned as text.
        parsed = self._try_parse_json(text)

        if parsed is not None:
            return self.format_response(parsed)

        # Already structured Markdown or conversational text.
        if self._is_formatted_markdown(text):
            return self._clean_markdown(text)

        # Detect common response types.
        if self._is_budget_response(text):
            return self._format_budget_text(text)

        if self._is_seasonal_response(text):
            return self._format_seasonal_text(text)

        return self._clean_markdown(text)

    # ======================================================
    # JSON PARSING
    # ======================================================

    def _try_parse_json(self, text: str):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return None

    # ======================================================
    # DICTIONARY FORMATTER
    # ======================================================

    def _format_dict(self, data: dict) -> str:

        # Handle MCP calculate_trip_cost result.
        if "estimated_per_person" in data:
            return self._format_trip_cost(data)

        # Handle destination objects.
        if "destinations" in data:
            return self._format_destination_list(
                data["destinations"]
            )

        # Handle itinerary.
        if "itinerary" in data:
            return self._format_itinerary(data["itinerary"])

        return self._format_generic_dict(data)

    # ======================================================
    # TRIP COST FORMATTER
    # ======================================================

    def _format_trip_cost(self, data: dict) -> str:

        destination = data.get("destination", "Your trip")

        friends = data.get("friends", 1)

        nights = data.get("nights", 0)

        per_person = float(
            data.get("estimated_per_person", 0)
        )

        group_total = float(
            data.get(
                "estimated_group_total",
                per_person * friends
            )
        )

        budget = data.get("budget_per_person")

        within_budget = data.get("within_budget")

        remaining = None

        if budget is not None:
            remaining = float(budget) - per_person

            # Calculate budget status if missing.
            if within_budget is None:
                within_budget = remaining >= 0

        status = (
            "Within budget"
            if within_budget
            else "Over budget"
        )

        percentage = None

        if budget and float(budget) > 0:
            percentage = min(
                100,
                max(0, per_person / float(budget) * 100)
            )

        result = [
            f"## 🏖️ {destination} Trip Estimate",
            "",
            f"**{friends} friends · {nights} nights**",
            "",
            f"### {'✅' if within_budget else '⚠️'} {status}",
            "",
            "| Budget Details | Amount |",
            "|---|---:|",
            f"| Cost per person | **{self._money(per_person)}** |",
            f"| Group total | **{self._money(group_total)}** |",
        ]

        if budget is not None:
            result.extend([
                f"| Budget per person | {self._money(float(budget))} |",
                f"| Remaining per person | **{self._money(remaining)}** |",
                "",
                "### 📊 Budget Utilization",
                "",
                f"`{percentage:.1f}%` of your budget is utilized.",
                "",
                self._progress_bar(percentage),
            ])

        result.extend([
            "",
            "### 📝 Assumptions",
            "",
            data.get(
                "assumption",
                "This is an estimated trip cost, not a live quote."
            ),
            "",
            "> Intercity travel costs may not be included.",
        ])

        return "\n".join(result)

    # ======================================================
    # DESTINATION LIST FORMATTER
    # ======================================================

    def _format_list(self, data: list) -> str:

        if not data:
            return "No travel destinations were found."

        if all(isinstance(item, dict) for item in data):
            return self._format_destination_list(data)

        lines = ["## 📍 Travel Recommendations", ""]

        for index, item in enumerate(data, start=1):
            lines.append(f"{index}. {item}")

        return "\n".join(lines)

    def _format_destination_list(self, destinations: list) -> str:

        lines = [
            "## 🌍 Available Travel Destinations",
            "",
            "| Destination | State | Category | Rate / Person / Night |",
            "|---|---|---|---:|"
        ]

        for destination in destinations:

            name = destination.get(
                "destination",
                destination.get("name", "Unknown")
            )

            state = destination.get("state", "-")

            category = destination.get("category", "-")

            rate = destination.get(
                "cost_per_person",
                destination.get(
                    "price_per_person",
                    destination.get("rate_per_person_night")
                )
            )

            rate_text = (
                self._money(float(rate))
                if rate is not None
                else "-"
            )

            lines.append(
                f"| {name} | {state} | {category} | {rate_text} |"
            )

        lines.extend([
            "",
            "💡 **Tip:** Share your budget, group size and "
            "number of nights to compare destinations."
        ])

        return "\n".join(lines)

    # ======================================================
    # ITINERARY FORMATTER
    # ======================================================

    def _format_itinerary(self, itinerary: list) -> str:

        lines = [
            "## 🗺️ Your Travel Itinerary",
            ""
        ]

        for index, day in enumerate(itinerary, start=1):

            if isinstance(day, dict):

                title = day.get(
                    "title",
                    day.get("day", f"Day {index}")
                )

                lines.extend([
                    f"### 📅 {title}",
                    ""
                ])

                for period in [
                    "morning",
                    "afternoon",
                    "evening"
                ]:
                    activity = day.get(period)

                    if activity:
                        lines.append(
                            f"- **{period.title()}:** {activity}"
                        )

            else:
                lines.append(f"### Day {index}")
                lines.append(str(day))

            lines.append("")

        return "\n".join(lines)

    # ======================================================
    # GENERIC DICTIONARY FORMATTER
    # ======================================================

    def _format_generic_dict(self, data: dict) -> str:

        lines = ["## ✈️ Trip Buddy Recommendation", ""]

        for key, value in data.items():

            label = key.replace("_", " ").title()

            if isinstance(value, (dict, list)):
                lines.append(f"### {label}")
                lines.append("")
                lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            else:
                lines.append(f"- **{label}:** {value}")

        return "\n".join(lines)

    # ======================================================
    # BUDGET TEXT DETECTION
    # ======================================================

    def _is_budget_response(self, text: str) -> bool:

        keywords = [
            "estimated cost per person",
            "estimated_per_person",
            "group total",
            "within your budget",
            "budget per person"
        ]

        text_lower = text.lower()

        return any(
            keyword in text_lower
            for keyword in keywords
        )

    def _format_budget_text(self, text: str) -> str:

        # Preserve an already readable answer rather than
        # trying to guess values from arbitrary prose.
        return (
            "## 💰 Trip Budget Summary\n\n"
            + self._clean_markdown(text)
        )

    # ======================================================
    # SEASONAL ADVICE FORMATTER
    # ======================================================

    def _is_seasonal_response(self, text: str) -> bool:

        keywords = [
            "monsoon",
            "weather",
            "rainfall",
            "landslide",
            "season",
            "climate"
        ]

        text_lower = text.lower()

        return any(
            keyword in text_lower
            for keyword in keywords
        )

    def _format_seasonal_text(self, text: str) -> str:

        return (
            "## 🌦️ Seasonal Travel Advice\n\n"
            + self._clean_markdown(text)
        )

    # ======================================================
    # MARKDOWN CLEANUP
    # ======================================================

    def _is_formatted_markdown(self, text: str) -> bool:

        return bool(
            re.search(
                r"(^#{1,3}\s|\n[-*]\s|\n\|.*\|)",
                text
            )
        )

    def _clean_markdown(self, text: str) -> str:

        # Remove excessive blank lines.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    # ======================================================
    # HELPERS
    # ======================================================

    @staticmethod
    def _money(value: float) -> str:

        return f"₹{value:,.0f}"

    @staticmethod
    def _progress_bar(percentage: float) -> str:

        filled = round(percentage / 10)

        filled = max(0, min(10, filled))

        empty = 10 - filled

        return (
            f"`{'█' * filled}{'░' * empty}` "
            f"**{percentage:.1f}%**"
        )
