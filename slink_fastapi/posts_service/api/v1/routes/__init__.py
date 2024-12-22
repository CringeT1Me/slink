from fastapi import APIRouter

from .posts import router as posts_router

router = APIRouter()
router.include_router(router=posts_router, prefix="/posts")
