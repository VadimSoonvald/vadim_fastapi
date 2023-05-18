import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")


class DatabaseConnection:
    client: AsyncIOMotorClient = None


db = DatabaseConnection()


def get_database() -> AsyncIOMotorClient:
    if db.client is None:
        db.client = AsyncIOMotorClient(DATABASE_URL)

    return db.client[DATABASE_NAME]
