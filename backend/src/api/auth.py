from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import deps
from ..services.redis_service import RedisService
from ..schemas.auth import LoginRequest, TokenResponse, RegisterRequest
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login_for_access_token(form_data: LoginRequest, db: Session = Depends(deps.get_db)) -> TokenResponse:
    user = AuthService.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = AuthService.create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: str = Depends(deps.get_current_user)) -> dict:
    RedisService.revoke_token(current_user.user_id)
    return {"msg": "Successfully logged out"}
