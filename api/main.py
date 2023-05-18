from fastapi import APIRouter
from api.endpoints.auth import router as auth_router
from api.endpoints.articles import router as articles_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(articles_router, prefix="/articles", tags=["articles"])