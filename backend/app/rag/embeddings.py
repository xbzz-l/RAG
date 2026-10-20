"""Embedding 模型：本地 BGE 中文向量模型

网络策略：模型已在本地缓存时，直接用本地目录路径加载（彻底绕开 HuggingFace
网络检查，杜绝超时卡顿）；未缓存时按 hub 模型名走国内镜像 hf-mirror 下载。
注意：环境变量必须在导入 huggingface 相关库【之前】设置才会生效。
"""
import os
from functools import lru_cache
from pathlib import Path

from ..config import settings

# BGE 官方推荐：查询侧加中文指令前缀，可显著提升检索效果（文档侧不加）
BGE_QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："


def _find_local_model_dir() -> str | None:
    """在 HF 缓存中定位已下载的模型目录（兼容标准布局与无符号链接的降级布局）"""
    hub_dirs = []
    cache_base = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface"))
    hub_dirs.append(cache_base / "hub")  # 标准位置：$HF_HOME/hub
    hub_dirs.append(cache_base)          # 兜底：HF_HOME 直接指向 hub
    model_slug = f"models--{settings.embedding_model.replace('/', '--')}"
    for hub in hub_dirs:
        model_dir = hub / model_slug
        if model_dir.exists():
            for f in model_dir.rglob("model.safetensors"):
                return str(f.parent)
    return None


def _setup_hf_env() -> None:
    """必须在导入 huggingface 库之前调用"""
    if _find_local_model_dir():
        # 已有缓存：完全离线加载，杜绝网络超时（答辩演示也稳定）
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
    else:
        # 未缓存：走国内镜像下载（huggingface_hub 1.x 用 HF_HUB_URL，兼容旧版 HF_ENDPOINT）
        os.environ["HF_HUB_URL"] = settings.hf_endpoint
        os.environ["HF_ENDPOINT"] = settings.hf_endpoint


_setup_hf_env()

from langchain_huggingface import HuggingFaceEmbeddings  # noqa: E402


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """加载 BGE 模型（CPU 推理，进程内单例），向量已归一化"""
    # 缓存存在则用本地目录加载，否则按 hub 名走镜像下载
    model_name = _find_local_model_dir() or settings.embedding_model
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
