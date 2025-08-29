from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..services.session_service import SessionService
from ..services.auth_service import require_role
from .users import get_current_user
from ..models.user import User
from ..utils.enums import UserRole

from ..schemas.session import SessionCreate, SessionResponse
from fastapi import Response

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new session. The creator automatically becomes the owner."""
    session = SessionService.create_session(db, current_user.id, session_data)
    return session

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific session by ID"""
    session = SessionService.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session

@router.get("/", response_model=list[SessionResponse])
async def get_all_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all sessions (Admin only)"""
    require_role(current_user, [UserRole.ADMIN])
    sessions = SessionService.get_all_sessions(db, skip, limit)
    return sessions

@router.post("/{session_id}/join")
async def join_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Join a session as a member"""
    member = SessionService.join_session(db, session_id, current_user.id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or inactive"
        )
    return {"message": "Successfully joined session"}

@router.delete("/{session_id}/leave")
async def leave_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Leave a session"""
    success = SessionService.leave_session(db, session_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not leave session. Either you're not a member, you're the owner, or you've already left"
        )
    return {"message": "Successfully left session"}
