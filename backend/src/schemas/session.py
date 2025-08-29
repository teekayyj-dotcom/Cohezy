from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from .user import UserResponse

class SessionBase(BaseModel):
    user_id: UUID4 = Field(..., description="The unique identifier for the user")
    session_token: str = Field(..., description="The session token")
    expires_at: datetime = Field(..., description="The expiration timestamp of the session")

class SessionCreate(SessionBase):
    name: str = Field(..., description="The name of the session")
    description: str | None = Field(None, description="A brief description of the session")
    start_time: datetime = Field(..., description="The timestamp when the session starts")
    end_time: datetime | None = Field(None, description="The timestamp when the session ends")

class SessionUpdate(BaseModel):
    session_token: str | None = Field(None, description="The session token")
    expires_at: datetime | None = Field(None, description="The expiration timestamp of the session")

class SessionResponse(SessionBase):
    id: UUID4 = Field(..., description="The unique identifier for the session")
    name: str = Field(..., description="The name of the session")
    description: str | None = Field(None, description="A brief description of the session")
    created_at: datetime = Field(..., description="The timestamp when the session was created")
    start_time: datetime = Field(..., description="The timestamp when the session started")
    end_time: datetime | None = Field(None, description="The timestamp when the session ended")
    owner_id: UUID4 = Field(..., description="The unique identifier for the session owner")

class SessionListResponse(BaseModel):
    sessions: list[SessionResponse] = Field(..., description="A list of session responses")
    total: int = Field(..., description="Total number of sessions")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of sessions per page")
    pages: int = Field(..., description="Total number of pages")
