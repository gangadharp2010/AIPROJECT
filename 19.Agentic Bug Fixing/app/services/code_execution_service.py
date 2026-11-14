"""Demo-only Python source loader and executor.

SECURITY: exec() is not a sandbox. Never run untrusted code in this process.
Move execution into a separately hardened sandbox before production use.
"""
# import ast
# from typing import Any, Callable
# from app.services.code_analysis_service import validate_function_source

# def load_function(source: str, expected_name: str | None = None) -> Callable[..., Any]:
#     name = validate_function_source(source)
#     if expected_name and name != expected_name:
#         raise ValueError(f"Expected function '{expected_name}', received '{name}'.")
#     namespace: dict[str, Any] = {}
#     compiled = compile(ast.parse(source), "<submitted-code>", "exec")
#     exec(compiled, namespace)  # noqa: S102 - explicitly demo-only; see module warning
#     function = namespace.get(name)
#     if not callable(function):
#         raise ValueError(f"Function '{name}' could not be loaded.")
#     return function

# def execute_function(function: Callable[..., Any], arguments: list[Any]) -> Any:
#     return function(*arguments)


import ast

from app.services.code_analysis_service import normalize_code

from app.services.code_analysis_service import validate_function_source


import ast

from app.services.code_analysis_service import normalize_code


def load_function(source_code: str, expected_name: str):
    source_code = normalize_code(source_code)

    try:
        tree = ast.parse(source_code)
    except SyntaxError as exc:
        raise ValueError(
            f"Invalid Python syntax: {exc.msg}"
        ) from exc

    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    if len(functions) != 1:
        raise ValueError(
            "Source must contain exactly one function"
        )

    function_node = functions[0]

    if function_node.name != expected_name:
        raise ValueError(
            f"Expected function '{expected_name}', "
            f"but found '{function_node.name}'"
        )

    namespace = {}

    compiled = compile(tree, "<user_code>", "exec")
    exec(compiled, namespace)

    return namespace[expected_name]


def execute_function(source_code: str, expected_name: str, *args, **kwargs):
    """Load and execute a function."""

    function = load_function(source_code, expected_name)

    return function(*args, **kwargs)
