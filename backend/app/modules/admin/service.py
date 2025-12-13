from app.core.database import db
from app.modules.catalog.schemas import SweetCreate, SweetUpdate
from fastapi import HTTPException
from bson import ObjectId

async def create_sweet(sweet: SweetCreate):
    database = db.get_db()
    sweet_dict = sweet.dict()
    result = await database.sweets.insert_one(sweet_dict)
    sweet_dict["id"] = str(result.inserted_id)
    return sweet_dict

async def update_sweet(id: str, sweet: SweetUpdate):
    database = db.get_db()
    update_data = {k: v for k, v in sweet.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    
    result = await database.sweets.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    
    updated_sweet = await database.sweets.find_one({"_id": ObjectId(id)})
    updated_sweet["id"] = str(updated_sweet["_id"])
    return updated_sweet

async def delete_sweet(id: str):
    database = db.get_db()
    result = await database.sweets.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"message": "Sweet deleted successfully"}

from app.modules.admin.schemas import AdminUserCreate
from app.core.security import get_password_hash

async def create_admin_user(user: AdminUserCreate):
    database = db.get_db()
    existing_user = await database.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_admin": True
    }
    result = await database.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict
