
import difflib
import html


def unified_diff(old_code: str, new_code: str) -> str:
    """Generate a unified diff between two code strings."""

    old_lines = old_code.splitlines()
    new_lines = new_code.splitlines()

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="original",
        tofile="modified",
        lineterm=""
    )

    return "\n".join(diff)


def diff_to_html(old_code: str, new_code: str) -> str:
    """Convert a unified diff into escaped HTML."""

    if old_code == new_code:
        return (
            '<div class="code-diff diff-empty">'
            'No changes detected'
            '</div>'
        )
        
    diff = unified_diff(old_code, new_code)

    if not diff:
        return (
            '<div class="code-diff diff-empty">'
            'No changes detected'
            '</div>'
        )

    html_lines = []

    for line in diff.splitlines():
        escaped_line = html.escape(line)

        if line.startswith(("--- ", "+++ ")):
            css_class = "diff-header"
        elif line.startswith("+"):
            css_class = "diff-added"
        elif line.startswith("-"):
            css_class = "diff-removed"
        else:
            css_class = "diff-unchanged"

        html_lines.append(
            f'<div class="{css_class}">{escaped_line}</div>'
        )

    return (
        '<div class="code-diff">'
        + "\n".join(html_lines)
        + "</div>"
    )
