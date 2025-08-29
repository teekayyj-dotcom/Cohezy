from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from . import deps
from ..schemas.user import UserCreate, UserResponse, UserListResponse
from ..services.user_service import UserService
from ..utils.enums import UserRole

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="Details of the newly created user"
)
def create_user(
    user: UserCreate,
    db: Session = Depends(deps.get_db)
) -> UserResponse:
    return UserService.create_user(db, user)

@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get all users",
    response_description="List of users"
)
def get_all_users(
    skip: int = Query(0, ge=0, description="Số lượng user cần bỏ qua"),
    limit: int = Query(100, ge=1, le=200, description="Số lượng user tối đa trả về"),
    db: Session = Depends(deps.get_db),
    current_user: UserResponse = Depends(deps.get_current_user)   # ✅ Yêu cầu đăng nhập
) -> UserListResponse:
    users = UserService.get_all_users(db, skip=skip, limit=limit)
    return UserListResponse(users=users)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    response_description="Details of the user"
)
def get_user_by_id(
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_user: UserResponse = Depends(deps.get_current_user)
) -> UserResponse:
    """Get a specific user by ID"""
    user = UserService.get_user_by_id(db, user_id)
    return user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    response_description="User deleted successfully"
)
def delete_user(
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_user: UserResponse = Depends(deps.get_current_user)
):
    """Delete a user (soft delete)"""
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    UserService.delete_user(db, user_id)
    return {"message": "User deleted successfully"}
    return user

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user info",
    response_description="Details of the current authenticated user"
)
def get_current_user(
    current_user: UserResponse = Depends(deps.get_current_user)
) -> UserResponse:
    return current_user

@router.delete(
    "/me",
    response_model=UserResponse,
    summary="Delete current user",
    response_description="Details of deleted user"
)
def delete_current_user(
    current_user: UserResponse = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> UserResponse:
    deleted_user = UserService.delete_user(db, current_user.id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return deleted_user
