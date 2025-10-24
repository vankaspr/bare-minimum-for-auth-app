from fastapi import APIRouter, Depends
from typing import Annotated

from core.config import settings
from core.database.models import User
from core.services.admin import AdminService
from core.dependency.admin import get_current_superuser
from core.dependency.services import get_admin_service

router = APIRouter(
    prefix=settings.api.admin,
    tags=["Admin"]
)

@router.get("/statistic/users")
async def statistics(
    user: Annotated[
        User,
        Depends(get_current_superuser)
    ],
    admin_service: Annotated[
        AdminService,
        Depends(get_admin_service)
    ],
):
    return await admin_service.get_user_stats()
