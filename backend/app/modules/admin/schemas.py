from pydantic import BaseModel, Field
from typing import Optional

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    image_url: Optional[str] = None

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None

class SweetResponse(BaseModel):
    id: str
    name: str
    category: str
    price: float
    quantity: int
    image_url: Optional[str] = None

class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str
