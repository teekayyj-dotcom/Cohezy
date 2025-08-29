from fastapi import APIRouter, Depends, HTTPException, status
from . import auth, users, sessions
from ..core.config import settings

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(sessions.router)

