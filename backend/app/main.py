"""FastAPI 应用入口：路由注册、CORS、启动初始化（建表 + 管理员账号）"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import hash_password
from .config import settings
from .database import Base, SessionLocal, engine
from .models import User
from .routers import auth as auth_router
from .routers import chat as chat_router
from .routers import kb as kb_router


def init_admin() -> None:
    """启动时确保管理员账号存在（admin/admin123，固定账号）"""
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.username == settings.admin_username).first()
        if exists is None:
            db.add(
                User(
                    username=settings.admin_username,
                    password_hash=hash_password(settings.admin_password),
                    role="admin",
                )
            )
            db.commit()
            print(f"[启动] 管理员账号已初始化: {settings.admin_username}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    init_admin()
    yield


app = FastAPI(title="IT技术栈知识库", lifespan=lifespan)

# 前端 Vite 开发服务器跨域（localhost 任意端口，避免端口漂移）
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(kb_router.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
