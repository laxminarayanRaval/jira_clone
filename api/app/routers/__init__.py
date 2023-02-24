from fastapi import APIRouter
from app.routers import project, issue, comment, user

api_router = APIRouter(prefix="/api")

api_router.include_router(project.router, prefix="/project")
api_router.include_router(issue.router, prefix="/issue")
api_router.include_router(comment.router, prefix="/comment")
api_router.include_router(user.router, prefix="/user")
