from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["viewer", "analyst", "admin"] = "viewer"

class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[Literal["viewer", "analyst", "admin"]] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
