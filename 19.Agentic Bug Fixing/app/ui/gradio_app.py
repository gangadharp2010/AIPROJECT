"""Gradio 6-compatible UI for the Agentic Bug Fixing application."""

import difflib
import json
import gradio as gr
import html

from app.agents.bug_fixing_agent import BugFixingAgent
from app.config.settings import settings
from app.examples.bug_examples import EXAMPLES
from app.services.code_diff_service import unified_diff
from app.services.code_analysis_service import validate_function_source
from app.ui.styles import CUSTOM_CSS


def launch():
    """Build and launch the Gradio application."""

    # Create the agent only when the user runs the first example.
    # This avoids initializing the OpenAI client during UI startup.
    agent_cache = {"agent": None}

    def load_example(example_name: str):
        """Load a predefined code sample and its JSON arguments."""
        example = EXAMPLES.get(example_name, {"code": "", "args": "[]"})
        return example["code"], example["args"]

    def unified_diff(original: str, fixed: str) -> str:
        """Generate a readable Git-style unified diff."""

        # Convert escaped newline sequences into real newlines
        if "\\n" in original and "\n" not in original:
            original = original.replace("\\n", "\n")

        if "\\n" in fixed and "\n" not in fixed:
            fixed = fixed.replace("\\n", "\n")

        diff_lines = difflib.unified_diff(
            original.splitlines(keepends=True),
            fixed.splitlines(keepends=True),
            fromfile="original",
            tofile="fixed",
            n=3,
        )

        return "".join(diff_lines)

    def render_diff_html(original: str, fixed: str) -> str:
        """Render a Git-style colored unified diff."""

        diff_lines = list(
            difflib.unified_diff(
                original.splitlines(),
                fixed.splitlines(),
                fromfile="original",
                tofile="fixed",
                lineterm="",
                n=3,
            )
        )

        if not diff_lines:
            return """
            <div style="padding:12px;color:#16a34a;">
                No changes detected.
            </div>
            """

        output = []

        for line in diff_lines:
            escaped = html.escape(line)

            if line.startswith("---"):
                output.append(
                    f'<div class="diff-header removed">{escaped}</div>'
                )

            elif line.startswith("+++"):
                output.append(
                    f'<div class="diff-header added">{escaped}</div>'
                )

            elif line.startswith("@@"):
                output.append(
                    f'<div class="diff-hunk">{escaped}</div>'
                )

            elif line.startswith("+"):
                output.append(
                    f'<div class="diff-added">{escaped}</div>'
                )

            elif line.startswith("-"):
                output.append(
                    f'<div class="diff-removed">{escaped}</div>'
                )

            else:
                output.append(
                    f'<div class="diff-context">{escaped}</div>'
                )

        return """
        <style>
            .git-diff {
                background: #0d1117;
                color: #e6edf3;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 14px;
                overflow-x: auto;
                font-family: Consolas, monospace;
                font-size: 13px;
                line-height: 1.7;
            }

            .git-diff div {
                white-space: pre;
                padding: 1px 8px;
            }

            .diff-header.removed {
                color: #ff7b72;
                font-weight: bold;
            }

            .diff-header.added {
                color: #3fb950;
                font-weight: bold;
            }

            .diff-hunk {
                color: #79c0ff;
                background: #161b22;
                margin: 5px 0;
            }

            .diff-added {
                color: #aff5b4;
                background: rgba(46, 160, 67, 0.20);
            }

            .diff-removed {
                color: #ffdcd7;
                background: rgba(248, 81, 73, 0.20);
            }

            .diff-context {
                color: #c9d1d9;
            }
        </style>

        <div class="git-diff">
        """ + "\n".join(output) + """
        </div>
        """
     
    def run_agent(code: str, args_text: str):
        """Run the bug-fixing workflow and return all UI outputs."""
        original_code = code or ""

        # 1. Parse function arguments supplied as JSON.
        try:
            arguments = json.loads(args_text or "[]")
            if not isinstance(arguments, list):
                arguments = [arguments]
        except json.JSONDecodeError as exc:
            message = f"Invalid JSON arguments: {exc}"
            return (
                original_code,
                "Not generated",
                message,
                message,
                "",
            )

        # 2. Validate that the input contains exactly one top-level function.
        try:
            validate_function_source(original_code)
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            return (
                original_code,
                "Not generated",
                message,
                message,
                "",
            )

        # 3. Initialize the agent on first use and run the LangGraph workflow.
        try:
            if agent_cache["agent"] is None:
                agent_cache["agent"] = BugFixingAgent()

            final_state = agent_cache["agent"].run(
                original_code,
                arguments,
            )
        except Exception as exc:
            message = f"Agent failed: {type(exc).__name__}: {exc}"
            return (
                original_code,
                "Agent failed",
                message,
                message,
                "",
            )

        # 4. Determine the final code and create a unified diff.
        attempts = final_state.get("attempts", 0)
        final_code = final_state.get("current_code", original_code)

        if attempts > 0 and final_code != original_code:
            fixed_code = final_code
            diff_text = render_diff_html(original_code, fixed_code)
            if not diff_text:
                diff_text = "The agent changed the code, but no diff was generated."
        else:
            fixed_code = "No fix generated."
            if final_state.get("error"):
                diff_text = (
                    "No successful code fix was generated. "
                    "Review the execution log and last error below."
                )
            else:
                diff_text = "No differences. The original code executed successfully."

        # 5. Format execution status.
        if final_state.get("error"):
            result_text = (
                f"FAILED after {attempts} fix attempt(s).\n"
                f"Last error: {final_state.get('error_description', 'Unknown error')}"
            )
        else:
            result_text = (
                "SUCCESS\n"
                f"Result: {final_state.get('result')!r}\n"
                f"Fix attempts: {attempts}"
            )

        execution_log = "\n".join(
            final_state.get("execution_log", [])
        )

        return (
            original_code,
            fixed_code,
            diff_text,
            result_text,
            execution_log,
        )

    # Select the first predefined example for the initial UI state.
    first_example = next(iter(EXAMPLES), None)
    initial_example = EXAMPLES.get(
        first_example,
        {"code": "", "args": "[]"},
    )

    # Gradio 6: theme and css are passed to launch(), not Blocks().
    with gr.Blocks(title="Agentic Bug Fixing") as demo:
        gr.Markdown("# Agentic Bug Fixing — OpenAI + LangGraph")

        gr.Markdown(
            "Enter a Python function and its arguments. If execution fails, "
            f"the agent asks **{settings.openai_model}** to propose a repair."
        )

        gr.Markdown(
            "<div class='note'>"
            "<strong>Demo safety notice:</strong> submitted and AI-generated "
            "Python code is executed by this application. Do not expose this "
            "demo publicly or run untrusted code without an isolated sandbox."
            "</div>"
        )

        example_dropdown = gr.Dropdown(
            choices=list(EXAMPLES.keys()),
            value=first_example,
            label="Load Example",
        )

        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### Python Function Code")
                code_input = gr.Code(
                    value=initial_example["code"],
                    language="python",
                    label="Python source",
                    lines=14,
                )

            with gr.Column(scale=1):
                gr.Markdown("### Function Arguments")
                arguments_input = gr.Textbox(
                    value=initial_example["args"],
                    label="Arguments (JSON format)",
                    placeholder='[10, 0] or {"key": "value"}',
                    lines=4,
                )

                run_button = gr.Button(
                    "Run Agent & Show Diff",
                    variant="primary",
                    size="lg",
                    elem_id="run-button",
                )

        gr.Markdown("### Git-Style Diff")

        # Use a plain Textbox for compatibility with Gradio 6.
        # Do not use gr.Code(language="diff"): some Gradio versions do not
        # include "diff" in the supported Code languages.
        # diff_output = gr.Textbox(
        #         label="Unified diff",
        #         lines=16,
        #         interactive=False,
        #     )
        diff_output = gr.HTML(
            label="Git-Style Diff",
            value="<div>Diff will appear here.</div>"
        )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Original Code")
                original_output = gr.Code(
                    language="python",
                    label="Original",
                    lines=12,
                    interactive=False,
                )

            with gr.Column():
                gr.Markdown("### Fixed Code")
                fixed_output = gr.Code(
                    language="python",
                    label="Fixed",
                    lines=12,
                    interactive=False,
                )

        gr.Markdown("### Execution Result")
        result_output = gr.Textbox(
            label="Status",
            lines=4,
            interactive=False,
        )

        with gr.Accordion("Agent Execution Log", open=False):
            execution_log_output = gr.Textbox(
                label="Execution log",
                lines=10,
                interactive=False,
            )

        # Load the selected predefined example.
        example_dropdown.change(
            fn=load_example,
            inputs=[example_dropdown],
            outputs=[code_input, arguments_input],
        )

        # Run the agent and update all result panels.
        run_button.click(
            fn=run_agent,
            inputs=[code_input, arguments_input],
            outputs=[
                original_output,
                fixed_output,
                diff_output,
                result_output,
                execution_log_output,
            ],
        )

    demo.queue().launch(
        server_name=settings.gradio_server_name,
        server_port=settings.gradio_server_port,
        share=False,
        theme=gr.themes.Soft(),
        css=CUSTOM_CSS,
    )



