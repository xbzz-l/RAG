"""种子知识库入库脚本：python -m app.seed_kb

读取 docs/kb_seed/*.md，清空旧知识库后逐篇分块向量化写入 Chroma 与 kb_documents 表。
文件名约定：`技术栈-xxx.md` 或 `学习路线-xxx.md`（自动识别分类与标题）。
"""
import sys
from pathlib import Path

# 支持 python -m app.seed_kb 直接运行
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import chromadb  # noqa: E402

from app.config import settings  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import KbDocument  # noqa: E402
from app.rag.ingest import index_document  # noqa: E402
from app.rag.vectorstore import COLLECTION_NAME, get_vectorstore  # noqa: E402


def reset_collection() -> None:
    """删除旧集合（种子重跑时保证幂等），随后 get_vectorstore 会重建新集合"""
    client = chromadb.PersistentClient(path=str(settings.chroma_dir))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # 集合不存在则忽略


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    reset_collection()

    db = SessionLocal()
    try:
        db.query(KbDocument).delete()
        db.commit()

        md_files = sorted(settings.seed_docs_dir.glob("*.md"))
        if not md_files:
            print(f"[提示] {settings.seed_docs_dir} 下没有找到种子文档")
            return

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            name = md_path.stem
            if name.startswith("学习路线-"):
                category, title = "学习路线", name[len("学习路线-"):]
            else:
                category = "技术栈"
                title = name[len("技术栈-"):] if name.startswith("技术栈-") else name

            doc = KbDocument(title=title, category=category, file_path=str(md_path), chunk_count=0)
            db.add(doc)
            db.commit()
            db.refresh(doc)

            n = index_document(doc.id, doc.title, doc.category, content)
            doc.chunk_count = n
            db.commit()
            print(f"[{category}] {title}: {n} 块")
    finally:
        db.close()

    print("种子知识库入库完成")


if __name__ == "__main__":
    seed()
