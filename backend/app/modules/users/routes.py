from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth import get_current_user, get_current_user_optional, RoleChecker
from . import schema, controller, model
router = APIRouter(prefix="/users", tags=["Users"])
@router.post("/", response_model=schema.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schema.UserCreate,
    db: Session = Depends(get_db),
    current_user: model.User | None = Depends(get_current_user_optional)
):
    """Create first user publicly, then admin-only."""
    return controller.create_user(db, user, current_user)

@router.get("/", response_model=list[schema.UserOut])
def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: model.User = Depends(RoleChecker(["admin"]))
):
    """Get all users. Admin only."""
    return controller.get_users(db, skip=skip, limit=limit)

@router.get("/me", response_model=schema.UserOut)
def read_user_me(current_user: model.User = Depends(get_current_user)):
    """Get current user."""
    return controller.get_user_me(current_user)

@router.patch("/{user_id}", response_model=schema.UserOut)
def update_user(
    user_id: int, user_update: schema.UserUpdate, db: Session = Depends(get_db),
    current_user: model.User = Depends(RoleChecker(["admin"]))
):
    """Update user role/status. Admin only."""
    return controller.update_user(db, user_id, user_update)
