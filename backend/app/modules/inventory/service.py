from app.core.database import db
from fastapi import HTTPException
from bson import ObjectId

async def purchase_sweet(id: str, quantity: int = 1):
    database = db.get_db()
    sweet = await database.sweets.find_one({"_id": ObjectId(id)})
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    
    if sweet["quantity"] < quantity:
        raise HTTPException(status_code=400, detail="Out of stock or insufficient quantity")
    
    # Decrement quantity
    await database.sweets.update_one({"_id": ObjectId(id)}, {"$inc": {"quantity": -quantity}})
    
    updated_sweet = await database.sweets.find_one({"_id": ObjectId(id)})
    return {"message": "Purchase successful", "quantity": updated_sweet["quantity"]}

async def restock_sweet(id: str, quantity: int):
    database = db.get_db()
    result = await database.sweets.update_one({"_id": ObjectId(id)}, {"$inc": {"quantity": quantity}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    
    updated_sweet = await database.sweets.find_one({"_id": ObjectId(id)})
    return {"message": "Restock successful", "quantity": updated_sweet["quantity"]}
