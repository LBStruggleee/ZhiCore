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

    embedding_provider: str = Field(default="dashscope", description="dashscope or huggingface")
    dashscope_api_key: str | None = None
    qwen_chat_model: str = "qwen-plus"
    qwen_embedding_model: str = "text-embedding-v4"

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
