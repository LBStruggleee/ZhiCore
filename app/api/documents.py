from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.documents import DocumentInfo, DocumentIndexResponse, DocumentUploadResponse
from app.services.document_service import document_service

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    document = await document_service.save_upload(file)
    return DocumentUploadResponse(**document.model_dump())


@router.post("/index", response_model=DocumentIndexResponse)
def index_documents() -> DocumentIndexResponse:
    return document_service.index_all_documents()


@router.get("", response_model=list[DocumentInfo])
def list_documents() -> list[DocumentInfo]:
    return document_service.list_documents()


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str) -> None:
    deleted = document_service.delete_document(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found.")
