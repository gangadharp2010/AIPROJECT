"""LangGraph workflow: execute -> route -> generate fix -> execute."""
import json
from langgraph.graph import END, StateGraph
from app.agents.state import BugFixState
from app.agents.prompts import FIX_PROMPT
from app.config.settings import settings
from app.services.code_execution_service import load_function, execute_function
from app.services.openai_service import create_chat_model
import ast

def clean_model_code(content: str) -> str:
    text = (content or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()

def repair_division_by_zero(
    source_code: str,
    function_name: str
) -> str:
    """Add a zero-denominator guard to a simple division return."""

    tree = ast.parse(source_code)

    function = next(
        (
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function_name
        ),
        None
    )

    if function is None:
        raise ValueError(f"Function '{function_name}' not found")

    for index, statement in enumerate(function.body):

        if (
            isinstance(statement, ast.Return)
            and isinstance(statement.value, ast.BinOp)
            and isinstance(statement.value.op, ast.Div)
            and isinstance(statement.value.right, ast.Name)
        ):
            denominator = statement.value.right.id

            guard = ast.If(
                test=ast.Compare(
                    left=ast.Name(id=denominator, ctx=ast.Load()),
                    ops=[ast.Eq()],
                    comparators=[ast.Constant(value=0)]
                ),
                body=[ast.Return(value=ast.Constant(value=0))],
                orelse=[]
            )

            function.body.insert(index, guard)

            ast.fix_missing_locations(tree)

            return ast.unparse(tree)

    raise ValueError("No supported division return statement found")

class BugFixGraph:
    def __init__(self):
        self.llm = create_chat_model()
        self.fix_chain = FIX_PROMPT | self.llm
        self.graph = self._build()

    def execute_node(self, state: BugFixState) -> dict:
        log = list(state.get("execution_log", []))
        try:
            fn = load_function(state["current_code"], state["function_name"])
            result = execute_function(fn, state.get("arguments", []))
            log.append(f"Execution succeeded: {result!r}")
            
            return {"function": fn, "error": False, "error_description": "", "result": result, "execution_log": log}
        except Exception as exc:
            description = f"{type(exc).__name__}: {str(exc)}"
            log.append(f"Execution failed: {description}")
            return {"error": True, "error_description": description, "execution_log": log}

    def fix_node(self, state: BugFixState) -> dict:
        attempt = state.get("attempts", 0) + 1
        log = list(state.get("execution_log", []))
        log.append(f"Requesting AI repair {attempt}/{settings.max_fix_attempts}")
        response = self.fix_chain.invoke({
            "function_source": state["current_code"],
            "arguments": json.dumps(state.get("arguments", []), default=str),
            "error_description": state.get("error_description", ""),
        })
        candidate = clean_model_code(response.content)
        # Validate the candidate before allowing the next execution iteration.
        load_function(candidate, state["function_name"])
        log.append("AI-generated function passed basic syntax/name validation.")
        return {"current_code": candidate, "attempts": attempt, "execution_log": log}

    @staticmethod
    def route(state: BugFixState) -> str:
        if not state.get("error"):
            return END
        if state.get("attempts", 0) >= settings.max_fix_attempts:
            return END
        return "fix"

    def _build(self):
        builder = StateGraph(BugFixState)
        builder.add_node("execute", self.execute_node)
        builder.add_node("fix", self.fix_node)
        builder.set_entry_point("execute")
        builder.add_conditional_edges("execute", self.route, {END: END, "fix": "fix"})
        builder.add_edge("fix", "execute")
        return builder.compile()

    def run(self, code: str, arguments: list) -> dict:
        from app.services.code_analysis_service import validate_function_source
        name = validate_function_source(code)
        initial: BugFixState = {
            "function_name": name,
            "original_code": code,
            "current_code": code,
            "arguments": arguments,
            "error": False,
            "error_description": "",
            "attempts": 0,
            "execution_log": [],
        }
        return self.graph.invoke(initial)
