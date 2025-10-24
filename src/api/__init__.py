from fastapi import APIRouter
from core.config import settings
from .auth import router as auth_router
from .user import router as user_router
from .admin import router as admin_router

router = APIRouter(
    prefix=settings.api.prefix
)

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(admin_router)