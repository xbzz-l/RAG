"""认证接口：注册 / 登录 / 当前用户信息"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..auth import create_access_token, get_current_user, hash_password, verify_password
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="用户名")
    password: str = Field(min_length=6, max_length=72, description="密码")


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """注册：用户名唯一校验 + bcrypt 哈希存储；所有人注册为普通用户"""
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "用户名已存在")
    if len(req.password.encode("utf-8")) > 72:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "密码过长（最多72字节）")
    user = User(username=req.username, password_hash=hash_password(req.password), role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "注册成功", "username": user.username}


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """登录：校验账号密码，返回 JWT + 角色"""
    user = db.query(User).filter(User.username == req.username).first()
    if user is None or not verify_password(req.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "账号或密码错误")
    return {
        "access_token": create_access_token(user),
        "username": user.username,
        "role": user.role,
    }


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    """返回当前登录用户信息（前端刷新页面时校验 token 是否仍有效）"""
    return {"username": user.username, "role": user.role}
