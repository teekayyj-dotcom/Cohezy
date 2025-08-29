from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.sql import func
from .base import Base
from ..utils.enums import MemberRole
import uuid

from sqlalchemy.orm import relationship

class SessionMember(Base):
    __tablename__ = 'session_members'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(MemberRole), nullable=False, default=MemberRole.MEMBER)
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="members")
    user = relationship("User", back_populates="session_memberships")

    __table_args__ = (UniqueConstraint('session_id', 'user_id', name='_session_user_uc'),)