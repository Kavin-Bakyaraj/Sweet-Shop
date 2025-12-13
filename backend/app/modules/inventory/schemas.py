from pydantic import BaseModel, Field

class PurchaseRequest(BaseModel):
    pass # No body needed for simple purchase, or maybe quantity?
    # Requirement says: POST /api/sweets/:id/purchase
    # Implies buying 1 unit? Or body with quantity?
    # "Purchase a sweet, decreasing its quantity."
    # Let's assume 1 unit for now, or optional quantity.
    # But usually purchase involves payment etc.
    # For this kata, just decrement quantity.
    quantity: int = Field(1, gt=0)

class RestockRequest(BaseModel):
    quantity: int = Field(..., gt=0)

class InventoryResponse(BaseModel):
    message: str
    quantity: int
