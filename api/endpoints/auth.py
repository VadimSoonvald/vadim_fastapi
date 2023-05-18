from typing import Union

import bcrypt
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from database.main import get_database
from models.auth import LoginModel, SignUpModel
from models.user import UserModel
from services.user import UserService

router = APIRouter()


@router.post("/login")
async def login(
        body: LoginModel,
        db: AsyncIOMotorClient = Depends(get_database)
) -> Union[dict, UserModel]:
    user = await UserService.get_by_username(body.user.username, db)
    if not user:
        return {"error": "Invalid credentials"}

    if not bcrypt.checkpw(body.user.password.encode("utf-8"), user.password.encode("utf-8")):
        return {"error": "Invalid credentials"}

    return {
        "user": user.to_user_response()
    }


@router.post("/register")
async def register(
        body: SignUpModel,
        db: AsyncIOMotorClient = Depends(get_database)
):
    is_user_exists = await UserService.get_by_username(body.user.username, db) or await UserService.get_by_email(
        body.user.email, db)
    if is_user_exists:
        return {"error": "User already exists"}

    hashed_password = bcrypt.hashpw(body.user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = UserModel(
        username=body.user.username,
        email=body.user.email,
        password=hashed_password,
    )

    await UserService.create(user, db)
    return {
        "user": user.to_user_response()
    }
