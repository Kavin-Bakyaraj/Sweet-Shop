from app.core.database import db
from typing import List, Optional

async def list_sweets():
    database = db.get_db()
    sweets = await database.sweets.find().to_list(length=None)
    for sweet in sweets:
        sweet["id"] = str(sweet["_id"])
    return sweets

async def search_sweets(q: Optional[str] = None, category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    database = db.get_db()
    query = {}
    
    if q:
        query["name"] = {"$regex": q, "$options": "i"}
    
    if category:
        query["category"] = category
        
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
            
    sweets = await database.sweets.find(query).to_list(length=None)
    for sweet in sweets:
        sweet["id"] = str(sweet["_id"])
    return sweets
