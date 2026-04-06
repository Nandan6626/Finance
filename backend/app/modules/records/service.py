from sqlalchemy.orm import Session
from . import model, repository, schema
from datetime import datetime

def create_record(db: Session, record: schema.RecordCreate, user_id: int):
    return repository.create_record(db, record, user_id)

def get_records(
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
):
    return repository.list_records(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
        role=role,
        record_type=record_type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        search=search,
    )
def get_record(db: Session, record_id: int):
    return repository.get_record_by_id(db, record_id)

def update_record(db: Session, db_record: model.Record, record_update: schema.RecordUpdate):
    return repository.update_record(db, db_record, record_update)
def delete_record(db: Session, db_record: model.Record):
    repository.delete_record(db, db_record)
    return True
 