from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.src.api import deps
from backend.src.services.redis_service import RedisService
from backend.src.schemas.auth import loginRequest, TokenResponse
from backend.src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login_for_access_token(form_data: loginRequest, db: Session = Depends(deps.get_db)) -> TokenResponse:
    user = AuthService.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = AuthService.create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: str = Depends(deps.get_current_user), redis=Depends(deps.get_redis)) -> dict:
    RedisService.revoke_token(current_user.user_id)
    return {"msg": "Successfully logged out"}
