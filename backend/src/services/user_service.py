from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from jose import jwt
from backend.src import models, schemas
from backend.src.utils.hashing import hash_password, verify_password
from backend.src.utils.redis_util import redis_client
from backend.src.config.settings import settings
from backend.src.core.logger import get_logger

logger = get_logger(__name__)

class UserService:
    """
    User Service
    ============
    Xử lý toàn bộ business logic liên quan đến User, bao gồm:
    - Đăng ký
    - Đăng nhập
    - Quản lý token
    - CRUD user
    """

    # ===================== AUTH =====================

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> models.User:
        try:
            db_user = db.query(models.User).filter(models.User.email == user.email).first()
            if db_user:
                logger.warning(f"Email {user.email} đã tồn tại")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            hashed_password = hash_password(user.password)
            new_user = models.User(
                email=user.email,
                hashed_password=hashed_password,
                role=user.role if hasattr(user, "role") else "student"
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info(f"Đăng ký user thành công: {new_user.email}")
            return new_user

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Lỗi DB khi tạo user: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        except Exception as e:
            db.rollback()
            logger.exception(f"Lỗi không xác định khi tạo user: {e}")
            raise HTTPException(status_code=500, detail="Unexpected error")

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            logger.warning(f"Đăng nhập thất bại: {email} không tồn tại")
            return None

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Đăng nhập thất bại: {email} mật khẩu sai")
            return None

        logger.info(f"Đăng nhập thành công: {email}")
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = UserService.authenticate_user(db, email, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Sinh JWT token
        access_token = UserService.create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        refresh_token = UserService.create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(days=7)
        )

        # Lưu refresh token vào Redis với TTL = 7 ngày
        redis_client.setex(f"refresh_token:{user.id}", timedelta(days=7), refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    @staticmethod
    def logout(user_id: str):
        redis_client.delete(f"refresh_token:{user_id}")
        logger.info(f"Đăng xuất user: {user_id}")
        return {"msg": "Logged out successfully"}

    # ===================== CRUD =====================

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: str, update_data: schemas.UserUpdate):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        logger.info(f"Update user thành công: {db_user.email}")
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: str):
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(db_user)
        db.commit()
        logger.info(f"Đã xóa user: {db_user.email}")
