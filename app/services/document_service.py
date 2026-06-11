import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.schemas.documents import DocumentInfo, DocumentIndexResponse
from app.services.pdf_loader import load_pdf_pages
from app.services.splitter import split_documents
from app.services.vector_store import add_documents, delete_document_vectors


class DocumentService:
    def __init__(self) -> None:
        self.manifest_path = settings.data_dir / "documents.json"
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.manifest_path.exists():
            self._write_manifest([])

    async def save_upload(self, file: UploadFile) -> DocumentInfo:
        document_id = uuid4().hex
        safe_name = Path(file.filename or "document.pdf").name
        stored_name = f"{document_id}_{safe_name}"
        target_path = settings.uploads_dir / stored_name

        with target_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                output.write(chunk)

        document = DocumentInfo(
            document_id=document_id,
            filename=safe_name,
            path=target_path,
            size_bytes=target_path.stat().st_size,
            uploaded_at=datetime.now(timezone.utc),
            indexed=False,
        )
        documents = self._read_manifest()
        documents.append(document)
        self._write_manifest(documents)
        return document

    def list_documents(self) -> list[DocumentInfo]:
        return self._read_manifest()

    def index_all_documents(self) -> DocumentIndexResponse:
        documents = self._read_manifest()
        indexed_documents = 0
        indexed_chunks = 0
        skipped_documents = 0

        for document in documents:
            if document.indexed:
                skipped_documents += 1
                continue
            pages = load_pdf_pages(document.path, document.document_id, document.filename)
            chunks = split_documents(pages)
            add_documents(chunks)
            document.indexed = True
            indexed_documents += 1
            indexed_chunks += len(chunks)

        self._write_manifest(documents)
        return DocumentIndexResponse(
            indexed_documents=indexed_documents,
            indexed_chunks=indexed_chunks,
            skipped_documents=skipped_documents,
        )

    def delete_document(self, document_id: str) -> bool:
        documents = self._read_manifest()
        remaining = [document for document in documents if document.document_id != document_id]
        if len(remaining) == len(documents):
            return False

        deleted = next(document for document in documents if document.document_id == document_id)
        if deleted.path.exists():
            deleted.path.unlink()
        if deleted.indexed:
            delete_document_vectors(document_id)
        self._write_manifest(remaining)
        return True

    def _read_manifest(self) -> list[DocumentInfo]:
        if not self.manifest_path.exists():
            return []
        raw = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        return [DocumentInfo(**item) for item in raw]

    def _write_manifest(self, documents: list[DocumentInfo]) -> None:
        tmp_path = self.manifest_path.with_suffix(".json.tmp")
        tmp_path.write_text(
            json.dumps([document.model_dump(mode="json") for document in documents], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        shutil.move(str(tmp_path), str(self.manifest_path))


document_service = DocumentService()
