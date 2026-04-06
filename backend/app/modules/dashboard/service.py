from sqlalchemy.orm import Session
import httpx
from fastapi import HTTPException
from app.core.config import settings
from . import repository

def _build_external_url() -> str:
    base = settings.EXTERNAL_API_BASE_URL.rstrip("/")
    path = settings.EXTERNAL_API_PATH.lstrip("/")
    return f"{base}/{path}"

def _initialize_month_bucket(month: str) -> dict[str, float | str]:
    return {"month": month, "income": 0.0, "expense": 0.0}

def get_total_by_type(db: Session, user_id: int, role: str, record_type: str):
    return repository.sum_amount_by_type(db, user_id, role, record_type)

def get_category_breakdown(db: Session, user_id: int, role: str):
    results = repository.category_breakdown(db, user_id, role)
    return [{"category": r.category, "total": r.total} for r in results]

def get_monthly_trends(db: Session, user_id: int, role: str):
    results = repository.monthly_trends(db, user_id, role)
    buckets: dict[str, dict[str, float | str]] = {}
    for row in results:
        month = row.month
        if month not in buckets:
            buckets[month] = _initialize_month_bucket(month)
        metric = "income" if row.type == "income" else "expense"
        buckets[month][metric] += row.total
    return [buckets[month] for month in sorted(buckets.keys())]

def get_recent_activity(db: Session, user_id: int, role: str, limit: int = 5):
    return repository.recent_activity(db, user_id, role, limit)

def get_external_api_data():
    url = _build_external_url()
    try:
        response = httpx.get(
            url, timeout=settings.EXTERNAL_API_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="External API unreachable")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail=f"External API error: {exc.response.status_code}")
    except ValueError:
        raise HTTPException(
            status_code=502, detail="External API returned non-JSON response")
    return {
        "source_url": url,
        "status": "success",
        "data": payload,
    }
