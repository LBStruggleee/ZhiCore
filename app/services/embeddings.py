from app.core.config import settings


def get_embeddings():
    provider = settings.embedding_provider.lower()

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        kwargs: dict[str, str] = {"model": settings.openai_embedding_model}
        if settings.openai_api_key:
            kwargs["api_key"] = settings.openai_api_key
        if settings.openai_base_url:
            kwargs["base_url"] = settings.openai_base_url
        return OpenAIEmbeddings(**kwargs)

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=settings.huggingface_embedding_model)

    raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")
