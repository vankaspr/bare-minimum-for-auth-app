from fastapi import APIRouter
from .verification_bridge import router as verification_router
from .reset_bridge import router as reset_router


router = APIRouter()
router.include_router(verification_router)
router.include_router(reset_router)
