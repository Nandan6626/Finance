from pydantic import BaseModel
from typing import List
from typing import Any
from app.modules.records.schema import RecordOut

class CategoryBreakdown(BaseModel):
    category: str
    total: float

class MonthlyTrend(BaseModel):
    month: str  # YYYY-MM
    income: float
    expense: float

class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    category_breakdown: List[CategoryBreakdown]
    monthly_trends: List[MonthlyTrend]
    recent_activity: List[RecordOut]

class ExternalAPIResponse(BaseModel):
    source_url: str
    status: str
    data: dict[str, Any]
