"""向量库：ChromaDB 本地持久化（LangChain 封装）"""
from functools import lru_cache

from langchain_chroma import Chroma

from ..config import settings
from .embeddings import get_embeddings

COLLECTION_NAME = "kb_docs"


@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:
    """获取 Chroma 向量库单例，数据持久化到 backend/data/chroma/"""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(settings.chroma_dir),
    )
