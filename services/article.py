from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from database.utils import ARTICLES_COLLECTION
from models.articles import ArticleModel
from models.user import UserModel


class ArticleService:
    @classmethod
    async def get_feed(cls, user: UserModel, limit: int, offset: int, db: AsyncIOMotorClient) -> List[ArticleModel]:
        articles = await db[ARTICLES_COLLECTION].find({"author": {"$in": user.following_users}}).skip(offset).limit(limit).to_list(limit)

        return [ArticleModel.from_mongo(article) for article in articles]

    @classmethod
    async def get_articles(cls, tag: str, author: str, favourited: str, limit: int, offset: int, db: AsyncIOMotorClient) -> List[ArticleModel]:
        query = {}
        if tag:
            query["tagList"] = tag
        if author:
            query["author"] = author
        if favourited:
            query["favorited"] = favourited

        articles = await db[ARTICLES_COLLECTION].find(query).skip(offset).limit(limit).to_list(limit)

        return [ArticleModel.from_mongo(article) for article in articles]

    @classmethod
    async def get_by_slug(cls, slug: str, db: AsyncIOMotorClient) -> ArticleModel:
        article = await db[ARTICLES_COLLECTION].find_one({"slug": slug})

        if not article:
            return None

        return ArticleModel.from_mongo(article)

    @classmethod
    async def create(cls, article: ArticleModel, db: AsyncIOMotorClient) -> ArticleModel:
        await db[ARTICLES_COLLECTION].insert_one(article.mongo())

        return await cls.get_by_slug(article.slug, db)