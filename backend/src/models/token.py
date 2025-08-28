import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from .base import Base

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_blacklisted = Column(Boolean, default=False)
    refresh_token = Column(String, unique=True, nullable=True)
    access_token = Column(String, unique=True, nullable=True)