"""Environment-based application settings."""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    max_fix_attempts: int = int(os.getenv("MAX_FIX_ATTEMPTS", "3"))
    gradio_server_name: str = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    gradio_server_port: int = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
