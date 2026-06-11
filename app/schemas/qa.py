from pydantic import BaseModel, Field


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)


class SourceReference(BaseModel):
    document: str
    page: int | None = None
    chunk_id: str
    excerpt: str
    score: float | None = None


class QAResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
