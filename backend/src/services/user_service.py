from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from jose import jwt
from ..models.user import User
from ..utils.hashing import hash_password, verify_password
from ..utils.enums import UserRole
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..schemas.auth import TokenResponse, RefreshTokenResponse
from ..config.settings import settings
from ..core.logger import get_logger

logger = get_logger(__name__)

class UserService:

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get user by ID"""
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def delete_user(db: Session, user_id: str) -> bool:
        """Soft delete a user by setting is_active to False"""
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user.is_active = False
        db.commit()
        return True

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all active users with pagination"""
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        try:
            db_user = db.query(User).filter(User.email == user.email).first()
            if db_user:
                logger.warning(f"Email {user.email} đã tồn tại")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            hashed_password = hash_password(user.password)
            new_user = User(
                email=user.email,
                hashed_password=hashed_password,
                role=user.role if hasattr(user, "role") else UserRole.STUDENT,
                full_name=user.full_name if hasattr(user, "full_name") else None
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
        user = db.query(User).filter(User.email == email).first()
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

        # redis_client.setex(f"refresh_token:{user.id}", timedelta(days=7), refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    @staticmethod
    def logout(user_id: str):
        logger.info(f"Đăng xuất user: {user_id}")
        return {"msg": "Logged out successfully"}

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: str, update_data: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
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
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(db_user)
        db.commit()
        logger.info(f"Đã xóa user: {db_user.email}")
