from fastapi import APIRouter
from backend.api import health, reviews, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(reviews.router, prefix="/api", tags=["reviews"])
api_router.include_router(ui.router, tags=["ui"])
