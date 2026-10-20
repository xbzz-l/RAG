"""数据库表模型：用户 / 会话 / 消息 / 知识库文档"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .database import Base


class User(Base):
    """用户表：普通用户 role='user'，管理员 role='admin'"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(100), nullable=False)
    role = Column(String(10), nullable=False, default="user")
    created_at = Column(DateTime, default=datetime.now)


class Conversation(Base):
    """会话表：每个用户的数据独立（按 user_id 隔离）"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(100), nullable=False, default="新对话")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Message(Base):
    """消息表：role 为 user / assistant；sources 存JSON字符串（命中知识库文档）"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    sources = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class KbDocument(Base):
    """知识库文档表：记录文档元信息，正文向量存于 ChromaDB"""
    __tablename__ = "kb_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(20), nullable=False, default="技术栈")  # 技术栈 / 学习路线
    file_path = Column(String(500), nullable=True)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
