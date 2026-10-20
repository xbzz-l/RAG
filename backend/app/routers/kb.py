"""知识库管理接口：上传 / 列表 / 原文 / 编辑 / 删除（仅管理员，require_admin 兜底）"""
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..config import settings
from ..database import get_db
from ..models import KbDocument, User
from ..rag import loader
from ..rag.ingest import index_document
from ..rag.vectorstore import get_vectorstore

router = APIRouter(
    prefix="/api/kb",
    tags=["kb"],
    dependencies=[Depends(require_admin)],  # 整个路由仅管理员可用
)

ALLOWED_EXT = {".md", ".txt", ".pdf"}


class KbUpdateRequest(BaseModel):
    title: str
    category: str
    content: str


def _get_doc(doc_id: int, db: Session) -> KbDocument:
    doc = db.get(KbDocument, doc_id)
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "文档不存在")
    return doc


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("技术栈"),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """上传文档（md/txt/pdf）并完成分块向量化入库"""
    filename = file.filename or "unnamed"
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"仅支持 {'/'.join(sorted(ALLOWED_EXT))} 格式")

    data = await file.read()
    if not data.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "文件内容为空")

    # 文件落盘（原文留档，供后续编辑回显）
    save_path = settings.upload_dir / f"{datetime.now():%Y%m%d%H%M%S}_{filename}"
    save_path.write_bytes(data)

    content = loader.parse_file(save_path)
    if not content.strip():
        save_path.unlink(missing_ok=True)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "未能从文件中解析出文本内容")

    # 文件名约定「技术栈-xxx.md / 学习路线-xxx.md」自动识别分类并去掉前缀
    stem = Path(filename).stem
    for prefix, cat in (("学习路线-", "学习路线"), ("技术栈-", "技术栈")):
        if stem.startswith(prefix):
            category = cat
            stem = stem[len(prefix):]
            break

    doc = KbDocument(title=stem, category=category, file_path=str(save_path))
    db.add(doc)
    db.commit()
    db.refresh(doc)

    n = index_document(doc.id, doc.title, doc.category, content)
    doc.chunk_count = n
    db.commit()
    return {"message": "上传成功", "id": doc.id, "title": doc.title, "chunk_count": n}


@router.get("/documents")
def list_documents(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """文档列表（按更新时间倒序）"""
    rows = db.query(KbDocument).order_by(KbDocument.updated_at.desc()).all()
    return [
        {
            "id": d.id,
            "title": d.title,
            "category": d.category,
            "chunk_count": d.chunk_count,
            "created_at": d.created_at.isoformat(),
            "updated_at": d.updated_at.isoformat(),
        }
        for d in rows
    ]


@router.get("/documents/{doc_id}/content")
def get_document_content(
    doc_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """取文档原文（编辑弹窗回显用）"""
    doc = _get_doc(doc_id, db)
    content = ""
    if doc.file_path and Path(doc.file_path).exists():
        content = loader.parse_file(Path(doc.file_path))
    return {"id": doc.id, "title": doc.title, "category": doc.category, "content": content}


@router.put("/documents/{doc_id}")
def update_document(
    doc_id: int,
    req: KbUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """编辑文档：更新原文文件 + 重新分块向量化（自动清理旧向量）"""
    doc = _get_doc(doc_id, db)
    if not req.title.strip() or not req.content.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "标题和内容不能为空")

    # 原文落盘：PDF 无法原地改，切换为 md 文件保存
    path = Path(doc.file_path) if doc.file_path else None
    if path is None or not path.exists() or path.suffix.lower() == ".pdf":
        path = settings.upload_dir / f"doc_{doc.id}.md"
        doc.file_path = str(path)
    path.write_text(req.content, encoding="utf-8")

    doc.title = req.title.strip()
    doc.category = req.category
    doc.chunk_count = index_document(doc.id, doc.title, doc.category, req.content)
    db.commit()
    return {"message": "更新成功", "chunk_count": doc.chunk_count}


@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """删除文档：清理向量 + 删除原文文件 + 删除记录"""
    doc = _get_doc(doc_id, db)
    get_vectorstore().delete(where={"doc_id": doc.id})
    if doc.file_path and Path(doc.file_path).exists():
        Path(doc.file_path).unlink(missing_ok=True)
    db.delete(doc)
    db.commit()
    return {"message": "删除成功"}
