from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f"{settings.API_V1_STR}/openapi.json")

if settings.BACKEND_CORS_ORIGINS:
    # print("=== : ", settings.BACKEND_CORS_ORIGINS )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        # allow_origins=["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:8080", "https://localhost", "https://localhost:4200", "https://localhost:3000", "https://localhost:8080", "http://dev.lakadee.com", "https://stag.lakadee.com", "https://lakadee.com"],
        # allow_origins=["http://localhost:8080"],
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
