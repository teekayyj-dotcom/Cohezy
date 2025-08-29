import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from .base import Base
from ..utils.enums import UserRole

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)

    session_memberships = relationship(
        "SessionMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )
