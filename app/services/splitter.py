from app.core.config import settings


def split_documents(documents: list) -> list:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            "\u3002",
            "\uff01",
            "\uff1f",
            "\uff1b",
            ";",
            ".",
            "!",
            "?",
            " ",
            "",
        ],
    )
    chunks = splitter.split_documents(documents)
    for index, chunk in enumerate(chunks):
        document_id = chunk.metadata["document_id"]
        page = chunk.metadata.get("page", "unknown")
        chunk.metadata["chunk_index"] = index
        chunk.metadata["chunk_id"] = f"{document_id}_page_{page}_chunk_{index}"
    return chunks
