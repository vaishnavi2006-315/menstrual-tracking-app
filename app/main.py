from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.events import lifespan
from app.routes import router as api_router


settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
    allow_credentials=settings.cors_allow_credentials,
)

app.include_router(api_router)
