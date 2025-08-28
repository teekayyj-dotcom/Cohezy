from .__base__ import BaseSchema

class TokenResponse(BaseSchema):
    access_token: str
    token_type: str
    refresh_token: str = "bearer"

class RefreshTokenResponse(BaseSchema):
    access_token: str
    token_type: str
    refresh_token: str

