from fastapi import APIRouter, Query, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from slugify import slugify

from database.main import get_database
from models.articles import ArticleCreateModel, ArticleModel
from models.common.object_id import PyObjectId
from services.article import ArticleService
from services.user import UserService

router = APIRouter()


@router.get("/feed")
async def feed(
        user_id: PyObjectId = Query(alias="userId"),
        limit: int = 20,
        offset: int = 0,
        db: AsyncIOMotorClient = Depends(get_database)
):
    user = await UserService.get_by_id(user_id, db)
    if not user:
        return {"error": "User not found"}

    articles = await ArticleService.get_feed(user, limit, offset, db)

    return {
        "articles": [await article.to_article_response(db, user) for article in articles],
        "articlesCount": len(articles)
    }


@router.get("/")
async def articles(
        user_id: PyObjectId = Query(alias="userId"),
        tag: str = None,
        author: str = None,
        favourited: str = None,
        limit: int = 20,
        offset: int = 0,
        db: AsyncIOMotorClient = Depends(get_database)
):
    user = await UserService.get_by_id(user_id, db)
    if not user:
        return {"error": "User not found"}

    articles = await ArticleService.get_articles(tag, author, favourited, limit, offset, db)

    return {
        "articles": [await article.to_article_response(db, user) for article in articles],
        "articlesCount": len(articles)
    }


@router.get("/{slug}")
async def article(
        user_id: PyObjectId = Query(alias="userId"),
        slug: str = None,
        db: AsyncIOMotorClient = Depends(get_database)
):
    user = await UserService.get_by_id(user_id, db)
    if not user:
        return {"error": "User not found"}

    article = await ArticleService.get_by_slug(slug, db)
    if not article:
        return {"error": "Article not found"}

    return {"article": await article.to_article_response(db, user)}


@router.post("/")
async def create_article(
        body: ArticleCreateModel,
        user_id: PyObjectId = Query(alias="userId"),
        db: AsyncIOMotorClient = Depends(get_database)
):
    user = await UserService.get_by_id(user_id, db)
    if not user:
        return {"error": "User not found"}

    is_article_exists = await ArticleService.get_by_slug(slugify(body.article.title), db)
    if is_article_exists:
        return {"error": "Article already exists"}

    new_article = ArticleModel(
        slug=slugify(body.article.title),
        title=body.article.title,
        description=body.article.description,
        body=body.article.body,
        tag_list=body.article.tag_list,
        author=user.id
    )

    article = await ArticleService.create(new_article, db)

    return {"article": await article.to_article_response(db, user)}
