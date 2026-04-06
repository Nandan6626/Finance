from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.modules.users.model import User
from . import schema, controller
router = APIRouter(prefix="/records", tags=["Records"])
@router.post("/", response_model=schema.RecordOut, status_code=status.HTTP_201_CREATED)
def create_record(record: schema.RecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.create_record(db, record, current_user)

@router.get("/", response_model=list[schema.RecordOut])
def get_records(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    record_type: Optional[str] = Query(default=None, alias="type"),
    category: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return controller.get_records(
        db,
        skip,
        limit,
        record_type,
        category,
        date_from,
        date_to,
        search,
        current_user,
    )
@router.get("/{record_id}", response_model=schema.RecordOut)
def get_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.get_record(db, record_id, current_user)

@router.patch("/{record_id}", response_model=schema.RecordOut)
def update_record(record_id: int, record_update: schema.RecordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.update_record(db, record_id, record_update, current_user)

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return controller.delete_record(db, record_id, current_user)
