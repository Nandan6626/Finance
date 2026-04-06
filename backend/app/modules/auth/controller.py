from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import service

def login_for_access_token(db: Session, email: str, password: str):
    auth_result = service.authenticate_user(db, email, password)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if auth_result == "inactive":
        raise HTTPException(status_code=400, detail="Inactive user")
    return service.issue_access_token(auth_result.id)
