from app.core.config import settings
from app.schemas.qa import QARequest, QAResponse, SourceReference
from app.services.vector_store import get_vector_store


SYSTEM_PROMPT = """你是企业知识库助手。
请只基于提供的上下文回答问题。
如果上下文中没有答案，请回答“根据现有知识库资料，无法确认该问题的答案。”
回答必须准确、简洁，并在语义上对应引用来源。"""


class QAService:
    def answer(self, request: QARequest) -> QAResponse:
        top_k = request.top_k or settings.default_top_k
        vector_store = get_vector_store()
        results = vector_store.similarity_search_with_relevance_scores(request.question, k=top_k)

        documents = [document for document, _score in results]
        sources = [
            self._source_from_document(document, score)
            for document, score in results
        ]

        if not documents:
            return QAResponse(answer="根据现有知识库资料，无法确认该问题的答案。", sources=[])

        answer = self._generate_answer(request.question, documents)
        return QAResponse(answer=answer, sources=sources)

    def _generate_answer(self, question: str, documents: list) -> str:
        try:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_openai import ChatOpenAI

            kwargs: dict[str, str | float] = {
                "model": settings.openai_chat_model,
                "temperature": 0,
            }
            if settings.openai_api_key:
                kwargs["api_key"] = settings.openai_api_key
            if settings.openai_base_url:
                kwargs["base_url"] = settings.openai_base_url

            llm = ChatOpenAI(**kwargs)
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", SYSTEM_PROMPT),
                    ("human", "问题：{question}\n\n上下文：\n{context}"),
                ]
            )
            chain = prompt | llm
            response = chain.invoke({"question": question, "context": self._format_context(documents)})
            return str(response.content).strip()
        except Exception:
            return self._fallback_answer(documents)

    def _format_context(self, documents: list) -> str:
        blocks = []
        for document in documents:
            metadata = document.metadata
            blocks.append(
                f"[{metadata.get('source')} 第{metadata.get('page')}页 {metadata.get('chunk_id')}]\n"
                f"{document.page_content}"
            )
        return "\n\n".join(blocks)

    def _source_from_document(self, document, score: float | None) -> SourceReference:
        metadata = document.metadata
        return SourceReference(
            document=str(metadata.get("source", "")),
            page=metadata.get("page"),
            chunk_id=str(metadata.get("chunk_id", "")),
            excerpt=document.page_content[:500],
            score=score,
        )

    def _fallback_answer(self, documents: list) -> str:
        excerpts = []
        for document in documents[:2]:
            source = document.metadata.get("source", "未知文档")
            page = document.metadata.get("page", "未知页码")
            excerpts.append(f"{source} 第{page}页：{document.page_content[:300]}")
        return "当前未能调用大模型生成回答。以下是知识库中最相关的片段：\n" + "\n\n".join(excerpts)


qa_service = QAService()
