"""文档解析与分块：支持 md / txt / pdf"""
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..config import settings


def parse_file(path: Path) -> str:
    """按扩展名解析文件为纯文本"""
    ext = path.suffix.lower()
    if ext == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    # md / txt 及其余文本类文件直接按 UTF-8 读取
    return path.read_text(encoding="utf-8", errors="ignore")


def get_splitter() -> RecursiveCharacterTextSplitter:
    """中文友好分块：优先按段落/换行/句号切分，块间带重叠避免语义断裂"""
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", "。", "；", ". ", " ", ""],
        keep_separator=True,
    )
