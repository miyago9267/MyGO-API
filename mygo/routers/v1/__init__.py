"""V1 API Routers"""
from fastapi import APIRouter
from .images import router as images_router
from . import health

router = APIRouter()

router.include_router(
    images_router,
    prefix="/images",
    tags=["Images"]
)

# Health check endpoint
router.add_api_route(
    "/health",
    health.health_check,
    methods=["GET"],
    summary="健康檢查",
    description="檢查 API 服務狀態",
    tags=["Health"]
)
