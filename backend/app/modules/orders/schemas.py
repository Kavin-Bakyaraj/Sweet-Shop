from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    sweet_id: str
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")

class OrderCreate(BaseModel):
    items: List[OrderItem] = Field(min_items=1, description="Order must contain at least one item")

class OrderItemResponse(OrderItem):
    name: str
    price: float

class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItemResponse]
    total_price: float
    status: str
    created_at: datetime
