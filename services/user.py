from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from database.utils import USERS_COLLECTION
from models.common.object_id import PyObjectId
from models.user import UserModel


class UserService:

    @classmethod
    async def get_by_id(cls, user_id: PyObjectId, db: AsyncIOMotorClient) -> Optional[UserModel]:
        user = await db[USERS_COLLECTION].find_one({"_id": user_id})

        if not user:
            return None

        return UserModel.from_mongo(user)

    @classmethod
    async def get_by_username(cls, username: str, db: AsyncIOMotorClient) -> Optional[UserModel]:
        user = await db[USERS_COLLECTION].find_one({"username": username})

        if not user:
            return None

        return UserModel.from_mongo(user)

    @classmethod
    async def get_by_email(cls, email: str, db: AsyncIOMotorClient) -> Optional[UserModel]:
        user = await db[USERS_COLLECTION].find_one({"email": email})

        if not user:
            return None

        return UserModel.from_mongo(user)

    @classmethod
    async def create(cls, user: UserModel, db: AsyncIOMotorClient) -> UserModel:
        await db[USERS_COLLECTION].insert_one(user.mongo())

        return await cls.get_by_username(user.username, db)