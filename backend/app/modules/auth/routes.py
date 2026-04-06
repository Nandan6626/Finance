from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import controller, schema
router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/login", response_model=schema.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return controller.login_for_access_token(db, form_data.username, form_data.password)
