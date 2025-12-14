from datetime import datetime
from typing import List

class OrderModel:
    def __init__(self, user_id: str, items: List[dict], total_price: float, status: str = "completed"):
        self.user_id = user_id
        self.items = items
        self.total_price = total_price
        self.status = status
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "items": self.items,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at
        }
