from fastapi import APIRouter
from apis.v1 import user,blog

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(blog.router, prefix="/blogs", tags=["Blogs"])