"""全局配置：从 backend/.env 读取环境变量，含默认值"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ 目录（config.py 位于 backend/app/ 下）
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # ---------- Ollama 本地大模型 ----------
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:3b"  # 低配置友好；可换 qwen2.5:1.5b / 7b

    # ---------- Embedding 模型 ----------
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    hf_endpoint: str = "https://hf-mirror.com"  # 国内下载镜像

    # ---------- JWT ----------
    jwt_secret: str = "rag-knowledge-base-secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24

    # ---------- 存储路径 ----------
    data_dir: Path = BASE_DIR / "data"           # SQLite/Chroma/上传文件根目录
    upload_dir: Path = BASE_DIR / "data" / "uploads"
    chroma_dir: Path = BASE_DIR / "data" / "chroma"
    seed_docs_dir: Path = BASE_DIR / "docs" / "kb_seed"

    # ---------- RAG 检索参数 ----------
    retrieve_k: int = 4                 # 检索top-k文档块
    retrieve_threshold: float = 0.25    # 余弦相似度阈值（低于视为未命中）
    chunk_size: int = 500               # 分块大小（字符）
    chunk_overlap: int = 50             # 分块重叠

    # ---------- 管理员账号（固定） ----------
    admin_username: str = "admin"
    admin_password: str = "admin123"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

# 确保运行时目录存在
for _dir in (settings.data_dir, settings.upload_dir, settings.chroma_dir):
    _dir.mkdir(parents=True, exist_ok=True)
