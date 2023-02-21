from fastapi import APIRouter
from app.routers.project import router

api_router = APIRouter(prefix="/api")

api_router.include_router(router, prefix="/project")
