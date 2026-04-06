from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from . import model, schema

def count_users(db: Session) -> int:
    return db.query(model.User).count()

def get_user_by_id(db: Session, user_id: int) -> model.User | None:
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> model.User | None:
    return db.query(model.User).filter(model.User.email == email).first()

def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[model.User]:
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schema.UserCreate) -> model.User:
    db_user = model.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: model.User, user_update: schema.UserUpdate) -> model.User:
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active
    if user_update.role is not None:
        db_user.role = user_update.role
    db.commit()
    db.refresh(db_user)
    return db_user
