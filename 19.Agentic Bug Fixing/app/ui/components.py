"""Small UI rendering helpers."""
import html

def error_panel(message: str) -> str:
    return f'<div class="diff-empty">{html.escape(message)}</div>'
