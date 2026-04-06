from sqlalchemy.orm import Session
from app.modules.users.model import User
from . import schema, service
def get_dashboard_summary(db: Session, current_user: User) -> schema.DashboardSummary:
    user_id = current_user.id
    role = current_user.role
    total_income = service.get_total_by_type(db, user_id, role, "income")
    total_expense = service.get_total_by_type(db, user_id, role, "expense")
    net_balance = total_income - total_expense
    category_breakdown = service.get_category_breakdown(db, user_id, role)
    monthly_trends = service.get_monthly_trends(db, user_id, role)
    recent_activity = service.get_recent_activity(db, user_id, role)
    return schema.DashboardSummary(
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        category_breakdown=category_breakdown,
        monthly_trends=monthly_trends,
        recent_activity=recent_activity
    )
def get_external_api_data() -> schema.ExternalAPIResponse:
    return service.get_external_api_data()
