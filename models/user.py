from typing import Optional

from pydantic import Field

from models.common.mongo_model import MongoModel
from models.common.object_id import PyObjectId


class UserModel(MongoModel):
    id: PyObjectId = Field(default_factory=PyObjectId)
    username: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)
    bio: str = Field(default="")
    image: str = Field(default="https://static.productionready.io/images/smiley-cyrus.jpg")
    favourite_articles: list[PyObjectId] = Field(default=[], alias="favouriteArticles")
    following_users: list[PyObjectId] = Field(default=[], alias="followingUsers")

    def to_user_response(self):
        return {
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "image": self.image,
        }

    def to_profile_response(self, user_id: Optional[PyObjectId] = None):
        return {
            "username": self.username,
            "bio": self.bio,
            "image": self.image,
            "following": user_id and user_id in self.following_users or False,
        }
