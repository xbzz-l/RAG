"""RAG 检索链：查询向量化 -> Chroma 检索 -> 组装带来源上下文 -> Ollama 流式生成"""
from typing import AsyncGenerator

from langchain_ollama import ChatOllama

from ..config import settings
from .embeddings import BGE_QUERY_INSTRUCTION
from .vectorstore import get_vectorstore

SYSTEM_PROMPT = (
    "你是「IT技术栈知识库」助手，只依据下方知识库上下文回答问题。\n"
    "要求：全是干货、无废话，结构清晰（可用小标题/列表）；"
    "技术栈类问题按「是什么/核心知识/作用与场景/基于什么语言/优缺点」组织；"
    "学习路线类问题按阶段展开、逐技术栈解释；不编造知识库中没有的内容。"
)

# 兜底模式：知识库未命中时，用大模型通用知识回答
GENERAL_SYSTEM_PROMPT = (
    "你是「IT技术栈知识库」助手的兜底模式。用户的问题未在知识库中检索到相关内容，"
    "请基于你的通用知识直接回答。\n"
    "要求：全是干货、无废话，结构清晰（可用小标题/列表）；"
    "技术栈类问题按「是什么/核心知识/作用与场景/基于什么语言/优缺点」组织；"
    "学习路线类问题按阶段展开、逐技术栈解释；不确定的内容直接说明，不要编造。"
)

# 兜底回答的显著标注（markdown 引用块样式），与有来源的知识库回答区分
FALLBACK_LABEL = "> ⚠️ 知识库未收录此问题，以下回答来自本地模型通用知识，仅供参考：\n\n"


def _build_context(docs) -> str:
    """把命中的文档块组装成带来源标题的上下文（不编号，避免模型把编号复述进回答）"""
    parts = []
    for doc in docs:
        title = doc.metadata.get("title", "未知文档")
        category = doc.metadata.get("category", "")
        parts.append(f"（来源：《{title}》｜{category}）\n{doc.page_content}")
    return "\n\n".join(parts)


def _dedupe_sources(docs) -> list[dict]:
    """按 doc_id 去重提取来源列表，供前端展示引用"""
    seen: set = set()
    sources: list[dict] = []
    for doc in docs:
        key = doc.metadata.get("doc_id")
        if key is not None and key not in seen:
            seen.add(key)
            sources.append(
                {
                    "title": doc.metadata.get("title", "未知文档"),
                    "category": doc.metadata.get("category", ""),
                }
            )
    return sources


def retrieve(query: str) -> tuple[list, list[dict]]:
    """向量检索 top-k，低于相似度阈值视为未命中；返回(文档块列表, 去重来源列表)"""
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_relevance_scores(
        BGE_QUERY_INSTRUCTION + query,
        k=settings.retrieve_k,
    )
    # 归一化向量下，relevance score 即余弦相似度，按阈值过滤
    docs = [doc for doc, score in results if score >= settings.retrieve_threshold]
    return docs, _dedupe_sources(docs)


def _get_llm() -> ChatOllama:
    """创建 Ollama 本地模型实例"""
    return ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        temperature=0.2,
    )


async def stream_answer(query: str, docs) -> AsyncGenerator[str, None]:
    """知识库命中时：检索上下文 + Ollama 流式生成回答，逐 token 产出"""
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"【知识库上下文】\n{_build_context(docs)}\n\n"
        f"【用户问题】{query}\n"
        f"【回答】"
    )
    llm = _get_llm()
    async for chunk in llm.astream(prompt):
        text = chunk.content if hasattr(chunk, "content") else str(chunk)
        if text:
            yield text


async def stream_general_answer(query: str) -> AsyncGenerator[str, None]:
    """知识库未命中时的兜底：大模型通用知识回答，逐 token 产出"""
    prompt = f"{GENERAL_SYSTEM_PROMPT}\n\n【用户问题】{query}\n【回答】"
    llm = _get_llm()
    async for chunk in llm.astream(prompt):
        text = chunk.content if hasattr(chunk, "content") else str(chunk)
        if text:
            yield text
