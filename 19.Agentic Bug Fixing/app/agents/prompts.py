"""Prompt templates for automated bug repair."""
from langchain_core.prompts import ChatPromptTemplate

FIX_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a careful Python debugging assistant.
Repair the supplied Python function based on the observed exception.

Rules:
- Preserve the exact function name and parameter names/order.
- Make the smallest reasonable correction.
- Handle the reported failure safely and explicitly.
- Return exactly one complete Python function definition.
- Return no Markdown fences, explanation, imports, classes, or extra functions.
- Do not hide unrelated errors with a broad except Exception.
"""),
    ("human", """Function:
{function_source}

Arguments (JSON):
{arguments}

Observed exception:
{error_description}

Return the corrected function only."""),
])
