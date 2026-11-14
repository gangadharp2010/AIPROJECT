"""Placeholder for future HTTP API tests; the current UI is Gradio."""
def test_project_imports():
    from app.services.code_diff_service import diff_to_html
    assert "diff-empty" in diff_to_html("same", "same")
