from app.core.config import settings
from app.services.embeddings import get_embeddings


def get_vector_store():
    from langchain_chroma import Chroma

    return Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=get_embeddings(),
        persist_directory=str(settings.chroma_dir),
    )


def add_documents(chunks: list) -> None:
    if not chunks:
        return
    vector_store = get_vector_store()
    ids = [chunk.metadata["chunk_id"] for chunk in chunks]
    vector_store.add_documents(chunks, ids=ids)


def delete_document_vectors(document_id: str) -> None:
    vector_store = get_vector_store()
    collection = vector_store._collection
    collection.delete(where={"document_id": document_id})
