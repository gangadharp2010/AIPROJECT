# """LangGraph state definition."""
# from typing import Any, Callable, TypedDict

# class BugFixState(TypedDict, total=False):
#     function: Callable[..., Any]
#     function_name: str
#     original_code: str
#     current_code: str
#     arguments: list[Any]
#     error: bool
#     error_description: str
#     result: Any
#     attempts: int
#     execution_log: list[str]
    
from typing import TypedDict, Any


class BugFixState(TypedDict, total=False):
    function_name: str
    original_code: str
    current_code: str
    arguments: list
    error: bool
    error_type: str
    error_description: str
    attempts: int
    execution_log: list
    result: Any
    function: Any    
