from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.schemas.user import UserCreate, UserLogin
from core.database import db_helper
from core.services.user import UserService

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
    
    return {
        "message": "Login successful 🙂‍↕️🤌",
        "user_id": user.id,
    }

