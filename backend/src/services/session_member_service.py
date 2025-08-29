from pydantic import BaseModel, EmailStr, Field, UUID4
from utils.enums import UserRole

class SessionMemberBase(BaseModel):
    user_id: UUID4 = Field(..., description="The unique identifier for the user")
    session_id: UUID4 = Field(..., description="The unique identifier for the session")
    role: UserRole = Field(default=UserRole.VIEWER, description="The role of the user in the session")

class SessionMemberResponse(SessionMemberBase):
    id: str = Field(..., description="The unique identifier for the session member")
    class Config:
        orm_mode = True
