from enum import Enum
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from backend.src.utils.enums import MemberRole

class SessionMember(Base):
    __tablename__ = 'session_members'

    id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    role = Column(Enum(MemberRole), nullable=False, default=MemberRole.MEMBER)  
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="session_members")
    user = relationship("User", back_populates="session_members")

    __table_args__ = (UniqueConstraint('session_id', 'user_id', name='_session_user_uc'),)