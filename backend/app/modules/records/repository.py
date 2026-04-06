from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.orm import Session
from . import model, schema

def create_record(db: Session, record: schema.RecordCreate, user_id: int) -> model.Record:
    record_data = record.model_dump(exclude={"user_id"}, exclude_unset=True)
    db_record = model.Record(**record_data, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def list_records(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    role: str = "viewer",
    record_type: str | None = None,
    category: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    search: str | None = None,
) -> list[model.Record]:
    query = db.query(model.Record)
    filters = []
    if role == "viewer":
        filters.append(model.Record.user_id == user_id)
    if record_type:
        filters.append(model.Record.type == record_type)
    if category:
        filters.append(model.Record.category == category)
    if date_from:
        filters.append(model.Record.date >= date_from)
    if date_to:
        filters.append(model.Record.date <= date_to)
    if search:
        filters.append(
            or_(
                model.Record.category.ilike(f"%{search}%"),
                model.Record.notes.ilike(f"%{search}%"),
            )
        )
    if filters:
        query = query.filter(*filters)

    return query.offset(skip).limit(limit).all()

def get_record_by_id(db: Session, record_id: int) -> model.Record | None:
    return db.query(model.Record).filter(model.Record.id == record_id).first()

def update_record(db: Session, db_record: model.Record, record_update: schema.RecordUpdate) -> model.Record:
    update_data = record_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_record(db: Session, db_record: model.Record) -> None:
    db.delete(db_record)
    db.commit()
