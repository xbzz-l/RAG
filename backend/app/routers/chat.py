"""对话接口：会话CRUD（按用户隔离） + RAG 流式对话（SSE）"""
import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import SessionLocal, get_db
from ..models import Conversation, Message, User
from ..rag import chain

router = APIRouter(prefix="/api", tags=["chat"])


class ChatStreamRequest(BaseModel):
    conversation_id: int | None = Field(default=None, description="会话ID，为空则新建会话")
    message: str = Field(min_length=1, max_length=2000)


def _sse(data: dict) -> str:
    """序列化一条 SSE 事件"""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def _save_message(conv_id: int, answer: str, sources: list) -> None:
    """回答落库 + 会话时间刷新（独立会话，不依赖请求依赖生命周期）"""
    if not answer:
        return
    s = SessionLocal()
    try:
        c = s.get(Conversation, conv_id)
        if c is not None:
            c.updated_at = datetime.now()
        s.add(
            Message(
                conversation_id=conv_id,
                role="assistant",
                content=answer,
                sources=json.dumps(sources, ensure_ascii=False),
            )
        )
        s.commit()
    finally:
        s.close()


# ---------- 会话管理 ----------
def _own_conversation(conv_id: int, user: User, db: Session) -> Conversation:
    """校验会话归属：不存在或非本人一律404（数据隔离）"""
    conv = db.get(Conversation, conv_id)
    if conv is None or conv.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "会话不存在")
    return conv


@router.get("/conversations")
def list_conversations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """当前用户的会话列表（按更新时间倒序）"""
    rows = (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    return [
        {"id": c.id, "title": c.title, "updated_at": c.updated_at.isoformat()} for c in rows
    ]


@router.get("/conversations/{conv_id}/messages")
def get_messages(
    conv_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取指定会话的全部历史消息（含来源引用）"""
    _own_conversation(conv_id, user, db)
    rows = (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .order_by(Message.id.asc())
        .all()
    )
    return [
        {
            "role": m.role,
            "content": m.content,
            "sources": json.loads(m.sources) if m.sources else [],
        }
        for m in rows
    ]


@router.delete("/conversations/{conv_id}")
def delete_conversation(
    conv_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除会话及其全部消息"""
    conv = _own_conversation(conv_id, user, db)
    db.query(Message).filter(Message.conversation_id == conv_id).delete()
    db.delete(conv)
    db.commit()
    return {"message": "会话已删除"}


# ---------- RAG 流式对话 ----------
@router.post("/chat/stream")
async def chat_stream(
    req: ChatStreamRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """RAG 流式对话。SSE 事件顺序：sources -> token* -> done（附会话ID）"""
    # 1) 向量检索知识库
    docs, sources = chain.retrieve(req.message)

    # 2) 会话归属校验 / 新建（首问）
    if req.conversation_id is None:
        conv = Conversation(user_id=user.id, title=req.message[:20])
        db.add(conv)
        db.commit()
        db.refresh(conv)
    else:
        conv = _own_conversation(req.conversation_id, user, db)

    # 3) 用户消息落库（回答在流式结束后落库）
    db.add(Message(conversation_id=conv.id, role="user", content=req.message))
    db.commit()

    async def event_stream():
        # 事件顺序：token*（流式回答）-> done（会话ID + 来源，回答结束后统一展示来源）
        answer = ""
        completed = False
        try:
            if not docs:
                # 兜底：大模型通用知识回答，先发显著标注，与有来源的知识库回答区分
                answer = chain.FALLBACK_LABEL
                yield _sse({"type": "token", "content": answer})
                async for token in chain.stream_general_answer(req.message):
                    answer += token
                    yield _sse({"type": "token", "content": token})
            else:
                async for token in chain.stream_answer(req.message, docs):
                    answer += token
                    yield _sse({"type": "token", "content": token})
            # 来源随 done 事件最后下发（前端回答结束后才展示来源）
            yield _sse({"type": "done", "conversation_id": conv.id, "sources": sources})
            completed = True
        finally:
            # 无论正常完成还是用户中途停止（客户端断开），都保存已生成内容
            if not completed and answer:
                answer += "\n\n_（用户已停止生成）_"
            _save_message(conv.id, answer, sources)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
