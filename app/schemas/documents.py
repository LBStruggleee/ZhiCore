from datetime import datetime
from pathlib import Path

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    path: Path
    size_bytes: int
    uploaded_at: datetime
    indexed: bool = False


class DocumentUploadResponse(DocumentInfo):
    pass


class DocumentIndexResponse(BaseModel):
    indexed_documents: int
    indexed_chunks: int
    skipped_documents: int
