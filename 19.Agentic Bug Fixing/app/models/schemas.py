"""Shared typed models and validation helpers."""
from pydantic import BaseModel, Field
from typing import Any

class RunRequest(BaseModel):
    code: str = Field(min_length=1)
    arguments: list[Any] = Field(default_factory=list)

class RunResponse(BaseModel):
    status: str
    result: str = ""
    original_code: str
    fixed_code: str = ""
    diff_html: str = ""
    attempts: int = 0
    error: str = ""
    execution_log: list[str] = Field(default_factory=list)
