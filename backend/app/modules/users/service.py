from sqlalchemy.orm import Session
from . import model, repository, schema

def count_users(db: Session) -> int:
    return repository.count_users(db)

def get_user_by_id(db: Session, user_id: int) -> model.User | None:
    return repository.get_user_by_id(db, user_id)

def get_user_by_email(db: Session, email: str) -> model.User | None:
    return repository.get_user_by_email(db, email)

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[model.User]:
    return repository.list_users(db, skip=skip, limit=limit)

def create_user(db: Session, user: schema.UserCreate) -> model.User:
    return repository.create_user(db, user)

def update_user(db: Session, db_user: model.User, user_update: schema.UserUpdate) -> model.User:
    return repository.update_user(db, db_user, user_update)