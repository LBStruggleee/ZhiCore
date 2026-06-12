from app.core.config import settings


def get_embeddings():
    provider = settings.embedding_provider.lower()

    if provider == "dashscope":
        from langchain_community.embeddings import DashScopeEmbeddings

        return DashScopeEmbeddings(
            model=settings.qwen_embedding_model,
            dashscope_api_key=settings.dashscope_api_key,
        )

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=settings.huggingface_embedding_model)

    raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")
