from pydantic import BaseModel, Field
from typing import Optional

class SweetBase(BaseModel):
    name: str
    category: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

class SweetCreate(SweetBase):
    pass

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)

class SweetResponse(SweetBase):
    id: str

    class Config:
        from_attributes = True
