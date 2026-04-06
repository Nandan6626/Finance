from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import schema, service
from app.modules.users.model import User
from datetime import datetime
ADMIN_ROLE = "admin"
VIEWER_ROLE = "viewer"

def _ensure_admin(current_user: User, action: str) -> None:
    if current_user.role != ADMIN_ROLE:
        raise HTTPException(
            status_code=403, detail=f"Only admins can {action}")

def _resolve_target_user_id(record: schema.RecordCreate, current_user: User) -> int:
    return record.user_id if record.user_id else current_user.id

def create_record(db: Session, record: schema.RecordCreate, current_user: User):
    _ensure_admin(current_user, "create records")
    target_user_id = _resolve_target_user_id(record, current_user)
    target_user = db.query(User).filter(User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    return service.create_record(db=db, record=record, user_id=target_user_id)

def get_records(
    db: Session,
    skip: int,
    limit: int,
    record_type: str | None,
    category: str | None,
    date_from: datetime | None,
    date_to: datetime | None,
    search: str | None,
    current_user: User
):
    return service.get_records(
        db=db, user_id=current_user.id, skip=skip, limit=limit, role=current_user.role,
        record_type=record_type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        search=search,
    )

def get_record(db: Session, record_id: int, current_user: User):
    record = service.get_record(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if current_user.role == VIEWER_ROLE and record.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not permitted to access this record")
    return record

def update_record(db: Session, record_id: int, record_update: schema.RecordUpdate, current_user: User):
    _ensure_admin(current_user, "modify records")
    record = service.get_record(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return service.update_record(db, record, record_update)

def delete_record(db: Session, record_id: int, current_user: User):
    _ensure_admin(current_user, "delete records")
    record = service.get_record(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    service.delete_record(db, record)
    return {"detail": "Record deleted"}
