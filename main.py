from fastapi import FastAPI
from api.main import router
from database.utils import connect_to_mongo, close_mongo_connection

app = FastAPI()

app.include_router(router, prefix="/api")

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)