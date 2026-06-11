from fastapi import APIRouter

from app.schemas.qa import QARequest, QAResponse
from app.services.qa_service import qa_service

router = APIRouter()


@router.post("/query", response_model=QAResponse)
def query_knowledge_base(request: QARequest) -> QAResponse:
    return qa_service.answer(request)
