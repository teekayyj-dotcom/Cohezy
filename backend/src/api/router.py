from fastapi import APiRouter, Depends, HTTPException, status
from backend.src.api import auth, users, sessions

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(sessions.router)

