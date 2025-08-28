from fastapi import FastAPI
from backend.src.api.router import api_router
from backend.src.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from backend.src.config.database import engine, Base
from backend.src.config.redis_client import init_redis, close_redis
from backend.src.core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Cohezy", version="1.0.0")

Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    init_redis()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    close_redis()

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
