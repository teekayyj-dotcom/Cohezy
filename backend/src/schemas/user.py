from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from ..utils.enums import UserRole

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    full_name: str = Field(..., description="The user's full name")
    is_active: bool = Field(default=True, description="Indicates if the user is active")
    is_superuser: bool = Field(default=False, description="Indicates if the user has superuser privileges")
    role: UserRole = Field(default=UserRole.STUDENT, description="The user's role")


class UserCreate(UserBase):
    password: str = Field(..., description="The user's password")

class UserUpdate(BaseModel):
    email: EmailStr | None = Field(None, description="The user's email address")
    full_name: str | None = Field(None, description="The user's full name")
    hashed_password: str | None = Field(None, description="The user's password")
    is_active: bool | None = Field(None, description="Indicates if the user is active")
    is_superuser: bool | None = Field(None, description="Indicates if the user has superuser privileges")

class UserResponse(UserBase):
    id: UUID4 = Field(..., description="The unique identifier for the user")
    created_at: datetime = Field(..., description="The timestamp when the user was created")

    class Config:
        from_attributes = True

class UserInDBBase(UserBase):
    id: UUID4 = Field(..., description="The unique identifier for the user")
    created_at: datetime = Field(..., description="The timestamp when the user was created")
    updated_at: datetime = Field(..., description="The timestamp when the user was last updated")

    class Config:
        from_attributes = True
        
class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int