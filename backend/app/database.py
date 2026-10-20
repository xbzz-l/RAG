"""SQLAlchemy 数据库连接：SQLite 本地文件"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

SQLITE_URL = f"sqlite:///{settings.data_dir / 'app.db'}"

engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},  # FastAPI 多线程访问 SQLite 需要
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    """FastAPI 依赖：请求级数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
