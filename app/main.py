from fastapi import Depends, FastAPI
from app.api.api_v1.api import api_router

app = FastAPI()

API_V1_STR: str = "/api/v1"
app.include_router(api_router, prefix=API_V1_STR)
