from fastapi import APIRouter

from app.api.api_v1.endpoints import items, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
