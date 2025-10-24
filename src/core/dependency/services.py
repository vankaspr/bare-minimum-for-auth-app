from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.database import db_helper
from core.services.user import UserService
from core.services.admin import AdminService

async def get_user_service(
    background_task: BackgroundTasks,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
        ]
) -> UserService:
    return UserService(
        session=session,
        background_task=background_task
        )
    
    
async def get_admin_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
) -> AdminService:
    return AdminService(session=session)