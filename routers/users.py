from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.cache_config import get_cache
from config.db_config import get_db
from crud import users
from models.users import Users
from schemas.users import (
    ChangePasswordRequestUser,
    FindPasswordRequestUser,
    LoginRequestUser,
    RegisterRequestUser,
    UpdateUsersRequest,
    UserAuthResponse,
    UserInfoResponse,
)
from utils.auth import get_current_user
from utils.response import success_response


ekko = APIRouter(prefix="/api/users", tags=["users"])


@ekko.post("/register")
async def register_user(user: RegisterRequestUser, db: AsyncSession = Depends(get_db)):
    cached_verify_code = await get_cache(user.email)
    if not cached_verify_code:
        raise HTTPException(status_code=404, detail="验证码已失效")
    if user.verify_code != cached_verify_code:
        raise HTTPException(status_code=403, detail="验证码错误")

    existing_user = await users.select_user_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    created_user = await users.create_user(db, user)
    if not created_user:
        raise HTTPException(status_code=400, detail="未能生成唯一用户ID，请重新创建")

    token = await users.create_token(db, created_user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(created_user))
    return success_response(message="注册成功", data=response_data)


@ekko.post("/login")
async def login_user(user: LoginRequestUser, db: AsyncSession = Depends(get_db)):
    current_user = await users.authenticate_user(db, user.email, user.pwd)
    if not current_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = await users.create_token(db, current_user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(current_user))
    return success_response(message="登录成功", data=response_data)


@ekko.get("/info")
async def info(user: Users = Depends(get_current_user)):
    return success_response(
        message="User info obtained successfully",
        data=UserInfoResponse.model_validate(user),
    )


@ekko.put("/update")
async def update_user_info(
    update_user: UpdateUsersRequest,
    user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updated_user = await users.update_user(db, user.id, update_user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(
        message="User info updated successfully",
        data=UserInfoResponse.model_validate(updated_user),
    )


@ekko.put("/password")
async def update_password(
    password_data: ChangePasswordRequestUser,
    user: Users = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cached_verify_code = await get_cache(user.email)
    if not cached_verify_code:
        raise HTTPException(status_code=404, detail="验证码已失效")
    if password_data.verify_code != cached_verify_code:
        raise HTTPException(status_code=403, detail="验证码错误")

    result = await users.change_password(db, user, password_data.new_password)
    if not result:
        raise HTTPException(status_code=500, detail="修改密码失败，请稍后再试")
    return success_response(message="修改密码成功")


@ekko.put("/find_password")
async def find_password(
    email_password: FindPasswordRequestUser,
    db: AsyncSession = Depends(get_db),
):
    email = email_password.email.email
    user = await users.select_user_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="未找到此邮箱对应用户，请检查邮箱是否正确")

    cached_verify_code = await get_cache(email)
    if not cached_verify_code:
        raise HTTPException(status_code=404, detail="验证码已失效")
    if email_password.verify_code != cached_verify_code:
        raise HTTPException(status_code=403, detail="验证码错误")

    updated_user = await users.find_password_email(db, user, password=email_password.new_password)
    if updated_user:
        return success_response(message="找回密码成功")
    raise HTTPException(status_code=500, detail="密码找回异常，请重试")
