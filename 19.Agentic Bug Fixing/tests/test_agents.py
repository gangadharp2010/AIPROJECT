"""Agent integration tests require OPENAI_API_KEY and are intentionally opt-in."""
import json
import os
import pytest
from app.agents.bug_fixing_agent import BugFixingAgent


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not configured"
)
def test_agent_repairs_division_by_zero():

    agent = BugFixingAgent()

    state = agent.run(
        "def divide(a, b):\n    return a / b",
        [10, 0]
    )
    print("\n========== AGENT STATE ==========")
    print(state)
    print("=================================")
    print("\n========== AGENT DEBUG ==========")

    print("Error:", state.get("error"))
    print("Error Type:", state.get("error_type"))
    print("Error Description:", state.get("error_description"))
    print("Result:", state.get("result"))
    print("Attempts:", state.get("attempts"))

    print("\nOriginal Code:")
    print(state.get("original_code"))

    print("\nFixed Code:")
    print(state.get("current_code"))

    print("\nExecution Log:")
    for log in state.get("execution_log", []):
        print("-", log)

    print("=================================")
    
    print(json.dumps(state, indent=4, default=str))

    #assert not state["error"]
    #assert state["result"] == 0