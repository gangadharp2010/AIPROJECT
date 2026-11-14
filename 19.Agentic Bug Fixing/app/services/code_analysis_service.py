"""Static validation helpers for submitted Python source."""
import ast

def get_function_name(source_code: str) -> str:
    """Extract exactly one top-level function name."""

    tree = parse_code(source_code)

    functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    if len(functions) == 0:
        raise ValueError("No function found in source code")

    if len(functions) > 1:
        raise ValueError("Multiple functions found in source code")

    return functions[0].name

def validate_function_source(source_code: str) -> str:
    name = get_function_name(source_code)
    tree = parse_code(source_code)
    top_level = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    if len(top_level) != 1:
        raise ValueError("Provide exactly one top-level function definition.")
    return name

def normalize_code(source_code: str) -> str:
    """Normalize source code containing escaped newline characters."""

    if not isinstance(source_code, str):
        raise TypeError("Source code must be a string")

    source_code = source_code.strip()

    # Convert literal backslash-n into actual newline characters.
    source_code = source_code.replace("\\r\\n", "\n")
    source_code = source_code.replace("\\n", "\n")

    return source_code


def parse_code(source_code: str) -> ast.Module:
    """Parse Python source code."""

    normalized = normalize_code(source_code)

    try:
        return ast.parse(normalized)
    except SyntaxError as exc:
        raise ValueError(
            f"Invalid Python syntax: {exc.msg}, "
            f"line {exc.lineno}"
        ) from exc
