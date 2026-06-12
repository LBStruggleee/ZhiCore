# Enterprise Knowledge Base Agent

基于 LangChain、ChromaDB、FastAPI 和通义千问的企业知识库问答 MVP，支持 PDF 上传、解析、切分、向量索引、语义检索、RAG 问答和引用溯源。

## 功能

- `POST /documents/upload` 上传 PDF
- `POST /documents/index` 解析 PDF 并写入 ChromaDB
- `GET /documents` 查看文档
- `DELETE /documents/{document_id}` 删除文档和向量
- `POST /qa/query` 基于知识库问答并返回引用来源
- `GET /health` 健康检查

## 本地启动

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

打开 API 文档：

```text
http://localhost:8000/docs
```

## Docker 启动

```bash
copy .env.example .env
docker compose up -d --build
```

服务地址：

```text
http://localhost:8000
```

## 千问配置

默认使用阿里云百炼 DashScope 的通义千问模型：

```env
EMBEDDING_PROVIDER=dashscope
DASHSCOPE_API_KEY=your_dashscope_api_key
QWEN_EMBEDDING_MODEL=text-embedding-v4
QWEN_CHAT_MODEL=qwen-plus
```

也可以使用本地 HuggingFace embedding 做向量化：

```env
EMBEDDING_PROVIDER=huggingface
HUGGINGFACE_EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
```

注意：问答生成默认调用通义千问 `QWEN_CHAT_MODEL`。如果未配置 `DASHSCOPE_API_KEY` 或模型调用失败，接口会返回最相关的知识库片段作为降级结果，引用来源仍会保留。

## API 示例

上传 PDF：

```bash
curl -X POST "http://localhost:8000/documents/upload" ^
  -F "file=@employee_handbook.pdf"
```

建立索引：

```bash
curl -X POST "http://localhost:8000/documents/index"
```

提问：

```bash
curl -X POST "http://localhost:8000/qa/query" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"公司的年假政策是什么？\",\"top_k\":5}"
```

响应示例：

```json
{
  "answer": "根据员工手册，年假按工龄计算。",
  "sources": [
    {
      "document": "employee_handbook.pdf",
      "page": 14,
      "chunk_id": "abc_page_14_chunk_3",
      "excerpt": "员工年假按照工龄...",
      "score": 0.87
    }
  ]
}
```

## 数据持久化

本地数据默认保存在：

```text
data/uploads
data/chroma
data/documents.json
```

Docker Compose 会挂载这些目录，容器重建后数据仍保留。

## 测试

```bash
pytest
```
