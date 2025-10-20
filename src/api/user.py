from fastapi import APIRouter, Depends
from typing import Annotated
from core.database.models import User
from core.dependency.user import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/me")
async def profile(
    user: Annotated[
        User,
        Depends(get_current_user)
    ]
):
    return {
        "message": "👺 - Current user info:",
        "id": user.id,
        "email": user.email, 
        "username": user.username
    }