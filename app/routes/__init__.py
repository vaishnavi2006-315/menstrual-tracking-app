from fastapi import APIRouter
from .health import router as health_router
from .cycle import router as cycle_router
from .user import router as user_router


router = APIRouter()
router.include_router(health_router)
router.include_router(cycle_router)
router.include_router(user_router)
