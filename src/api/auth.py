from exceptions import auth
from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.schemas.user import UserCreate, UserLogin
from core.database.schemas.auth import (
    VerifyEmail,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    )
from core.database import db_helper
from core.services.user import UserService
from core.dependency.services import get_user_service

from utilities.jwt_token import create_jwt_token

from core.config import settings

router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)

@router.post("/register")
async def register(
    user_data: UserCreate,
    user_service: Annotated[
        UserService,
        Depends(get_user_service)
    ],
):
    """
    Registrate new user and send verification token to email.
    """
    
    user = await user_service.create_user(user_data=user_data)
    return user 


@router.post("/login")
async def login(
    login_data: UserLogin,
    user_service: Annotated[
        UserService,
        Depends(get_user_service)
    ],
):
    user = await user_service.authenticate(login_data.login, login_data.password)
    access_token = create_jwt_token(data={
        "sub": user.id,
        "type": "access_token",
        "username": user.username,
        })
    return {
        "message": "Login successful 🙂‍↕️🤌",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
    }


@router.post("/verify-email")
async def verify_email(
    request: VerifyEmail,
    user_service: Annotated[
        UserService,
        Depends(get_user_service)
    ],
):
    await user_service.verify_email_token(request.token)
    
    return {
        "message": "Email verified successfully 🏆",
    }
    

# 😺 todo: create template for bridge page!!
# todo: ando 🤏 finish other routers:
    

@router.post("/logout")
async def logout():
    pass

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    user_service: Annotated[
        UserService, 
        Depends(get_user_service)
    ],
    
):
    await user_service.forgot_password(request.email)
    return {
        "message": "Email for reset password was sent!"
    }

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    user_service: Annotated[
        UserService, 
        Depends(get_user_service)
        ],
):
    await user_service.reset_password(request.token, request.password)
    return {
        "message": "Password reset successfully"
    }