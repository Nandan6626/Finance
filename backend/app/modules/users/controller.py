from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import schema, service
from .model import User

def create_user(db: Session, user: schema.UserCreate, current_user: User | None):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    has_users = service.count_users(db) > 0
    if has_users and (not current_user or current_user.role != "admin"):
        raise HTTPException(
            status_code=403, detail="Only admins can create users")
    return service.create_user(db=db, user=user)

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return service.get_users(db, skip=skip, limit=limit)

def get_user_me(current_user):
    return current_user

def update_user(db: Session, user_id: int, user_update: schema.UserUpdate):
    db_user = service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return service.update_user(db, db_user, user_update)
