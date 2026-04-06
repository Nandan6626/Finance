from sqlalchemy import func
from sqlalchemy.orm import Session
from app.modules.records.model import Record
def sum_amount_by_type(db: Session, user_id: int, role: str, record_type: str) -> float:
    query = db.query(func.sum(Record.amount))
    if role == "viewer":
        query = query.filter(Record.user_id == user_id)
    query = query.filter(Record.type == record_type)
    result = query.scalar()
    return result if result else 0.0

def category_breakdown(db: Session, user_id: int, role: str):
    query = db.query(Record.category, func.sum(Record.amount).label("total"))
    if role == "viewer":
        query = query.filter(Record.user_id == user_id)
    query = query.filter(Record.type == "expense").group_by(Record.category)
    return query.all()

def monthly_trends(db: Session, user_id: int, role: str):
    query = db.query(func.strftime("%Y-%m", Record.date).label("month"),Record.type,
        func.sum(Record.amount).label("total"),
    )
    if role == "viewer":
        query = query.filter(Record.user_id == user_id)
    return query.group_by("month", Record.type).all()

def recent_activity(db: Session, user_id: int, role: str, limit: int = 5):
    query = db.query(Record).order_by(Record.date.desc())
    if role == "viewer":
        query = query.filter(Record.user_id == user_id)
    return query.limit(limit).all()
