from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime

class RecordBase(BaseModel):
    amount: float = Field(gt=0)
    type: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=100)
    date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=500)

class RecordCreate(RecordBase):
    user_id: Optional[int] = None

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=500)
    
class RecordOut(RecordBase):
    id: int
    user_id: int
    date: datetime
    model_config = ConfigDict(from_attributes=True)
