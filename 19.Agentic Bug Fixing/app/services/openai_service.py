"""OpenAI chat model factory."""
from langchain_openai import ChatOpenAI
from app.config.settings import settings

def create_chat_model() -> ChatOpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Configure it in .env or the environment.")
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
        timeout=60,
        max_retries=2,
    )
