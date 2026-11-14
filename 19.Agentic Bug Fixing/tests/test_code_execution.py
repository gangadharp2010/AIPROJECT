# import pytest
# from app.services.code_execution_service import load_function, execute_function

# def test_load_and_execute_function():
#     fn = load_function("def add(a, b):\\n    return a + b")
#     assert execute_function(fn, [2, 3]) == 5

# def test_expected_name_mismatch():
#     with pytest.raises(ValueError):
#         load_function("def add(a, b):\\n    return a + b", "subtract")

import pytest

from app.services.code_execution_service import load_function, execute_function


def test_load_and_execute_function():
    code = """
def add(a, b):
    return a + b
"""

    func = load_function(code, "add")

    assert func(2, 3) == 5


def test_expected_name_mismatch():
    code = """
def add(a, b):
    return a + b
"""

    with pytest.raises(ValueError):
        load_function(code, "subtract")


def test_rejects_multiple_functions():
    code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""

    with pytest.raises(ValueError):
        load_function(code, "add")