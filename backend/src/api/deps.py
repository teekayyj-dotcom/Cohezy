from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from backend.src.config.database import SessionLocal
from backend.src.services.auth_service import get_user_by_id
from backend.src.utils.redis_util import get_token, redis_client as RedisClient
from backend.src.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    try:
        return RedisClient().get_client()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot connect to Redis"
        )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), redis=Depends(get_redis)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        # Check token in Redis
        redis_token = get_token(user_id, redis)
        if redis_token and redis_token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired, please login again")

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def require_role(*allowed_roles):
    def role_checker(user=Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user
    return role_checker
