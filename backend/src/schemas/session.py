from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from .user import UserResponse

class SessionBase(BaseModel):
    title: str = Field(..., description="The title of the session")
    description: str | None = Field(None, description="A brief description of the session")

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    session_token: str | None = Field(None, description="The session token")
    expires_at: datetime | None = Field(None, description="The expiration timestamp of the session")

class SessionResponse(SessionBase):
    id: str = Field(..., description="The unique identifier for the session")
    is_active: bool = Field(..., description="Whether the session is active")
    created_at: datetime = Field(..., description="The timestamp when the session was created")
    updated_at: datetime | None = Field(None, description="The timestamp when the session was last updated")

class SessionListResponse(BaseModel):
    sessions: list[SessionResponse] = Field(..., description="A list of session responses")
    total: int = Field(..., description="Total number of sessions")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of sessions per page")
    pages: int = Field(..., description="Total number of pages")
