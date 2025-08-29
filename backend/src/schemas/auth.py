from .__base__ import BaseSchema
from pydantic import EmailStr, Field
from ..utils.enums import UserRole

class RegisterRequest(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    role: UserRole = UserRole.STUDENT

class LoginRequest(BaseSchema):
    email: EmailStr
    password: str

class TokenData(BaseSchema):
    user_id: str

class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"

class RefreshTokenResponse(BaseSchema):
    access_token: str
    token_type: str
    refresh_token: str

