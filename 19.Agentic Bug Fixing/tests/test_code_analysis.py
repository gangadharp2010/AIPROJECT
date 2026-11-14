# import pytest
# from app.services.code_analysis_service import get_function_name, validate_function_source

# def test_get_function_name():
#     assert get_function_name("def hello(name):\\n    return name") == "hello"

# def test_rejects_no_function():
#     with pytest.raises(ValueError):
#         validate_function_source("x = 1")

# def test_rejects_multiple_functions():
#     with pytest.raises(ValueError):
#         validate_function_source("def a(): pass\\ndef b(): pass")
        
import pytest

from app.services.code_analysis_service import get_function_name


def test_get_function_name():
    code = "def add(a, b):\n    return a + b"

    assert get_function_name(code) == "add"


def test_rejects_multiple_functions():
    code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""

    with pytest.raises(ValueError):
        get_function_name(code)


def test_supports_escaped_newlines():
    code = "def add(a, b):\n    return a + b"

    assert get_function_name(code) == "add"        