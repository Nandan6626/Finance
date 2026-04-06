from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password
from app.modules.users.service import get_user_by_email

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return "inactive"
    return user

def issue_access_token(user_id: int) -> dict[str, str]:
    access_token = create_access_token(subject=user_id)
    return {"access_token": access_token, "token_type": "bearer"}
