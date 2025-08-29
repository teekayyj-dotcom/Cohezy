from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..services.session_service import SessionService
from ..services.auth_service import require_role
from .users import get_current_user
from ..models.user import User
from ..utils.enums import UserRole

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("{session_id}/token", status_code=status.HTTP_201_CREATED)
async def create_session_token(session_id: str, current_user: User = Depends(get_current_user)):
    require_role(current_user, [UserRole.ADMIN])
    session_token = SessionService.create_session(session_id, current_user.id)
    return {"session_token": session_token}

@router.post("{session_id}/join")
async def join_session(session_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    token = SessionService.create_session(session_id, current_user.id)
    return {"session_id": session_id,
            "session_token": token,
            "message": "Joined session successfully"}

@router.get("{session_id}/verify")
async def verify_session(session_id: str, session_token: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_valid = SessionService.verify_session(session_id, session_token)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")
    return {"message": "Session token is valid"}

@router.delete("{session_id}/leave")
async def leave_session(session_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    SessionService.delete_session(session_id, current_user.id)
    return {"message": "Left session successfully"}
