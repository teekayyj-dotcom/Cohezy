from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.router import api_router
from src.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from src.config.database import engine, Base
from src.core.logger import get_logger
from src.db.init_db import init_db
from src.models import session, user, session_member

logger = get_logger(__name__)

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cohezy",
        version="1.0.0",
        description="Cohezy API documentation",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(title="Cohezy", version="1.0.0")

app.openapi = custom_openapi

# Initialize database
init_db()

# Include routers
from src.core.config import settings
app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
