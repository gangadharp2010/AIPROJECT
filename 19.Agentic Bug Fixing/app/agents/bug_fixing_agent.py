"""Public agent facade."""
from app.agents.graph import BugFixGraph

class BugFixingAgent:
    def __init__(self):
        self.workflow = BugFixGraph()

    def run(self, code: str, arguments: list) -> dict:
        return self.workflow.run(code, arguments)
