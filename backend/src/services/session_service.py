import uuid
from datetime import datetime, timedelta
from ..config.settings import settings

from sqlalchemy.orm import Session
from ..models.session import Session as SessionModel
from ..models.session_member import SessionMember
from ..schemas.session import SessionCreate
from ..utils.enums import MemberRole, UserRole

class SessionService:
    @staticmethod
    def create_session(db: Session, user_id: str, session_data: SessionCreate) -> SessionModel:
        """Create a new session and make the creator the owner"""
        
        # Create the session
        session = SessionModel(
            title=session_data.title,
            description=session_data.description,
            is_active=True
        )
        db.add(session)
        db.flush()  # To get the session ID

        # Create the session member record for the owner
        session_member = SessionMember(
            session_id=session.id,
            user_id=user_id,
            role=MemberRole.OWNER,
            is_active=True
        )
        db.add(session_member)
        db.commit()
        db.refresh(session)
        
        return session

    @staticmethod
    def get_session(db: Session, session_id: str) -> SessionModel:
        """Get a session by ID"""
        return db.query(SessionModel).filter(
            SessionModel.id == session_id,
            SessionModel.is_active == True
        ).first()

    @staticmethod
    def join_session(db: Session, session_id: str, user_id: str) -> SessionMember:
        """Join a session as a member"""
        # Check if session exists and is active
        session = db.query(SessionModel).filter(
            SessionModel.id == session_id,
            SessionModel.is_active == True
        ).first()
        if not session:
            return None

        # Check if user is already a member
        existing_member = db.query(SessionMember).filter(
            SessionMember.session_id == session_id,
            SessionMember.user_id == user_id
        ).first()
        
        if existing_member:
            if not existing_member.is_active:
                existing_member.is_active = True
                db.commit()
            return existing_member

        # Create new member
        session_member = SessionMember(
            session_id=session_id,
            user_id=user_id,
            role=MemberRole.MEMBER,
            is_active=True
        )
        db.add(session_member)
        db.commit()
        db.refresh(session_member)
        return session_member

    @staticmethod
    def leave_session(db: Session, session_id: str, user_id: str) -> bool:
        """Leave a session"""
        # Find the member record
        member = db.query(SessionMember).filter(
            SessionMember.session_id == session_id,
            SessionMember.user_id == user_id,
            SessionMember.is_active == True
        ).first()

        if not member:
            return False

        # Can't leave if you're the owner
        if member.role == MemberRole.OWNER:
            return False

        member.is_active = False
        db.commit()
        return True

    @staticmethod
    def get_all_sessions(db: Session, skip: int = 0, limit: int = 100) -> list[SessionModel]:
        """Get all active sessions with pagination"""
        return db.query(SessionModel).filter(
            SessionModel.is_active == True
        ).offset(skip).limit(limit).all()
