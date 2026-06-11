from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.qa import router as qa_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API-only enterprise knowledge base MVP powered by LangChain and ChromaDB.",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(documents_router, prefix="/documents", tags=["documents"])
app.include_router(qa_router, prefix="/qa", tags=["qa"])
