from app.services.code_diff_service import unified_diff, diff_to_html

def test_diff_contains_added_and_removed_lines():
    diff = unified_diff("x = 1", "x = 2")
    assert "-x = 1" in diff
    assert "+x = 2" in diff

def test_html_escapes_code():
    rendered = diff_to_html("def f():\n    return 1", "def f():\n    return 2")
    assert "diff-added" in rendered
