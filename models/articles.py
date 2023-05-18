from datetime import datetime
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field

from models.common.mongo_model import MongoModel
from models.common.object_id import PyObjectId
from models.user import UserModel
from services.user import UserService


class ArticleModel(MongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId)
    slug: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    body: str = Field(...)
    tag_list: list[str] = Field(default=[], alias="tagList")
    author: PyObjectId = Field(...)
    favourites_count: int = Field(default=0, alias="favouritesCount")
    comments: list[PyObjectId] = Field(default=[])
    created_at: datetime = Field(default=datetime.utcnow(), alias="createdAt")
    updated_at: datetime = Field(default=datetime.utcnow(), alias="updatedAt")

    async def to_article_response(self, db: AsyncIOMotorClient, user: Optional[UserModel] = None):
        author = await UserService.get_by_id(self.author, db)

        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "body": self.body,
            "tagList": self.tag_list,
            "favorited": user and self.id in user.favourite_articles or False,
            "favoritesCount": self.favourites_count,
            "author": author.to_profile_response(),
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }


class ArticleCreateDataModel(MongoModel):
    title: str = Field(...)
    description: str = Field(...)
    body: str = Field(...)
    tag_list: list[str] = Field(default=[], alias="tagList")


class ArticleCreateModel(MongoModel):
    article: ArticleCreateDataModel