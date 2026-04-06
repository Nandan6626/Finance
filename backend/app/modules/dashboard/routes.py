from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.users.model import User
from app.middleware.auth import get_current_user, RoleChecker
from . import schema, controller

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
@router.get("/", response_model=schema.DashboardSummary)
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(RoleChecker(["admin", "analyst"]))):
    return controller.get_dashboard_summary(db, current_user)
@router.get("/external-data", response_model=schema.ExternalAPIResponse)
def get_external_data(current_user: User = Depends(RoleChecker(["admin", "analyst"]))):
    return controller.get_external_api_data()
