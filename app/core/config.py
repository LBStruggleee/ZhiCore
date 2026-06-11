from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Enterprise Knowledge Base Agent"
    data_dir: Path = Field(default=Path("data"))
    uploads_dir: Path = Field(default=Path("data/uploads"))
    chroma_dir: Path = Field(default=Path("data/chroma"))
    chroma_collection: str = "enterprise_kb"

    embedding_provider: str = Field(default="openai", description="openai or huggingface")
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o-mini"

    huggingface_embedding_model: str = "BAAI/bge-small-zh-v1.5"

    chunk_size: int = 1000
    chunk_overlap: int = 150
    default_top_k: int = 5


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    return settings


settings = get_settings()
