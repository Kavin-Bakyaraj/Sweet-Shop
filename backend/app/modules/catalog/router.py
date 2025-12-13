from fastapi import APIRouter, Query
from typing import List, Optional
from app.modules.catalog.schemas import SweetResponse
from app.modules.catalog.service import list_sweets, search_sweets

router = APIRouter(prefix="/sweets", tags=["Catalog"])

@router.get("/search", response_model=List[SweetResponse])
async def search(
    q: Optional[str] = None, 
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    return await search_sweets(q, category, min_price, max_price)

@router.get("", response_model=List[SweetResponse])
async def get_all_sweets():
    return await list_sweets()
