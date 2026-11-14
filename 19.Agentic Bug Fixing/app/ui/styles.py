"""Custom CSS for the Gradio interface."""
CUSTOM_CSS = """
.gradio-container {max-width: 1450px !important; margin: auto !important;}
#run-button {background: #e85d1f !important; color: white !important; border: 0 !important;}
.diff-viewer {background:#f6f8fa;border-radius:8px;padding:14px;overflow-x:auto;}
.diff-viewer pre {margin:0;font-family:ui-monospace,Consolas,monospace;font-size:13px;line-height:1.55;}
.diff-file {font-weight:700;color:#24292f;}
.diff-hunk {color:#0969da;font-weight:600;}
.diff-removed {background:#ffebe9;color:#cf222e;}
.diff-added {background:#dafbe1;color:#1a7f37;}
.diff-context {color:#57606a;}
.diff-empty {background:#dafbe1;color:#1a7f37;padding:14px;border-radius:8px;}
.note {font-size:.9rem;color:#6b7280;}
"""
