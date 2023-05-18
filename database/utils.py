from motor.motor_asyncio import AsyncIOMotorClient

from database.main import db, DATABASE_URL


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(DATABASE_URL, maxPoolSize=100, minPoolSize=10)


async def close_mongo_connection():
    db.client.close()

USERS_COLLECTION = "users"
ARTICLES_COLLECTION = "articles"