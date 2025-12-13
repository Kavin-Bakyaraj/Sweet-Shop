from fastapi import APIRouter, Depends
from app.modules.inventory.schemas import RestockRequest, InventoryResponse
from app.modules.inventory.service import purchase_sweet, restock_sweet
from app.core.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/inventory/sweets", tags=["Inventory"])

@router.post("/{id}/purchase", response_model=InventoryResponse)
async def purchase(id: str, user=Depends(get_current_user)):
    # Default quantity 1 for now as per requirement implication
    return await purchase_sweet(id, quantity=1)

@router.post("/{id}/restock", response_model=InventoryResponse)
async def restock(id: str, request: RestockRequest, admin=Depends(get_current_admin)):
    return await restock_sweet(id, request.quantity)
