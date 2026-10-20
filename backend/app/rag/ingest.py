"""知识入库：文档内容 -> 分块 -> 向量化 -> 写入 Chroma

doc_id 是核心索引：同一 doc_id 重复入库会先清理旧向量（覆盖式更新）。
"""
from . import loader
from .vectorstore import get_vectorstore


def index_document(doc_id: int, title: str, category: str, content: str) -> int:
    """对文档内容分块并向量化入库，返回块数；更新场景自动清掉旧向量"""
    vectorstore = get_vectorstore()
    vectorstore.delete(where={"doc_id": doc_id})  # 清理旧向量（不存在时为空操作）
    chunks = loader.get_splitter().split_text(content)
    if not chunks:
        return 0
    vectorstore.add_texts(
        texts=chunks,
        metadatas=[{"doc_id": doc_id, "title": title, "category": category} for _ in chunks],
    )
    return len(chunks)
