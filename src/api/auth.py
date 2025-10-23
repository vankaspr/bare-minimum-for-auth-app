from exceptions import auth
from fastapi import APIRouter, Depends
from typing import Annotated


from core.database.schemas.user import UserCreate, UserLogin
from core.database.schemas.auth import (
    VerifyEmail,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    RefreshTokenRequest
    )

from core.database.models import User

from core.services.user import UserService
from core.dependency.services import get_user_service
from core.dependency.user import get_current_user

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
    
    refresh_token = await user_service.create_refresh_token(user.id)
    
    return {
        "message": "Login successful 🙂‍↕️🤌",
        "access_token": access_token,
        "refresh_token": refresh_token,
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
    

@router.post("/logout")
async def logout(
    user: Annotated[
        User,
        Depends(get_current_user)
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service)
    ]
):
    """ 
    Revokes all refresh tokens for the 
    current user upon logout.
    """
    await user_service.revoke_refresh_token(user.id)
    
    return {
        "message" : "Successfully logged out"
    }


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
    

@router.post("/refresh")
async def refresh(
    request: RefreshTokenRequest,
    user_service: Annotated[
        UserService, 
        Depends(get_user_service)
        ],
):
    """ 
    Issues new access and refresh tokens using a valid refresh token
    """
    
    # found olf refresh token in DB and validate it 
    token = await user_service.validate_refresh_token(request.refresh_token)
    
    token.is_revoked = True
    await user_service.session.commit()
    
    # create new access token
    access_token = create_jwt_token(
        {
            "sub": token.user_id,
            "type": "access_token",
        }
    )
    
    # create new refresh token 
    refresh_token = await user_service.create_refresh_token(token.user_id)
    
    return {
        "message": "Update access ando refresh tokens 🥳",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }