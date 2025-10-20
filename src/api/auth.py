from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.schemas.user import UserCreate, UserLogin
from core.database import db_helper
from core.services.user import UserService

from utilities.access_token import create_access_token

from core.config import settings

router = APIRouter(
    prefix=settings.api.auth,
    tags=["Auth"],
)

@router.post("/register")
async def register(
    user_data: UserCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ]
):
    user_service = UserService(session=session)
    user = await user_service.create_user(user_data=user_data)
    return user 


@router.post("/login")
async def login(
    login_data: UserLogin,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ]
):
    user_service = UserService(session=session)
    user = await user_service.authenticate(login_data.login, login_data.password)
    
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "message": "Login successful 🙂‍↕️🤌",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
    }

