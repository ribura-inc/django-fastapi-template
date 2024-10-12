from fastapi import APIRouter

from app.api.routes import (
    health,
    login,
    user,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"], prefix="/health")
api_router.include_router(login.router, tags=["login"], prefix="/login")
api_router.include_router(user.router, tags=["users"], prefix="/users")
