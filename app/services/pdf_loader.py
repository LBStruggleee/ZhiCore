from pathlib import Path


def load_pdf_pages(path: Path, document_id: str, filename: str) -> list:
    import fitz
    from langchain_core.documents import Document

    pages: list = []
    with fitz.open(path) as pdf:
        for index, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()
            if not text:
                continue
            pages.append(
                Document(
                    page_content=text,
                    metadata={
                        "document_id": document_id,
                        "source": filename,
                        "page": index,
                        "path": str(path),
                    },
                )
            )
    return pages
