from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from core.database import db_helper
from utilities.access_token import verify_token
from core.services.user import UserService
from .transport import security

async def get_current_user(
    token: Annotated[
        str,
        Depends(security)
    ], 
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ]
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    payload = verify_token(token.credentials)
    if not payload:
        raise credentials_exception
    
    user_id_str: str = payload.get("sub")
    if not user_id_str:
        raise credentials_exception
    
    try:
        user_id = int(user_id_str)  # ← конвертируем обратно в int
    except ValueError:
        raise credentials_exception
    
    user_service = UserService(session) 
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise credentials_exception
    
    return user 